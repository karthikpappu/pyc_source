# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/ppo2/microbatched_model.py
# Compiled at: 2019-07-10 12:45:57
# Size of source mod 2**32: 3340 bytes
import numpy as np, tensorflow as tf
from deephyper.search.nas.baselines.ppo2.model import Model

class MicrobatchedModel(Model):
    __doc__ = '\n    Model that does training one microbatch at a time - when gradient computation\n    on the entire minibatch causes some overflow\n    '

    def __init__(self, *, policy, ob_space, ac_space, nbatch_act, nbatch_train, nsteps, ent_coef, vf_coef, max_grad_norm, microbatch_size):
        self.nmicrobatches = nbatch_train // microbatch_size
        self.microbatch_size = microbatch_size
        assert nbatch_train % microbatch_size == 0, 'microbatch_size ({}) should divide nbatch_train ({}) evenly'.format(microbatch_size, nbatch_train)
        super().__init__(policy=policy,
          ob_space=ob_space,
          ac_space=ac_space,
          nbatch_act=nbatch_act,
          nbatch_train=microbatch_size,
          nsteps=nsteps,
          ent_coef=ent_coef,
          vf_coef=vf_coef,
          max_grad_norm=max_grad_norm)
        self.grads_ph = [tf.placeholder(dtype=(g.dtype), shape=(g.shape)) for g in self.grads]
        grads_ph_and_vars = list(zip(self.grads_ph, self.var))
        self._apply_gradients_op = self.trainer.apply_gradients(grads_ph_and_vars)

    def train(self, lr, cliprange, observations, advs, returns, actions, values, neglogpacs, **_kwargs):
        advs = (advs - advs.mean()) / (advs.std() + 1e-08)
        stats_vs = []
        for microbatch_idx in range(self.nmicrobatches):
            _sli = range(microbatch_idx * self.microbatch_size, (microbatch_idx + 1) * self.microbatch_size)
            td_map = {self.train_model.X: observations[_sli], 
             self.A: actions[_sli], 
             self.ADV: advs[_sli], 
             self.RETURNS: returns[_sli], 
             self.LR: lr, 
             self.CLIPRANGE: cliprange, 
             self.OLDNEGLOGPAC: neglogpacs[_sli], 
             self.VALUE_PREV: values[_sli]}
            sliced_kwargs = {key:_kwargs[key][_sli] for key in _kwargs}
            td_map.update((self.train_model.feed_dict)(**sliced_kwargs))
            grad_v, stats_v = self.sess.run([
             self.grads, self.stats_list], td_map)
            if microbatch_idx == 0:
                sum_grad_v = grad_v
            else:
                for i, g in enumerate(grad_v):
                    sum_grad_v[i] += g

            stats_vs.append(stats_v)

        feed_dict = {ph:sum_g / self.nmicrobatches for ph, sum_g in zip(self.grads_ph, sum_grad_v)}
        feed_dict[self.LR] = lr
        self.sess.run(self._apply_gradients_op, feed_dict)
        return np.mean((np.array(stats_vs)), axis=0).tolist()