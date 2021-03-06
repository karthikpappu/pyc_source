# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/optimizer/optimizer.py
# Compiled at: 2019-07-11 14:24:06
# Size of source mod 2**32: 5451 bytes
from sys import float_info
from skopt import Optimizer as SkOptimizer
from skopt.learning import RandomForestRegressor, ExtraTreesRegressor, GradientBoostingQuantileRegressor
import numpy as np
from deephyper.search import util
from deephyper.benchmark import HpProblem
logger = util.conf_logger('deephyper.search.hps.optimizer.optimizer')

class Optimizer:
    SEED = 12345
    KAPPA = 1.96

    def __init__(self, problem, num_workers, args):
        if not args.learner in ('RF', 'ET', 'GBRT', 'GP', 'DUMMY'):
            raise AssertionError(f"Unknown scikit-optimize base_estimator: {args.learner}")
        else:
            if args.learner == 'RF':
                base_estimator = RandomForestRegressor(n_jobs=(-1))
            else:
                if args.learner == 'ET':
                    base_estimator = ExtraTreesRegressor(n_jobs=(-1))
                else:
                    if args.learner == 'GBRT':
                        base_estimator = GradientBoostingQuantileRegressor(n_jobs=(-1))
                    else:
                        base_estimator = args.learner
                self.space = problem.space
                cs_kwargs = self.space['create_structure'].get('kwargs')
                if cs_kwargs is None:
                    structure = self.space['create_structure']['func']()
                else:
                    structure = (self.space['create_structure']['func'])(**cs_kwargs)
            n_init = np.inf if args.learner == 'DUMMY' else num_workers
            self.starting_points = []
            skopt_space = [(0, vnode.num_ops - 1) for vnode in structure.variable_nodes]
            self._optimizer = SkOptimizer(skopt_space,
              base_estimator=base_estimator,
              acq_optimizer='sampling',
              acq_func=(args.acq_func),
              acq_func_kwargs={'kappa': self.KAPPA},
              random_state=(self.SEED),
              n_initial_points=n_init)
            assert args.liar_strategy in 'cl_min cl_mean cl_max'.split()
        self.strategy = args.liar_strategy
        self.evals = {}
        self.counter = 0
        logger.info('Using skopt.Optimizer with %s base_estimator' % args.learner)

    def _get_lie(self):
        if self.strategy == 'cl_min':
            if self._optimizer.yi:
                return min(self._optimizer.yi)
            return 0.0
        else:
            if self.strategy == 'cl_mean':
                if self._optimizer.yi:
                    return np.mean(self._optimizer.yi)
                else:
                    return 0.0
            if self._optimizer.yi:
                return max(self._optimizer.yi)
            return 0.0

    def _xy_from_dict(self):
        XX = list(self.evals.keys())
        YY = [-self.evals[x] for x in XX]
        return (XX, YY)

    def to_dict(self, x):
        cfg = self.space.copy()
        cfg['arch_seq'] = list(x)
        return cfg

    def _ask(self):
        if len(self.starting_points) > 0:
            x = self.starting_points.pop()
        else:
            x = self._optimizer.ask()
        y = self._get_lie()
        key = tuple(x)
        if key not in self.evals:
            self.counter += 1
            self._optimizer.tell(x, y)
            self.evals[key] = y
            logger.debug(f"_ask: {x} lie: {y}")
        else:
            logger.debug(f"Duplicate _ask: {x} lie: {y}")
        return self.to_dict(x)

    def ask(self, n_points=None, batch_size=20):
        if n_points is None:
            return self._ask()
        batch = []
        for _ in range(n_points):
            batch.append(self._ask())
            if len(batch) == batch_size:
                yield batch
                batch = []

        if batch:
            yield batch

    def ask_initial(self, n_points):
        if len(self.starting_points) > 0:
            XX = [self.starting_points.pop() for i in range(min(n_points, len(self.starting_points)))]
            if len(XX) < n_points:
                XX += self._optimizer.ask(n_points=(n_points - len(XX)))
        else:
            XX = self._optimizer.ask(n_points=n_points)
        for x in XX:
            y = self._get_lie()
            key = tuple(x)
            if key not in self.evals:
                self.counter += 1
                self._optimizer.tell(x, y)
                self.evals[key] = y

        return [self.to_dict(x) for x in XX]

    def tell(self, xy_data):
        if not isinstance(xy_data, list):
            raise AssertionError(f"where type(xy_data)=={type(xy_data)}")
        else:
            minval = min(self._optimizer.yi) if self._optimizer.yi else 0.0
            for x, y in xy_data:
                key = tuple(x['arch_seq'])
                assert key in self.evals, f"where key=={key} and self.evals=={self.evals}"
                logger.debug(f"tell: {x} --> {key}: evaluated objective: {y}")
                self.evals[key] = y if y > float_info.min else minval

            self._optimizer.Xi = []
            self._optimizer.yi = []
            XX, YY = self._xy_from_dict()
            assert len(XX) == len(YY) == self.counter, f"where len(XX)=={len(XX)},len(YY)=={len(YY)}, self.counter=={self.counter}"
            self._optimizer.tell(XX, YY)
            assert len(self._optimizer.Xi) == len(self._optimizer.yi) == self.counter, f"where len(self._optimizer.Xi)=={len(self._optimizer.Xi)}, len(self._optimizer.yi)=={len(self._optimizer.yi)},self.counter=={self.counter}"