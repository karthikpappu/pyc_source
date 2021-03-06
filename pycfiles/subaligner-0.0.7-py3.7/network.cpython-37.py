# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/subaligner/network.py
# Compiled at: 2020-05-03 19:52:37
# Size of source mod 2**32: 22714 bytes
import os, math, importlib, psutil, numpy as np, tensorflow as tf
import tensorflow.keras.optimizers as tf_optimizers
from tensorflow.keras.layers import Dense, Input, LSTM, Conv1D, Dropout, Activation, BatchNormalization, Bidirectional, Flatten
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, TensorBoard, CSVLogger
from tensorflow.keras.models import Model, load_model, save_model
from tensorflow.keras.utils import plot_model
import tensorflow.keras as K
from .utils import Utils
Utils.suppress_lib_logs()

class Network(object):
    __doc__ = ' Network factory creates immutable DNNs.\n    Not thread safe since the session of keras_backend is global.\n    Only factory methods are allowed when generating DNN objects.\n    '
    _Network__secret = object()
    _Network__LSTM = 'lstm'
    _Network__BI_LSTM = 'bi_lstm'
    _Network__CONV_1D = 'conv_1d'
    _Network__UNKNOWN = 'unknown'

    def __init__(self, secret, input_shape, hyperparameters, model_path=None, backend='tensorflow'):
        """ Network object initialiser used by factory methods.

        Arguments:
            secret {object} -- A hash only known by factory methods.
            input_shape {tuple} -- A shape tuple (integers), not including the batch size.
            hyperparameters {Hyperparameters} -- A configuration for hyper parameters used for training.
            model_path {string} -- The path to the model file.
            backend {string} -- The tensor manipulation backend (default: {tensorflow}). Only tensorflow is supported
                                by TF 2 and this parameter is here only for a historical reason.
        Raises:
            NotImplementedError -- Thrown when any network attributes are modified.
        """
        if not secret == Network._Network__secret:
            raise AssertionError('Only factory methods are supported when creating instances')
        else:
            Network._Network__set_keras_backend(backend)
            if hyperparameters.network_type == Network._Network__LSTM:
                self._Network__input_shape = input_shape
                self._Network__model = self._Network__lstm(input_shape, hyperparameters)
            if hyperparameters.network_type == Network._Network__BI_LSTM:
                self._Network__input_shape = input_shape
                self._Network__model = self._Network__lstm(input_shape,
                  hyperparameters, is_bidirectional=True)
            if hyperparameters.network_type == Network._Network__CONV_1D:
                self._Network__input_shape = input_shape
                self._Network__model = self._Network__conv1d(input_shape, hyperparameters)
            if input_shape is None:
                if hyperparameters.network_type == Network._Network__UNKNOWN and model_path is not None:
                    self._Network__model = load_model(model_path)
                    self._Network__input_shape = self._Network__model.input_shape[1:]
        self._Network__n_type = hyperparameters.network_type
        self.hyperparameters = hyperparameters

        def __setattr__(self, *args):
            raise NotImplementedError('Cannot modify the immutable object')

        def __delattr__(self, *args):
            raise NotImplementedError('Cannot modify the immutable object')

    @classmethod
    def get_network(cls, input_shape, hyperparameters):
        """Factory method for creating a network.

        Arguments:
            input_shape {tuple} -- A shape tuple (integers), not including the batch size.
            hyperparameters {Hyperparameters} -- A configuration for hyper parameters used for training.

        Returns:
            Network -- A constructed network object.
        """
        return cls(cls._Network__secret, input_shape, hyperparameters)

    @classmethod
    def get_from_model(cls, model_path, hyperparameters):
        """Load model into a network object.

        Arguments:
            model_path {string} -- The path to the model file.
            hyperparameters {Hyperparameters} -- A configuration for hyper parameters used for training.
        """
        hp = hyperparameters.clone()
        hp.network_type = Network._Network__UNKNOWN
        return cls((cls._Network__secret),
          None,
          hp,
          model_path=model_path)

    @classmethod
    def save_model_and_weights(cls, model_filepath, weights_filepath, combined_filepath):
        """Combine model and weights and save to a file

        Arguments:
            model_filepath {string} -- The path to the model file.
            weights_filepath {string} -- The path to the weights file.
        """
        model = load_model(model_filepath)
        model.load_weights(weights_filepath)
        model.save(combined_filepath)

    @staticmethod
    def load_model_and_weights(model_filepath, weights_filepath, hyperparameters):
        """Load weights to the Network model.

        Arguments:
            model_filepath {string} -- The model file path.
            weights_filepath {string} -- The weights file path.
            hyperparameters {Hyperparameters} -- A configuration for hyper parameters used for training.

        Returns:
            Network -- Reconstructed network object.
        """
        network = Network.get_from_model(model_filepath, hyperparameters)
        network._Network__model.load_weights(weights_filepath)
        return network

    @property
    def input_shape(self):
        """Get the input shape of the network.

        Returns:
            tuple -- The input shape of the network.
        """
        return self._Network__input_shape

    @property
    def n_type(self):
        """Get the type of the network.

        Returns:
            string -- The type of the network.
        """
        return self._Network__n_type

    @property
    def summary(self):
        """Get the summary of the network.

        Returns:
            string -- The summary of the network.
        """
        return self._Network__model.summary()

    @property
    def layers(self):
        """Get the layers of the network.

        Returns:
            list -- The statck of layers contained by the network
        """
        return self._Network__model.layers

    def get_predictions(self, input_data, weights_filepath):
        """Get a Numpy array of predictions.

        Arguments:
            input_data {numpy.ndarray} -- The input data, as a Numpy array.
            weights_filepath {string} -- The weights file path.

        Returns:
            numpy.ndarray -- The Numpy array of predictions.
        """
        self._Network__model.load_weights(weights_filepath)
        return self._Network__model.predict_on_batch(input_data)

    def fit_and_get_history(self, train_data, labels, model_filepath, weights_filepath, logs_dir, training_log, resume):
        """Fit the training data to the network and save the network model as a HDF file.

        Arguments:
            train_data {numpy.array} -- The Numpy array of training data.
            labels {numpy.array} -- The Numpy array of training labels.
            model_filepath {string} -- The model file path.
            weights_filepath {string} -- The weights file path.
            logs_dir {string} -- The TensorBoard log file directory.
            training_log {string} -- The path to the log file of epoch results.
            resume {bool} -- True to continue with previous training result or False to start a new one (default: {False}).
        Returns:
            tuple -- A tuple contains validation losses and validation accuracies.
        """
        csv_logger = CSVLogger(training_log) if not resume else CSVLogger(training_log, append=True)
        checkpoint = ModelCheckpoint(filepath=weights_filepath,
          monitor=(self.hyperparameters.monitor),
          verbose=1,
          save_best_only=False,
          save_weights_only=True)
        tensorboard = TensorBoard(log_dir=logs_dir,
          histogram_freq=0,
          write_graph=True,
          write_images=True)
        earlyStopping = EarlyStopping(monitor=(self.hyperparameters.monitor), min_delta=(self.hyperparameters.es_min_delta), mode=(self.hyperparameters.es_mode),
          patience=(self.hyperparameters.es_patience),
          verbose=1)
        callbacks_list = [
         checkpoint,
         tensorboard,
         csv_logger,
         earlyStopping]
        if not resume:
            Optimizer = getattr(tf_optimizers, self.hyperparameters.optimizer)
            self._Network__model.compile(loss=(self.hyperparameters.loss),
              optimizer=Optimizer(learning_rate=(self.hyperparameters.learning_rate)),
              metrics=(self.hyperparameters.metrics))
        initial_epoch = 0
        if resume:
            assert os.path.isfile(training_log), '{} does not exist and is required by training resumption'.format(training_log)
            training_log_file = open(training_log)
            initial_epoch += sum((1 for _ in training_log_file)) - 1
            training_log_file.close()
            assert self.hyperparameters.epochs > initial_epoch, 'Existing model has been trained for {} epochs'.format(initial_epoch)
        hist = self._Network__model.fit(train_data,
          labels,
          epochs=(self.hyperparameters.epochs),
          batch_size=(self.hyperparameters.batch_size),
          shuffle=True,
          validation_split=(self.hyperparameters.validation_split),
          verbose=1,
          callbacks=callbacks_list,
          initial_epoch=initial_epoch)
        save_model(self._Network__model, model_filepath)
        return (
         hist.history['val_loss'], hist.history['val_acc'] if int(tf.__version__.split('.')[0]) < 2 else hist.history['val_accuracy'])

    def fit_with_generator(self, train_data_raw, labels_raw, model_filepath, weights_filepath, logs_dir, training_log, resume):
        """Fit the training data to the network and save the network model as a HDF file.

        Arguments:
            train_data_raw {list} -- The HDF5 raw training data.
            labels_raw {list} -- The HDF5 raw training labels.
            model_filepath {string} -- The model file path.
            weights_filepath {string} -- The weights file path.
            logs_dir {string} -- The TensorBoard log file directory.
            training_log {string} -- The path to the log file of epoch results.
            resume {bool} -- True to continue with previous training result or False to start a new one (default: {False}).
        Returns:
            tuple -- A tuple contains validation losses and validation accuracies.
        """
        initial_epoch = 0
        batch_size = self.hyperparameters.batch_size
        validation_split = self.hyperparameters.validation_split
        csv_logger = CSVLogger(training_log)
        checkpoint = ModelCheckpoint(filepath=weights_filepath,
          monitor=(self.hyperparameters.monitor),
          verbose=1,
          save_best_only=False,
          save_weights_only=True)
        tensorboard = TensorBoard(log_dir=logs_dir,
          histogram_freq=0,
          write_graph=True,
          write_images=True)
        earlyStopping = EarlyStopping(monitor=(self.hyperparameters.monitor), min_delta=(self.hyperparameters.es_min_delta), mode=(self.hyperparameters.es_mode),
          patience=(self.hyperparameters.es_patience),
          verbose=1)
        callbacks_list = [
         checkpoint,
         tensorboard,
         csv_logger,
         earlyStopping]
        if not resume:
            Optimizer = getattr(tf_optimizers, self.hyperparameters.optimizer)
            self._Network__model.compile(loss=(self.hyperparameters.loss),
              optimizer=Optimizer(learning_rate=(self.hyperparameters.learning_rate)),
              metrics=(self.hyperparameters.metrics))
        if resume:
            assert os.path.isfile(training_log), '{} does not exist and is required by training resumption'.format(training_log)
            training_log_file = open(training_log)
            initial_epoch += sum((1 for _ in training_log_file)) - 1
            training_log_file.close()
            assert self.hyperparameters.epochs > initial_epoch, 'Existing model has been trained for {} epochs'.format(initial_epoch)
        train_generator = self._Network__generator(train_data_raw, labels_raw, batch_size, validation_split, is_validation=False)
        test_generator = self._Network__generator(train_data_raw, labels_raw, batch_size, validation_split, is_validation=True)
        steps_per_epoch = math.ceil(float(train_data_raw.shape[0]) * (1 - validation_split) / batch_size)
        validation_steps = math.ceil(float(train_data_raw.shape[0]) * validation_split / batch_size)
        hist = self._Network__model.fit(train_generator,
          steps_per_epoch=steps_per_epoch,
          validation_data=test_generator,
          validation_steps=validation_steps,
          epochs=(self.hyperparameters.epochs),
          shuffle=False,
          callbacks=callbacks_list,
          initial_epoch=initial_epoch)
        self._Network__model.save(model_filepath)
        return (
         hist.history['val_loss'], hist.history['val_acc'] if int(tf.__version__.split('.')[0]) < 2 else hist.history['val_accuracy'])

    @classmethod
    def simple_fit(cls, input_shape, train_data, labels, hyperparameters):
        """Fit the training data to the network and save the network model as a HDF file.

        Arguments:
            input_shape {tuple} -- A shape tuple (integers), not including the batch size.
            train_data {numpy.array} -- The Numpy array of training data.
            labels {numpy.array} -- The Numpy array of training labels.
            hyperparameters {Hyperparameters} -- A configuration for hyper parameters used for training.

        Returns:
            tuple -- A tuple contains validation losses and validation accuracies.
        """
        network = cls(cls._Network__secret, input_shape, hyperparameters)
        Optimizer = getattr(tf_optimizers, hyperparameters.optimizer)
        network._Network__model.compile(loss=(hyperparameters.loss),
          optimizer=Optimizer(learning_rate=(hyperparameters.learning_rate)),
          metrics=(hyperparameters.metrics))
        initial_epoch = 0
        hist = network._Network__model.fit(train_data,
          labels,
          epochs=(hyperparameters.epochs),
          batch_size=(hyperparameters.batch_size),
          shuffle=True,
          validation_split=(hyperparameters.validation_split),
          verbose=1,
          initial_epoch=initial_epoch)
        return (
         hist.history['val_loss'], hist.history['val_acc'] if int(tf.__version__.split('.')[0]) < 2 else hist.history['val_accuracy'])

    @classmethod
    def simple_fit_with_generator(cls, input_shape, train_data_raw, labels_raw, hyperparameters):
        """Fit the training data to the network and save the network model as a HDF file.

        Arguments:
            input_shape {tuple} -- A shape tuple (integers), not including the batch size.
            train_data_raw {list} -- The HDF5 raw training data.
            labels_raw {list} -- The HDF5 raw training labels.
            hyperparameters {Hyperparameters} -- A configuration for hyper parameters used for training.
        Returns:
            tuple -- A tuple contains validation losses and validation accuracies.
        """
        network = cls(cls._Network__secret, input_shape, hyperparameters)
        initial_epoch = 0
        batch_size = hyperparameters.batch_size
        validation_split = hyperparameters.validation_split
        Optimizer = getattr(tf_optimizers, hyperparameters.optimizer)
        network._Network__model.compile(loss=(hyperparameters.loss),
          optimizer=Optimizer(learning_rate=(hyperparameters.learning_rate)),
          metrics=(hyperparameters.metrics))
        train_generator = cls._Network__generator(train_data_raw, labels_raw, batch_size, validation_split, is_validation=False)
        test_generator = cls._Network__generator(train_data_raw, labels_raw, batch_size, validation_split, is_validation=True)
        steps_per_epoch = math.ceil(float(train_data_raw.shape[0]) * (1 - validation_split) / batch_size)
        validation_steps = math.ceil(float(train_data_raw.shape[0]) * validation_split / batch_size)
        hist = network._Network__model.fit(train_generator,
          steps_per_epoch=steps_per_epoch,
          validation_data=test_generator,
          validation_steps=validation_steps,
          epochs=(hyperparameters.epochs),
          shuffle=False,
          initial_epoch=initial_epoch)
        return (
         hist.history['val_loss'], hist.history['val_acc'] if int(tf.__version__.split('.')[0]) < 2 else hist.history['val_accuracy'])

    def plot_model(self, file_path):
        """Plot the network architecture in the dot format.

        Arguments:
            file_path {string} -- The path of the saved image.
        """
        plot_model((self._Network__model), to_file=file_path, show_shapes=True)

    @staticmethod
    def reset():
        K.clear_session()

    @staticmethod
    def __lstm(input_shape, hyperparameters, is_bidirectional=False):
        inputs = Input(shape=input_shape)
        hidden = BatchNormalization()(inputs)
        for nodes in hyperparameters.front_hidden_size:
            hidden = Bidirectional(LSTM(nodes))(hidden) if is_bidirectional else LSTM(nodes)(hidden)
            hidden = BatchNormalization()(hidden)
            hidden = Activation('relu')(hidden)
            hidden = Dropout(hyperparameters.dropout)(hidden)

        for nodes in hyperparameters.back_hidden_size:
            hidden = Dense(nodes)(hidden)
            hidden = BatchNormalization()(hidden)
            hidden = Activation('relu')(hidden)
            hidden = Dropout(hyperparameters.dropout)(hidden)

        hidden = Dense(1)(hidden)
        outputs = Activation('sigmoid')(hidden)
        return Model(inputs, outputs)

    @staticmethod
    def __conv1d(input_shape, hyperparameters):
        inputs = Input(shape=input_shape)
        hidden = BatchNormalization()(inputs)
        for nodes in hyperparameters.front_hidden_size:
            hidden = Conv1D(filters=nodes, kernel_size=3, activation='relu')(hidden)

        for nodes in hyperparameters.back_hidden_size:
            hidden = Dense(nodes)(hidden)
            hidden = BatchNormalization()(hidden)
            hidden = Activation('relu')(hidden)
            hidden = Dropout(hyperparameters.dropout)(hidden)

        hidden = Dense(1)(hidden)
        outputs = Activation('sigmoid')(hidden)
        return Model(inputs, outputs)

    @staticmethod
    def __set_keras_backend(backend):
        if K.backend() != backend:
            os.environ['KERAS_BACKEND'] = backend
            importlib.reload(K)
            assert K.backend() == backend, 'Unable to set backend to {}'.format(backend)
        elif backend.lower() == 'tensorflow':
            physical_core_num = psutil.cpu_count(logical=False)
            tf.config.threading.set_inter_op_parallelism_threads(physical_core_num)
            tf.config.threading.set_intra_op_parallelism_threads(physical_core_num)
            tf.config.set_soft_device_placement(True)
            physical_devices = tf.config.experimental.list_physical_devices('GPU')
            try:
                for gpu in physical_devices:
                    tf.config.experimental.set_memory_growth(gpu, True)

            except Exception:
                pass

            K.clear_session()
        else:
            if backend.lower() == 'theano' or backend.lower() == 'cntk':
                if int(tf.__version__.split('.')[0]) >= 2:
                    raise ValueError('Multi-backend is not supported')
            else:
                raise ValueError('Unknown backend: {}'.format(backend))

    @staticmethod
    def __generator(train_data_raw, labels_raw, batch_size, validation_split, is_validation):
        while 1:
            total_size = train_data_raw.shape[0]
            for i in range(0, total_size, batch_size):
                real_batch_size = total_size - i - 1 if total_size - i - 1 < batch_size else batch_size
                train_range_right = i + int(real_batch_size * (1 - validation_split))
                if is_validation:
                    batched_train_data = train_data_raw[train_range_right:i + real_batch_size]
                    batched_labels = labels_raw[train_range_right:i + real_batch_size]
                else:
                    batched_train_data = train_data_raw[i:train_range_right]
                    batched_labels = labels_raw[i:train_range_right]
                np_batched_train_data = np.array(batched_train_data)
                np_batched_labels = np.array(batched_labels)
                rand = np.random.permutation(np.arange(len(np_batched_labels)))
                np_batched_random_train_data = np_batched_train_data[rand]
                np_batched_random_labels = np_batched_labels[rand]
                np_batched_random_train_data = np.array([np.rot90(m=val, k=1, axes=(0,
                                                                                    1)) for val in np_batched_random_train_data])
                np_batched_random_train_data = np_batched_random_train_data - np.mean(np_batched_random_train_data, axis=0)
                yield (
                 np_batched_random_train_data, np_batched_random_labels)