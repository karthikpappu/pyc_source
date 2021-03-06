# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/pytransit/models/ma_uniform.py
# Compiled at: 2020-03-28 19:16:40
# Size of source mod 2**32: 5791 bytes
from typing import Union
from numpy import ndarray, squeeze, zeros, asarray
from numba.ma_uniform_nb import uniform_model_v, uniform_model_s, uniform_model_pv
from .transitmodel import TransitModel
__all__ = [
 'UniformModel']

class UniformModel(TransitModel):

    def evaluate(self, k: Union[(float, ndarray)], t0: Union[(float, ndarray)], p: Union[(float, ndarray)], a: Union[(float, ndarray)], i: Union[(float, ndarray)], e: Union[(float, ndarray)]=None, w: Union[(float, ndarray)]=None, copy: bool=True) -> ndarray:
        """Evaluates the uniform transit model for a set of scalar or vector parameters.

        Parameters
        ----------
        k
            Radius ratio(s) either as a single float, 1D vector, or 2D array.
        t0
            Transit center(s) as a float or a 1D vector.
        p
            Orbital period(s) as a float or a 1D vector.
        a
            Orbital semi-major axis (axes) divided by the stellar radius as a float or a 1D vector.
        i
            Orbital inclination(s) as a float or a 1D vector.
        e
            Orbital eccentricity as a float or a 1D vector.
        w
            Argument of periastron as a float or a 1D vector.
        copy

        Notes
        -----
        The model can be evaluated either for one set of parameters or for many sets of parameters simultaneously.
        The orbital parameters can be given either as a float or a 1D array-like (preferably ndarray for optimal speed.)

        Returns
        -------
        Transit model
        """
        k = asarray(k)
        if isinstance(t0, float):
            if e is None:
                e, w = (0.0, 0.0)
            flux = uniform_model_s(self.time, k, t0, p, a, i, e, w, self.lcids, self.pbids, self.nsamples, self.exptimes, self._es, self._ms, self._tae)
        else:
            npv = t0.size
            if e is None:
                e, w = zeros(npv), zeros(npv)
            k = asarray(k)
            if k.ndim == 1:
                k = k.reshape((k.size, 1))
            flux = uniform_model_v(self.time, k, t0, p, a, i, e, w, self.lcids, self.pbids, self.nsamples, self.exptimes, self._es, self._ms, self._tae)
        return squeeze(flux)

    def evaluate_ps(self, k: float, t0: float, p: float, a: float, i: float, e: float=0.0, w: float=0.0) -> ndarray:
        """Evaluate the transit model for a set of scalar parameters.

         Parameters
         ----------
         k : array-like
             Radius ratio(s) either as a single float or an 1D array.
         t0 : float
             Transit center as a float.
         p : float
             Orbital period as a float.
         a : float
             Orbital semi-major axis divided by the stellar radius as a float.
         i : float
             Orbital inclination(s) as a float.
         e : float, optional
             Orbital eccentricity as a float.
         w : float, optional
             Argument of periastron as a float.

         Notes
         -----
         This version of the `evaluate` method is optimized for calculating a single transit model (such as when using a
         local optimizer). If you want to evaluate the model for a large number of parameters simultaneously, use either
         `evaluate` or `evaluate_pv`.

         Returns
         -------
         ndarray
             Modelled flux as a 1D ndarray.
         """
        if self.time is None:
            raise ValueError('Need to set the data before calling the transit model.')
        k = asarray(k)
        flux = uniform_model_s(self.time, k, t0, p, a, i, e, w, self.lcids, self.pbids, self.nsamples, self.exptimes, self._es, self._ms, self._tae)
        return squeeze(flux)

    def evaluate_pv(self, pvp: ndarray) -> ndarray:
        """Evaluate the transit model for a 2D parameter array.

         Parameters
         ----------
         pvp
             Parameter array with a shape `(npv, npar)` where `npv` is the number of parameter vectors, and each row
             contains a set of parameters `[k, t0, p, a, i, e, w]`. The radius ratios can also be given per passband,
             in which case the row should be structured as `[k_0, k_1, k_2, ..., k_npb, t0, p, a, i, e, w]`.

         Notes
         -----
         This version of the `evaluate` method is optimized for calculating several models in parallel, such as when
         using *emcee* for MCMC sampling.

         Returns
         -------
         ndarray
             Modelled flux either as a 1D or 2D ndarray.
         """
        assert self.time is not None, 'Need to set the data before calling the transit model.'
        flux = uniform_model_pv(self.time, pvp, self.lcids, self.pbids, self.nsamples, self.exptimes, self._es, self._ms, self._tae)
        return squeeze(flux)