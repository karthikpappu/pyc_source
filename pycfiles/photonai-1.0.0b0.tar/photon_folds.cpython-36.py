# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nwinter/PycharmProjects/photon_projects/photon_core/photonai/processing/photon_folds.py
# Compiled at: 2019-09-16 11:08:55
# Size of source mod 2**32: 4914 bytes
import uuid, numpy as np
from sklearn.model_selection import GroupKFold, GroupShuffleSplit, LeaveOneGroupOut, StratifiedKFold, StratifiedShuffleSplit, ShuffleSplit
from photonai.photonlogger import Logger
from photonai.processing.cross_validation import StratifiedKFoldRegression

class FoldInfo:

    def __init__(self, fold_id=None, fold_nr: int=0, train_indices: list=None, test_indices: list=None):
        self.fold_id = fold_id
        self.fold_nr = fold_nr
        self.train_indices = train_indices
        self.test_indices = test_indices

    @staticmethod
    def _data_overview(y):
        if len(y.shape) > 1:
            Logger().info('One Hot Encoded data fold information not yet implemented')
            return {}
        else:
            unique, counts = np.unique(y, return_counts=True)
            unique = [str(u) for u in unique]
            counts = [int(c) for c in counts]
            return dict(zip(unique, counts))

    @staticmethod
    def generate_folds(cv_strategy, X, y, kwargs, eval_final_performance=True, test_size=0.2):
        """
        Generates the training and  test set indices for the hyperparameter search
        Returns a tuple of training and test indices

        - If there is a strategy given for the outer cross validation the strategy is called to split the data
            - additionally, if a group variable and a GroupCV is passed, split data according to groups
            - if a group variable and a StratifiedCV is passed, split data according to groups and ignore targets when
            stratifying the data
            - if no group variable but a StratifiedCV is passed, split data according to targets
        - If no strategy is given and eval_final_performance is True, all data is used for training
        - If no strategy is given and eval_final_performance is False: a test set is seperated from the
          training and validation set by the parameter test_size with ShuffleSplit
        """
        if 'groups' in kwargs.keys():
            groups = kwargs['groups']
        else:
            groups = None
        if cv_strategy is not None:
            if groups is not None:
                if isinstance(cv_strategy, (GroupKFold, GroupShuffleSplit, LeaveOneGroupOut)):
                    try:
                        data_test_cases = cv_strategy.split(X, y, groups)
                    except:
                        Logger().error('Could not split data according to groups')

            if groups is not None:
                if isinstance(cv_strategy, (StratifiedKFoldRegression,
                 StratifiedKFold,
                 StratifiedShuffleSplit)):
                    try:
                        data_test_cases = cv_strategy.split(X, groups)
                    except:
                        Logger().error('Could not stratify data for outer cross validation according to group variable')

            data_test_cases = cv_strategy.split(X, y)
        else:
            if not eval_final_performance:
                data_test_cases = FoldInfo._yield_all_data(X)
            else:
                train_test_cv_object = ShuffleSplit(n_splits=1, test_size=test_size)
                data_test_cases = train_test_cv_object.split(X, y)
        fold_objects = list()
        for i, (train_indices, test_indices) in enumerate(data_test_cases):
            fold_info_obj = FoldInfo(fold_id=(uuid.uuid4()), fold_nr=(i + 1),
              train_indices=train_indices,
              test_indices=test_indices)
            fold_objects.append(fold_info_obj)

        return fold_objects

    @staticmethod
    def _yield_all_data(X):
        """
        Helper function that iteratively returns the data stored in self.X
        Returns an iterable version of self.X
        """
        if hasattr(X, 'shape'):
            yield (
             np.asarray(list(range(X.shape[0]))), [])
        else:
            yield (
             np.asarray(list(range(len(X)))), [])