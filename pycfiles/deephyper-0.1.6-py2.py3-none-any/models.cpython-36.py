# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/deepq/models.py
# Compiled at: 2019-07-10 12:45:57
# Size of source mod 2**32: 6394 bytes
import tensorflow as tf, tensorflow.contrib.layers as layers

def _mlp(hiddens, input_, num_actions, scope, reuse=False, layer_norm=False):
    with tf.variable_scope(scope, reuse=reuse):
        out = input_
        for hidden in hiddens:
            out = layers.fully_connected(out,
              num_outputs=hidden, activation_fn=None)
            if layer_norm:
                out = layers.layer_norm(out, center=True, scale=True)
            out = tf.nn.relu(out)

        q_out = layers.fully_connected(out,
          num_outputs=num_actions, activation_fn=None)
        return q_out


def mlp(hiddens=[], layer_norm=False):
    """This model takes as input an observation and returns values of all actions.

    Parameters
    ----------
    hiddens: [int]
        list of sizes of hidden layers
    layer_norm: bool
        if true applies layer normalization for every layer
        as described in https://arxiv.org/abs/1607.06450

    Returns
    -------
    q_func: function
        q_function for DQN algorithm.
    """
    return lambda *args, **kwargs: _mlp(hiddens, *args, layer_norm=layer_norm, **kwargs)


def _cnn_to_mlp(convs, hiddens, dueling, input_, num_actions, scope, reuse=False, layer_norm=False):
    with tf.variable_scope(scope, reuse=reuse):
        out = input_
        with tf.variable_scope('convnet'):
            for num_outputs, kernel_size, stride in convs:
                out = layers.convolution2d(out, num_outputs=num_outputs,
                  kernel_size=kernel_size,
                  stride=stride,
                  activation_fn=(tf.nn.relu))

        conv_out = layers.flatten(out)
        with tf.variable_scope('action_value'):
            action_out = conv_out
            for hidden in hiddens:
                action_out = layers.fully_connected(action_out,
                  num_outputs=hidden, activation_fn=None)
                if layer_norm:
                    action_out = layers.layer_norm(action_out,
                      center=True, scale=True)
                action_out = tf.nn.relu(action_out)

            action_scores = layers.fully_connected(action_out,
              num_outputs=num_actions, activation_fn=None)
        if dueling:
            with tf.variable_scope('state_value'):
                state_out = conv_out
                for hidden in hiddens:
                    state_out = layers.fully_connected(state_out,
                      num_outputs=hidden, activation_fn=None)
                    if layer_norm:
                        state_out = layers.layer_norm(state_out,
                          center=True, scale=True)
                    state_out = tf.nn.relu(state_out)

                state_score = layers.fully_connected(state_out,
                  num_outputs=1, activation_fn=None)
            action_scores_mean = tf.reduce_mean(action_scores, 1)
            action_scores_centered = action_scores - tf.expand_dims(action_scores_mean, 1)
            q_out = state_score + action_scores_centered
        else:
            q_out = action_scores
        return q_out


def cnn_to_mlp(convs, hiddens, dueling=False, layer_norm=False):
    """This model takes as input an observation and returns values of all actions.

    Parameters
    ----------
    convs: [(int, int, int)]
        list of convolutional layers in form of
        (num_outputs, kernel_size, stride)
    hiddens: [int]
        list of sizes of hidden layers
    dueling: bool
        if true double the output MLP to compute a baseline
        for action scores
    layer_norm: bool
        if true applies layer normalization for every layer
        as described in https://arxiv.org/abs/1607.06450

    Returns
    -------
    q_func: function
        q_function for DQN algorithm.
    """
    return lambda *args, **kwargs: _cnn_to_mlp(convs, hiddens, dueling, *args, layer_norm=layer_norm, **kwargs)


def build_q_func(network, hiddens=[
 256], dueling=True, layer_norm=False, **network_kwargs):
    if isinstance(network, str):
        from deephyper.search.nas.baselines.common.models import get_network_builder
        network = (get_network_builder(network))(**network_kwargs)

    def q_func_builder(input_placeholder, num_actions, scope, reuse=False):
        with tf.variable_scope(scope, reuse=reuse):
            latent = network(input_placeholder)
            if isinstance(latent, tuple):
                if latent[1] is not None:
                    raise NotImplementedError('DQN is not compatible with recurrent policies yet')
                latent = latent[0]
            latent = layers.flatten(latent)
            with tf.variable_scope('action_value'):
                action_out = latent
                for hidden in hiddens:
                    action_out = layers.fully_connected(action_out,
                      num_outputs=hidden, activation_fn=None)
                    if layer_norm:
                        action_out = layers.layer_norm(action_out,
                          center=True, scale=True)
                    action_out = tf.nn.relu(action_out)

                action_scores = layers.fully_connected(action_out,
                  num_outputs=num_actions, activation_fn=None)
            if dueling:
                with tf.variable_scope('state_value'):
                    state_out = latent
                    for hidden in hiddens:
                        state_out = layers.fully_connected(state_out,
                          num_outputs=hidden, activation_fn=None)
                        if layer_norm:
                            state_out = layers.layer_norm(state_out,
                              center=True, scale=True)
                        state_out = tf.nn.relu(state_out)

                    state_score = layers.fully_connected(state_out,
                      num_outputs=1, activation_fn=None)
                action_scores_mean = tf.reduce_mean(action_scores, 1)
                action_scores_centered = action_scores - tf.expand_dims(action_scores_mean, 1)
                q_out = state_score + action_scores_centered
            else:
                q_out = action_scores
            return q_out

    return q_func_builder