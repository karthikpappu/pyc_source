# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/allrank/training/early_stop.py
# Compiled at: 2020-02-21 08:15:29
# Size of source mod 2**32: 596 bytes
from allrank.utils.ltr_logging import get_logger
logger = get_logger()

class EarlyStop:

    def __init__(self, patience):
        self.patience = patience
        self.best_value = 0.0
        self.best_epoch = 0

    def step(self, current_value, current_epoch):
        logger.info('Current:{} Best:{}'.format(current_value, self.best_value))
        if current_value > self.best_value:
            self.best_value = current_value
            self.best_epoch = current_epoch

    def stop_training(self, current_epoch) -> bool:
        return current_epoch - self.best_epoch > self.patience