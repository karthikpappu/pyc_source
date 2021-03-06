# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/plasma/models/builder.py
# Compiled at: 2017-02-17 21:50:27
from keras.models import Sequential
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM, SimpleRNN
from keras.utils.data_utils import get_file
from keras.layers.wrappers import TimeDistributed
from keras.callbacks import Callback
from keras.optimizers import *
from keras.regularizers import l1, l2, l1l2
import dill, re, os
from copy import deepcopy

class LossHistory(Callback):

    def on_train_begin(self, logs=None):
        self.losses = []

    def on_batch_end(self, batch, logs=None):
        self.losses.append(logs.get('loss'))


class ModelBuilder:

    def __init__(self, conf):
        self.conf = conf

    def get_unique_id(self):
        num_epochs = self.conf['training']['num_epochs']
        this_conf = deepcopy(self.conf)
        this_conf['training']['num_epochs'] = 0
        unique_id = hash(dill.dumps(this_conf))
        return unique_id

    def build_model(self, predict, custom_batch_size=None):
        conf = self.conf
        model_conf = conf['model']
        rnn_size = model_conf['rnn_size']
        rnn_type = model_conf['rnn_type']
        optimizer = model_conf['optimizer']
        lr = model_conf['lr']
        clipnorm = model_conf['clipnorm']
        regularization = model_conf['regularization']
        if optimizer == 'sgd':
            optimizer_class = SGD
        else:
            if optimizer == 'adam':
                optimizer_class = Adam
            elif optimizer == 'rmsprop':
                optimizer_class = RMSprop
            elif optimizer == 'nadam':
                optimizer_class = Nadam
            else:
                optimizer = optimizer
            if lr is not None or clipnorm is not None:
                optimizer = optimizer_class(lr=lr, clipnorm=clipnorm)
            loss_fn = conf['data']['target'].loss
            dropout_prob = model_conf['dropout_prob']
            length = model_conf['length']
            pred_length = model_conf['pred_length']
            skip = model_conf['skip']
            stateful = model_conf['stateful']
            return_sequences = model_conf['return_sequences']
            output_activation = conf['data']['target'].activation
            num_signals = conf['data']['num_signals']
            batch_size = self.conf['training']['batch_size']
            if predict:
                batch_size = self.conf['model']['pred_batch_size']
                if return_sequences:
                    length = pred_length
                else:
                    length = 1
            if custom_batch_size is not None:
                batch_size = custom_batch_size
            if rnn_type == 'LSTM':
                rnn_model = LSTM
            elif rnn_type == 'SimpleRNN':
                rnn_model = SimpleRNN
            else:
                print 'Unkown Model Type, exiting.'
                exit(1)
            batch_input_shape = (batch_size, length, num_signals)
            model = Sequential()
            for _ in range(model_conf['rnn_layers']):
                model.add(rnn_model(rnn_size, return_sequences=return_sequences, batch_input_shape=batch_input_shape, stateful=stateful, W_regularizer=l2(regularization), U_regularizer=l2(regularization), b_regularizer=l2(regularization), dropout_W=dropout_prob, dropout_U=dropout_prob))
                model.add(Dropout(dropout_prob))

        if return_sequences:
            model.add(TimeDistributed(Dense(1, activation=output_activation)))
        else:
            model.add(Dense(1, activation=output_activation))
        model.compile(loss=loss_fn, optimizer=optimizer)
        model.reset_states()
        return model

    def build_train_test_models(self):
        return (
         self.build_model(False), self.build_model(True))

    def save_model_weights(self, model, epoch):
        save_path = self.get_save_path(epoch)
        model.save_weights(save_path, overwrite=True)

    def get_save_path(self, epoch):
        unique_id = self.get_unique_id()
        return self.conf['paths']['model_save_path'] + ('model.{}._epoch_.{}.h5').format(unique_id, epoch)

    def load_model_weights(self, model):
        epochs = self.get_all_saved_files()
        if len(epochs) == 0:
            print 'no previous checkpoint found'
            return -1
        else:
            max_epoch = min(self.conf['training']['num_epochs'] - 1, max(epochs))
            print ('loading from epoch {}').format(max_epoch)
            model.load_weights(self.get_save_path(max_epoch))
            return max_epoch

    def get_latest_save_path(self):
        epochs = self.get_all_saved_files()
        if len(epochs) == 0:
            print 'no previous checkpoint found'
            return ''
        else:
            max_epoch = min(self.conf['training']['num_epochs'], max(epochs))
            print ('loading from epoch {}').format(max_epoch)
            return self.get_save_path(max_epoch)

    def extract_id_and_epoch_from_filename(self, filename):
        regex = re.compile('-?\\d+')
        numbers = [ int(x) for x in regex.findall(filename) ]
        assert len(numbers) == 3
        assert numbers[2] == 5
        return (numbers[0], numbers[1])

    def get_all_saved_files(self):
        unique_id = self.get_unique_id()
        filenames = os.listdir(self.conf['paths']['model_save_path'])
        epochs = []
        for file in filenames:
            curr_id, epoch = self.extract_id_and_epoch_from_filename(file)
            if curr_id == unique_id:
                epochs.append(epoch)

        return epochs