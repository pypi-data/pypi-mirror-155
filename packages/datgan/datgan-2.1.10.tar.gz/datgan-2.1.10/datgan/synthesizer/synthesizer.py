#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File that describes the Synthesizer for the DATGAN
"""
import os
import json
import time
import numpy as np
from tqdm import tqdm
import tensorflow as tf
from sklearn.preprocessing import OneHotEncoder

from datgan.utils.utils import elapsed_time
from datgan.synthesizer.generator import Generator
from datgan.synthesizer.discriminator import Discriminator

# Loss functions
from datgan.synthesizer.losses.SGANLoss import SGANLoss
from datgan.synthesizer.losses.WGANLoss import WGANLoss
from datgan.synthesizer.losses.WGGPLoss import WGGPLoss


class Synthesizer:
    """
    Synthesizer for the DATGAN model
    """

    def __init__(self, output, metadata, dag, batch_size, z_dim, noise, learning_rate, g_period, l2_reg, num_gen_rnn,
                 num_gen_hidden, num_dis_layers, num_dis_hidden, label_smoothing, loss_function, var_order, n_sources,
                 conditional_inputs, save_checkpoints, restore_session, verbose):
        """
        Constructs all the necessary attributes for the DATGANSynthesizer class.

        Parameters
        ----------
        output: str
            Output path
        metadata: dict
            Information about the data.
        dag: networkx.DiGraph
            Directed Acyclic Graph provided by the user.
        batch_size: int
            Size of the batch to feed the model at each step. Defined in the DATGAN class.
        z_dim: int
            Dimension of the noise vector used as an input to the generator. Defined in the DATGAN class.
        noise: float
            Upper bound to the gaussian noise added to with the label smoothing. (only used if label_smoothing is
            set to 'TS' or 'OS') Defined in the DATGAN class.
        learning_rate: float
            Learning rate. Defined in the DATGAN class.
        g_period: int
            Every "g_period" steps, train the generator once. (Used to train the discriminator more than the generator)
        l2_reg: bool
            Tell the model to use L2 regularization while training both NNs.
        num_gen_rnn: int
            Size of the hidden units in the LSTM cell. Defined in the DATGAN class.
        num_gen_hidden: int
            Size of the hidden layer used on the output of the generator to act as a convolution. Defined in the DATGAN
            class.
        num_dis_layers: int
            Number of layers for the discriminator. Defined in the DATGAN class.
        num_dis_hidden: int
            Size of the hidden layers in the discriminator. Defined in the DATGAN class.
        label_smoothing: str
            Type of label smoothing. Defined in the DATGAN class.
        loss_function: str
            Name of the loss function to be used. Defined in the DATGAN class.
        var_order: list[str]
            Ordered list for the variables. Used in the Generator.
        n_sources: int
            Number of source nodes in the DAG.
        conditional_inputs: list
            List of variables in the dataset that are used as inputs to the model.
        save_checkpoints: bool, default True
            Whether to store checkpoints of the model after each training epoch.
        restore_session: bool, default True
            Whether continue training from the last checkpoint.
        verbose: int
            Level of verbose.
        """

        self.output = output
        self.metadata = metadata
        self.dag = dag
        self.batch_size = batch_size
        self.z_dim = z_dim
        self.noise = noise
        self.learning_rate = learning_rate
        self.g_period = g_period
        self.l2_reg = l2_reg
        self.num_gen_rnn = num_gen_rnn
        self.num_gen_hidden = num_gen_hidden
        self.num_dis_layers = num_dis_layers
        self.num_dis_hidden = num_dis_hidden
        self.label_smoothing = label_smoothing
        self.loss_function = loss_function
        self.var_order = var_order
        self.n_sources = n_sources
        self.conditional_inputs = conditional_inputs
        self.save_checkpoints = save_checkpoints
        self.restore_session = restore_session
        self.verbose = verbose

        # Checkpoints
        self.checkpoint = None
        self.checkpoint_manager = None
        self.checkpoint_dir = self.output + 'checkpoints'
        self.checkpoint_prefix = os.path.join(self.checkpoint_dir, "ckpt")

        # Transformer
        self.onehot = OneHotEncoder(categories=[np.array(self.var_order)], sparse=False)

        # Other parameters
        self.generator = None
        self.discriminator = None
        self.qnet = None
        self.optimizerD = None
        self.optimizerG = None
        self.loss = None
        self.data = None
        self.logging = {}

        # zero value
        self.zero = tf.Variable(0, dtype=tf.float32)

        # Categorical Cross Entropy
        self.sce = tf.keras.losses.CategoricalCrossentropy(from_logits=True)

    def fit(self, encoded_data, num_epochs):
        """
        Fit the synthesizer

        Parameters
        ----------
        encoded_data: dict
            Dictionary of the encoded data to be transformed into a tensor.
        num_epochs: int
            Number of epochs
        """

        self.initialize()

        self.data = (tf.data.Dataset.from_tensor_slices(encoded_data)
                     .shuffle(self.metadata['len'], reshuffle_each_iteration=True)
                     .batch(self.batch_size, drop_remainder=True))

        # Verbose stuff
        if self.verbose == 1:
            iterable_epochs = tqdm(range(self.checkpoint.epoch.numpy(), num_epochs), desc="Training DATGAN")
        else:
            iterable_epochs = range(self.checkpoint.epoch.numpy(), num_epochs)

        if self.verbose == 2:
            # Time for training each epoch
            time_epoch = []

        # Keep track of all the iterations for the WGAN and WGGP loss
        iter_ = 0

        # Prepare the logs if the dict is empty
        if not self.logging:
            self.loss.prepare_logs(self.logging)

        for epoch in iterable_epochs:

            if self.verbose == 2:
                iterable_steps = tqdm(self.data, desc="Epoch {}/{}".format(epoch + 1, num_epochs))
                start_time = time.perf_counter()
            else:
                iterable_steps = self.data

            # Prepare the logs for the current epoch
            tmp_logs = {}
            self.loss.prepare_logs(tmp_logs)

            for batch in iterable_steps:

                # Get the conditional data
                cond_batch_dict = {}
                for c in self.conditional_inputs:
                    col_info = self.metadata['details'][c]
                    if col_info['type'] == 'categorical':
                        # Add some uniform noise to the categorical data
                        noise = tf.random.uniform(batch[c].shape, minval=0, maxval=self.noise/col_info['n'])
                        cat_cond_data = (batch[c] + noise)
                        cond_batch_dict[c] =  cat_cond_data/tf.reduce_sum(cat_cond_data, keepdims=True, axis=1)
                    else:
                        cond_batch_dict[c] = batch[c]

                # Reset the logs in the class for the loss function
                self.loss.reset_logs()

                # Make one step of training
                discr_logs, gen_logs = self.train_step(batch, cond_batch_dict, (iter_ % self.g_period == 0))

                # Get the logs and temporarily save them
                logs = {'discriminator': discr_logs, 'generator': gen_logs}

                for nn in logs.keys():
                    for k in logs[nn].keys():
                        if not self.l2_reg and k == 'reg_loss':
                            pass

                        tmp_logs[nn][k].append(logs[nn][k].numpy())

                # Update the iterations
                iter_ += 1

            # Get the average values for the logs
            for nn in tmp_logs.keys():
                for k in tmp_logs[nn].keys():
                    self.logging[nn][k].append(np.mean(tmp_logs[nn][k], dtype=np.float64))

            # Save the log file
            with open(os.path.join(self.output, 'logging.json'), 'w') as outfile:
                json.dump(self.logging, outfile)

            self.checkpoint.epoch.assign_add(1)

            # Save a checkpoint or at least the last model
            if self.save_checkpoints or int(self.checkpoint.epoch.numpy()) == num_epochs:
                self.checkpoint_manager.save()

            if self.verbose == 2:
                end_time = time.perf_counter()
                print("\033[1mEpoch {}\033[0m finished. time: {:.2f} seconds".format(int(self.checkpoint.epoch.numpy()),
                                                                                     end_time - start_time))
                print("Generator:")
                print("  {} loss: {:.2e}".format(self.loss_function, self.logging['generator']['gen_loss'][-1]))
                print("  KL div.: {:.2e}".format(self.logging['generator']['kl_div'][-1]))
                if self.loss_function == 'SGAN':
                    print("  Reg. loss: {:.2e}".format(self.logging['generator']['reg_loss'][-1]))
                print("\033[1m  Gen. loss: {:.2e}\033[0m".format(self.logging['generator']['loss'][-1]))

                print("Discriminator:")
                if self.loss_function == 'SGAN':
                    print("  Accuracy original: {:.1f}%".format(self.logging['discriminator']['acc_orig'][-1] * 100))
                    print("  Accuracy synthetic: {:.1f}%".format(self.logging['discriminator']['acc_synth'][-1] * 100))
                    print("  SGAN loss: {:.2e}".format(self.logging['discriminator']['discr_loss'][-1]))
                    print("  Reg. loss: {:.2e}".format(self.logging['discriminator']['reg_loss'][-1]))

                else:
                    print("  Wasserstein loss on real data: {:.2e}".format(
                        self.logging['discriminator']['loss_real'][-1]))
                    print("  Wasserstein loss on fake data: {:.2e}".format(
                        self.logging['discriminator']['loss_fake'][-1]))

                    if self.loss_function == 'WGGP':
                        print("  Wasserstein loss: {:.2e}".format(self.logging['discriminator']['wass_loss'][-1]))
                        print("  Grad. pen.: {:.2e}".format(self.logging['discriminator']['grad_pen'][-1]))

                print("\033[1m  Discr. loss: {:.2e}\033[0m".format(self.logging['discriminator']['loss'][-1]))

                # Remaining training time
                if self.checkpoint.epoch.numpy() < num_epochs:
                    time_epoch.append(end_time - start_time)
                    if len(time_epoch) < 5:
                        avg = np.mean(time_epoch)
                    else:
                        avg = np.mean(time_epoch[-5:])
                    remaining_time = avg * (num_epochs - self.checkpoint.epoch.numpy())
                    print("Remaining training time around \033[1m{}\033[0m.".format(elapsed_time(remaining_time)))

                print()

    def initialize(self):
        """
        Initialize different stuff for fitting the DATGAN model
        """

        # Load the generator and the discriminator
        self.generator = Generator(self.metadata, self.dag, self.batch_size, self.z_dim, self.num_gen_rnn,
                                   self.num_gen_hidden, self.var_order, self.loss_function, self.l2_reg,
                                   self.conditional_inputs, self.verbose)

        self.discriminator = Discriminator(self.num_dis_layers, self.num_dis_hidden, self.loss_function, self.l2_reg)

        # Get the optimizer depending on the loss function
        if self.loss_function == 'SGAN':
            # Optimizers
            self.optimizerG = tf.keras.optimizers.Adam(learning_rate=self.learning_rate, beta_1=0.5, beta_2=0.9)
            self.optimizerD = tf.keras.optimizers.Adam(learning_rate=self.learning_rate, beta_1=0.5, beta_2=0.9)

            # Loss function
            self.loss = SGANLoss(self.metadata, self.var_order)

        elif self.loss_function == 'WGAN':
            # Optimizers
            self.optimizerG = tf.keras.optimizers.RMSprop(learning_rate=self.learning_rate)
            self.optimizerD = tf.keras.optimizers.RMSprop(learning_rate=self.learning_rate)

            # Loss function
            self.loss = WGANLoss(self.metadata, self.var_order)
        elif self.loss_function == 'WGGP':
            # Optimizers
            self.optimizerG = tf.keras.optimizers.Adam(learning_rate=self.learning_rate, beta_1=0.0, beta_2=0.9)
            self.optimizerD = tf.keras.optimizers.Adam(learning_rate=self.learning_rate, beta_1=0.0, beta_2=0.9)

            # Loss function
            self.loss = WGGPLoss(self.metadata, self.var_order)

        self.checkpoint = tf.train.Checkpoint(epoch=tf.Variable(0),
                                              generator_optimizer=self.optimizerG,
                                              discriminator_optimizer=self.optimizerD,
                                              generator=self.generator,
                                              discriminator=self.discriminator)

        self.checkpoint_manager = tf.train.CheckpointManager(self.checkpoint, self.checkpoint_dir, max_to_keep=3)

        # Restore from checkpoints
        self.restore_models()

    def restore_models(self):
        """
        Restore the models from the checkpoint
        """
        if self.restore_session:
            # Restore the models
            self.checkpoint.restore(self.checkpoint_manager.latest_checkpoint)
            if self.checkpoint_manager.latest_checkpoint:
                if self.verbose > 0:
                    print("Restored models from epoch {:d}.".format(int(self.checkpoint.epoch.numpy())))

                # Reload the logs
                with open(os.path.join(self.output, 'logging.json'), 'r') as infile:
                    self.logging = json.load(infile)

    @tf.function
    def train_step(self, batch, cond_batch_dict, train_gen):
        """
        Do one step of the training process

        Parameters
        ----------
        batch: dict
            Dictionary of the original encoded data
        cond_batch_dict: dict
            Dictionary of values from the conditional inputs
        train_gen: bool
            Boolean value telling the model if it should train the Generator for this step

        Returns
        -------
        dict x2:
            Dictionary of log values for both the generator and the discriminator

        """
        noise = tf.random.normal([self.n_sources, self.batch_size, self.z_dim])

        # Transformed the data in a tensor
        batch_orig = self.transform_data(batch, synthetic=True)

        with tf.GradientTape() as gen_tape, tf.GradientTape() as disc_tape:

            # Only train the generator every g_period steps
            synth = self.generator(noise, cond_batch_dict, training=True)

            # Transform the data
            batch_synth = self.transform_data(synth, synthetic=True)

            # Use the discriminator on the original and synthetic data
            orig_output = self.discriminator(batch_orig, training=True)
            synth_output = self.discriminator(batch_synth, training=True)

            # Compute the loss function for the discriminator
            if self.loss_function in ['SGAN', 'WGAN']:
                discr_loss = self.loss.discr_loss(orig_output,
                                                  synth_output,
                                                  tf.reduce_sum(self.discriminator.losses))
            else:  # self.loss_function == 'WGGP'

                # Compute interpolated values
                alpha = tf.random.uniform(shape=[self.batch_size, 1], minval=0., maxval=1.)
                batch_interp = alpha * batch_orig + (tf.ones_like(alpha) - alpha) * batch_synth

                with tf.GradientTape() as gp_tape:
                    gp_tape.watch(batch_interp)
                    interp_output = self.discriminator(batch_interp, training=True)
                interp_grad = gp_tape.gradient(interp_output, batch_interp)

                discr_loss = self.loss.discr_loss(orig_output,
                                                  synth_output,
                                                  interp_grad,
                                                  tf.reduce_sum(self.discriminator.losses))

            # If we need to train the generator, compute its loss function...
            if train_gen:
                gen_loss = self.loss.gen_loss(synth_output,
                                              batch_orig,
                                              batch_synth,
                                              tf.reduce_sum(self.generator.losses))

        # ... and apply the gradients
        if train_gen:
            gen_grad = gen_tape.gradient(gen_loss, self.generator.trainable_variables)
            self.optimizerG.apply_gradients(zip(gen_grad, self.generator.trainable_variables))

        # Apply one step of optimization for the Discriminator
        discr_grad = disc_tape.gradient(discr_loss, self.discriminator.trainable_variables)
        self.optimizerD.apply_gradients(zip(discr_grad, self.discriminator.trainable_variables))

        # Apply clipping on the weights of the discriminator for the WGAN loss
        if self.loss_function == 'WGAN':
            for w in self.discriminator.trainable_variables:
                w.assign(tf.clip_by_value(w, -0.01, 0.01))

        return self.loss.get_logs('discriminator'), self.loss.get_logs('generator') if train_gen else {}

    def transform_data(self, dict_, synthetic):
        """
        Transform the original or the synthetic data in torch.Tensor.

        Parameters
        ----------
        dict_: dict
            Dictionary of the encoded data
        synthetic: bool
            Boolean value to say if we are passing the synthetic or original data

        Returns
        -------
        tensor: tf.Tensor
            Transformed encoded data
        """

        data = []

        for col in self.var_order:
            # Get info
            col_info = self.metadata['details'][col]

            if col_info['type'] == 'categorical':

                # Synthetic data
                val = dict_[col]

                # Label smoothing
                if col not in self.conditional_inputs:
                    if (synthetic and self.label_smoothing == 'TS') or \
                            ((not synthetic) and self.label_smoothing in ['TS', 'OS']):
                        noise = tf.random.uniform(val.shape, minval=0, maxval=self.noise / col_info['n'])
                        val = (val + noise) / tf.reduce_sum(val + noise, keepdims=True, axis=1)

                data.append(val)

            elif col_info['type'] == 'continuous':
                # Add values
                data.append(dict_[col][:, :col_info['n']])

                # Add probabilities
                data.append(dict_[col][:, col_info['n']:])

        return tf.concat(data, axis=1)

    def get_cond_batch(self, dict_):
        """
        Get the batch of data for the conditional inputs

        Parameters
        ----------
        dict_: dict
            Dictionary of the encoded data

        Returns
        -------
        tensor: tf.Tensor
            Input data
        """

        if len(self.conditional_inputs) > 0:
            data = []

            for col in self.conditional_inputs:
                data.append(dict_[col])

            return tf.concat(data, axis=1)
        else:
            return None

    def sample(self, cond_inputs):
        """
        Use the generator to sample data

        Parameters
        ----------
        cond_inputs: dict of tf.Tensor
            Values of conditional inputs

        Returns
        -------
        samples: numpy.ndarray
            Matrix of encoded synthetic variables
        """

        # Compute the noise
        z = tf.random.normal([self.n_sources, self.batch_size, self.z_dim])

        # Generate data
        synth = self.generator(z, cond_inputs)

        for col in self.var_order:
            synth[col] = synth[col].numpy()

        return synth
