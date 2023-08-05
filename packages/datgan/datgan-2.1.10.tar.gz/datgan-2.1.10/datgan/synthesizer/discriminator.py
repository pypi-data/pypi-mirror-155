#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File that describes the QNet for the DATGAN (as used in the InfoGAN)
"""

import tensorflow as tf
from tensorflow.keras import layers
from tensorflow import keras


class Discriminator(keras.Model):
    """
    The discriminator is a fully connected neural network. Exactly the same as in TGAN. The only difference is that
    Layer Normalization is used instead of Batch Normalization with the 'WGGP' loss.

    """

    def __init__(self, num_dis_layers, num_dis_hidden, loss_function, l2_reg):
        """
        Initialize the model

        Parameters
        ----------
        num_dis_layers: int
            Number of layers for the discriminator. (Default value in class DATGAN: 1)
        num_dis_hidden: int
            Size of the hidden layers in the discriminator. (Default value in class DATGAN: 100)
        loss_function: str
            Name of the loss function to be used. (Defined in the class DATGAN)
        l2_reg: bool
            Use l2 regularization or not
        """
        super().__init__()
        self.num_dis_layers = num_dis_layers
        self.num_dis_hidden = num_dis_hidden
        self.loss_function = loss_function
        self.l2_reg = l2_reg

        # Batch diversity parameters
        self.n_kernels = 5
        self.kernel_dim = 3

        # Regularizer
        if self.l2_reg:
            self.kern_reg = tf.keras.regularizers.L2(1e-5)
        else:
            self.kern_reg = None

        self.list_layers = None
        self.batch_tensor = None
        self.build_layers()

    def build_layers(self):
        """
        Build the layers of the Discriminator.
        """

        self.list_layers = []

        for i in range(self.num_dis_layers):

            if i == 0:
                internal = [layers.Dense(self.num_dis_hidden,
                                         kernel_initializer=tf.keras.initializers.TruncatedNormal(stddev=0.1),
                                         kernel_regularizer=self.kern_reg)]
            else:
                internal = [layers.Dense(self.num_dis_hidden,
                                         kernel_regularizer=self.kern_reg)]

            # Add the layer for the batch_diversity
            internal.append(layers.Dense(self.n_kernels*self.kernel_dim,
                                         kernel_regularizer=self.kern_reg))

            # No need to use the scale parameters for the normalization since the results will be passed to the Dropout
            # and LeakyReLU layers
            if self.loss_function == 'WGGP':
                internal.append(layers.LayerNormalization(center=True,
                                                          scale=False,
                                                          beta_regularizer=self.kern_reg))
            else:
                # Don't use the gamma parameters in the BatchNormalization
                internal.append(layers.BatchNormalization(center=True,
                                                          scale=False,
                                                          beta_regularizer=self.kern_reg))

            internal.append(layers.Dropout(0.5))

            internal.append(layers.LeakyReLU())

            self.list_layers.append(internal)

        if self.loss_function == 'SGAN':
            self.list_layers.append(layers.Dense(1,
                                                 activation='sigmoid',
                                                 kernel_regularizer=self.kern_reg))
        else:
            self.list_layers.append(layers.Dense(1,
                                                 kernel_regularizer=self.kern_reg))

    def call(self, x):
        """
        Compute the Discriminator value

        Parameters
        ----------
        x: torch.Tensor
            A Torch Tensor of dimensions (N, n_features)

        Returns
        -------
        torch.Tensor:
            Critic of the current input of dimensions (N, 1)
        """

        for i in range(self.num_dis_layers):
            internal = self.list_layers[i]

            # Initial layer
            x = internal[0](x)

            # Concatenation with batch diversity
            x = tf.concat([x, self.batch_diversity(internal[1](x))], axis=1)

            # Pass through LayerNorm or BatchNorm
            x = internal[2](x)

            # Dropout
            x = internal[3](x)

            # LeakyReLU
            x = internal[4](x)

        # Pass through the output layer
        return self.list_layers[-1](x)

    def batch_diversity(self, input_tensor):
        """
        Return the minibatch discrimination vector as defined by Salimans et al., 2016.


        Parameters
        ----------
        input_tensor: tf.keras.layers.Dense
            Input layer

        Returns
        -------
        tensorflow.Tensor:
            batch diversity tensor

        """
        activation = tf.reshape(input_tensor, (-1, self.n_kernels, self.kernel_dim))

        # Calculate the L1 and then the sum of the negative exponential
        diffs = tf.expand_dims(activation, 3) - tf.expand_dims(tf.transpose(activation, [1, 2, 0]), 0)
        abs_diffs = tf.reduce_sum(tf.abs(diffs), 2)
        minibatch_features = tf.reduce_sum(tf.exp(-abs_diffs), 2)

        return minibatch_features

    def mini_batch_discriminator(self, features, num_features, kernels, kernerl_dim):
        """
        Return the minibatch discrimination vector as defined by Salimans et al., 2016.

        Parameters
        ----------
        features: tf.keras.layers.Dense
            Input layer
        num_features: int
            Number of features
        kernels: int
            Number of kernels
        kernerl_dim: int
            Dimension of the kernel

        Returns
        -------
        tensorflow.Tensor:
            batch diversity tensor
        """
        features = tf.reshape(features, [-1, num_features])
        M1 = tf.reshape(features, [-1, 1, num_features])
        M2 = tf.reshape(features, [1, -1, num_features])
        diff = tf.exp(-tf.reduce_sum(tf.abs(M1 - M2), axis=3))
        return tf.reduce_sum(diff, axis=0)

