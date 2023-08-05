#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tensorflow as tf


class GANLoss(tf.keras.losses.Loss):
    """
    Generic class for the loss function
    """

    def __init__(self, metadata, var_order, name="GENERIC_CLASS"):
        """
        Initialize the class

        Parameters
        ----------
        metadata: dict
            Metadata for the columns (used when computing the kl divergence)
        var_order: list
            Ordered list of the variables
        name: string
            Name of the loss function
        """
        super().__init__(name=name)

        self.logs = {}
        self.reset_logs()

        self.metadata = metadata
        self.var_order = var_order

        self.kl = tf.keras.losses.KLDivergence()

    def kl_div(self, original, synthetic):
        """
        Compute the KL divergence on the right variables.

        Parameters
        ----------
        original: tf.Tensor
            Tensor for the original encoded variables
        synthetic: tf.Tensor
            Tensor for the synthetic encoded variables

        Returns
        -------
        tf.Tensor:
            Sum of the KL divergences for the right variables

        """
        # KL loss
        kl_div = tf.constant(0.0)
        ptr = tf.constant(0, dtype=tf.int64)

        # Go through all variables
        for col in self.var_order:
            # Get info
            col_info = self.metadata['details'][col]

            if col_info['type'] == 'continuous':
                # Skip the value. We only compute the KL on the probability vector
                ptr += tf.constant(col_info['n'], dtype=tf.int64)

            pred = tf.reduce_sum(synthetic[:, ptr:ptr + col_info['n']], axis=0)
            pred = pred / tf.reduce_sum(pred)

            real = tf.reduce_sum(original[:, ptr:ptr + col_info['n']], axis=0)
            real = real / tf.reduce_sum(real)

            kl_div += self.kl(pred, real)
            ptr += tf.constant(col_info['n'], dtype=tf.int64)

        return kl_div

    def reset_logs(self):
        """
        Reset the logs of the loss to empty dictionaries
        """
        self.logs = {'discriminator': {}, 'generator': {}}

    def get_logs(self, key):
        """
        Return the logs of the loss
        """
        return self.logs[key]
