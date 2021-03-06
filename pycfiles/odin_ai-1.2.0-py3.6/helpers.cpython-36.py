# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/odin/bay/helpers.py
# Compiled at: 2019-08-11 16:50:28
# Size of source mod 2**32: 3549 bytes
from __future__ import absolute_import, division, print_function
from enum import Flag, auto
from numbers import Number
import numpy as np, tensorflow as tf
from tensorflow_probability import distributions as tfd
from odin.bay import distributions as obd

class Statistic(Flag):
    SAMPLE = auto()
    MEAN = auto()
    VAR = auto()
    STDDEV = auto()
    DIST = auto()


def _dist2text(dist):
    return '[%s]%s batch:%s event:%s' % (dist.__class__.__name__, dist.dtype.name,
     dist.batch_shape, dist.event_shape)


def _extract_desc(dist, name, pad):
    text = pad + (name + ':' if len(name) > 0 else '') + _dist2text(dist) + '\n'
    obj_type = type(dist)
    for key in dir(dist):
        val = getattr(dist, key)
        if isinstance(val, tfd.Distribution) and not isinstance(getattr(obj_type, key, None), property):
            text += _extract_desc(val, key, pad + ' ')

    return text


def print_dist(dist, return_text=False):
    assert isinstance(dist, tfd.Distribution)
    text = _extract_desc(dist, '', '')
    if return_text:
        return text[:-1]
    print(text)


def kl_divergence(q, p, use_analytic_kl=False, q_sample=lambda q: q.sample(), reduce_axis=(), auto_remove_independent=True, name=None):
    """ Calculating KL(q(x)||p(x))

  Parameters
  ----------
  q : tensorflow_probability.Distribution
    the posterior distribution

  p : tensorflow_probability.Distribution
    the prior distribution

  use_analytic_kl : bool (default: False)
    if True, use the close-form solution\xa0 for

  q_sample : {callable, Tensor, Number}
    callable for extracting sample from `q(x)` (takes q distribution
    as input argument)

  reudce_axis : {None, int, tuple}
    reduce axis when use MCMC to estimate KL divergence, default
    `()` mean keep all original dimensions

  auto_remove_independent : bool (default: True)
    if `q` or `p` is `tfd.Independent` wrapper, get the original
    distribution for calculating the analytic KL

  name : {None, str}

  Returns
  -------
  """
    if auto_remove_independent:
        if isinstance(q, tfd.Independent):
            if not isinstance(p, tfd.Independent):
                q = q.distribution
        if not isinstance(q, tfd.Independent):
            if isinstance(p, tfd.Independent):
                p = p.distribution
    q_name = [i for i in q.name.split('/') if len(i) > 0][(-1)]
    p_name = [i for i in p.name.split('/') if len(i) > 0][(-1)]
    with tf.compat.v1.name_scope(name, 'KL_q%s_p%s' % (q_name, p_name)):
        if bool(use_analytic_kl):
            return tfd.kl_divergence(q, p)
        else:
            if callable(q_sample):
                z = q_sample(q)
            else:
                if isinstance(q_sample, Number):
                    z = q.sample(int(q_sample))
                else:
                    z = q_sample
            kl = q.log_prob(z) - p.log_prob(z)
            kl = tf.reduce_mean(input_tensor=kl, axis=reduce_axis)
            return kl