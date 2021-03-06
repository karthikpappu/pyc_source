# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/stats/t.py
# Compiled at: 2019-08-22 04:37:04
# Size of source mod 2**32: 5992 bytes
"""
One- and two sample tests.
"""
import numpy as np
from matplotlib import pyplot, cm as colormaps
from . import _datachecks, _reml, _spm
from .. import rft1d
rank = np.linalg.matrix_rank
eps = np.finfo(float).eps

def glm(Y, X, c, Q=None, roi=None):
    """
        General linear model (for t contrasts).
        
        :Parameters:
        
        - *Y* --- (J x Q) numpy array (dependent variable)
        - *X* --- (J x B) design matrix  (J responses, B parameters)
        - *c* --- B-component contrast vector (list or array)
        - *Q* --- non-sphericity specifiers (not currently supported for **glm**)
        
        .. note:: Non-sphericity estimates are not supported for **spm1d.stats.glm**
        
        :Returns:
        
        - An **spm1d._spm.SPM_T** object.
        
        :Example:
        
        >>> t  = spm1d.stats.glm(Y, X, (-1,1))
        >>> ti = t.inference(alpha=0.05, two_tailed=True)
        >>> ti.plot()
        """
    Y = np.matrix(Y)
    X = np.matrix(X)
    c = np.matrix(c).T
    b = np.linalg.pinv(X) * Y
    eij = Y - X * b
    R = eij.T * eij
    df = Y.shape[0] - rank(X)
    sigma2 = np.diag(R) / df
    t = np.array(c.T * b).flatten() / (np.sqrt(sigma2 * float(c.T * np.linalg.inv(X.T * X) * c)) + eps)
    if Q is not None:
        df = _reml.estimate_df_T(Y, X, eij, Q)
    else:
        eij = np.asarray(eij)
        if Y.shape[1] > 1:
            fwhm = rft1d.geom.estimate_fwhm(eij)
            if roi is None:
                resels = rft1d.geom.resel_counts(eij, fwhm, element_based=False)
            else:
                B = np.any((np.isnan(eij)), axis=0)
                B = np.logical_and(np.logical_not(B), roi)
                mask = np.logical_not(B)
                resels = rft1d.geom.resel_counts(mask, fwhm, element_based=False)
                t = np.ma.masked_array(t, np.logical_not(roi))
            s = np.asarray(sigma2).flatten()
            t = _spm.SPM_T(t, (1, df), fwhm, resels, (np.asarray(X)), (np.asarray(b)), eij, sigma2=s, roi=roi)
        else:
            b, r, s2 = np.asarray(b).flatten(), eij.flatten(), float(sigma2)
        t = _spm.SPM0D_T(t, (1, df), beta=b, residuals=r, sigma2=s2)
    return t


def regress(Y, x, roi=None):
    """
        Simple linear regression.
        
        :Parameters:
        
        - *Y* --- (J x Q) numpy array (dependent variable)
        - *x* --- J-component list or array (independent variable)
        
        :Returns:
        
        - An **spm1d._spm.SPM_T** object.
        
        :Example:
        
        >>> Y  = np.random.rand(10, 101)
        >>> Y  = spm1d.util.smooth(Y, fwhm=10)
        >>> x  = np.random.rand(10)
        >>> t  = spm1d.stats.regress(Y, x)
        >>> ti = t.inference(alpha=0.05)
        >>> ti.plot()
        
        :Notes:
                - the correlation coefficient is retrievable as "t.r" where "t" is the output from **spm1d.stats.regress**
                - statistical inferences are based on *t*, not on *r*
        """
    Y = _datachecks.asmatrix(Y, dtype=float)
    _datachecks.check('regress', Y, x)
    J = Y.shape[0]
    X = np.ones((J, 2))
    X[:, 0] = x
    c = [1, 0]
    spmt = glm(Y, X, c, roi=roi)
    spmt.r = spmt.z / (J - 2 + spmt.z ** 2) ** 0.5
    spmt.isregress = True
    return spmt


def ttest(Y, y0=None, roi=None):
    """
        One-sample t test.
        
        :Parameters:
        
        - *Y* --- (J x Q) data array  (J responses, Q nodes)
        - *y0* --- optional Q-component datum array (default is the null continuum)
        
        :Returns:
        
        - An **spm1d._spm.SPM_T** object.
        
        :Example:
        
        >>> Y  = np.random.randn(8, 101)
        >>> Y  = spm1d.util.smooth(Y, fwhm=15)
        >>> t  = spm1d.stats.ttest(Y)
        >>> ti = t.inference(alpha=0.05, two_tailed=True)
        >>> ti.plot()
        """
    Y = _datachecks.asmatrix(Y, dtype=float)
    _datachecks.check('ttest', Y, y0)
    J = Y.shape[0]
    Ytemp = Y.copy()
    if y0 is not None:
        Ytemp -= y0
    X = np.ones((J, 1))
    c = 1
    return glm(Ytemp, X, c, roi=roi)


def ttest_paired(YA, YB, roi=None):
    """
        Paired t test.
        
        :Parameters:
        
        - *YA* --- (J x Q) data array  (J responses, Q nodes)
        - *YB* --- (J x Q) data array  (J responses, Q nodes)

        :Returns:
        
        - An **spm1d._spm.SPM_T** object.
        
        :Example:
        
        >>> YA,YB  = np.random.randn(8, 101), np.random.randn(8, 101)
        >>> YA,YB  = spm1d.util.smooth(Y, fwhm=10), spm1d.util.smooth(Y, fwhm=10)
        
        >>> t      = spm1d.stats.ttest_paired(YA, YB)
        >>> ti = t.inference(alpha=0.05)
        >>> ti.plot()
        """
    YA, YB = _datachecks.asmatrix(YA, dtype=float), _datachecks.asmatrix(YB, dtype=float)
    _datachecks.check('ttest_paired', YA, YB)
    return ttest((YA - YB), roi=roi)


def ttest2(YA, YB, equal_var=False, roi=None):
    """
        Two-sample t test.
        
        :Parameters:
        
        - *YA* --- (J x Q) data array  (J responses, Q nodes)
        - *YB* --- (J x Q) data array  (J responses, Q nodes)
        - *equal_var* --- If *True*, equal group variance will be assumed
        
        :Returns:
        
        - An **spm1d._spm.SPM_T** object.
        
        :Example:
        
        >>> YA,YB  = np.random.randn(8, 101), np.random.randn(8, 101)
        >>> YA,YB  = spm1d.util.smooth(Y, fwhm=10), spm1d.util.smooth(Y, fwhm=10)
        
        >>> t  = spm1d.stats.ttest2(YA, YB)
        >>> ti = t.inference(alpha=0.05)
        >>> ti.plot()
        """
    YA, YB = _datachecks.asmatrix(YA, dtype=float), _datachecks.asmatrix(YB, dtype=float)
    _datachecks.check('ttest2', YA, YB)
    JA, JB = YA.shape[0], YB.shape[0]
    Y = np.vstack((YA, YB))
    X = np.zeros((JA + JB, 2))
    X[:JA, 0] = 1
    X[JA:, 1] = 1
    c = (1, -1)
    Q = None
    if not equal_var:
        J = JA + JB
        q0, q1 = np.eye(JA), np.eye(JB)
        Q0, Q1 = np.matrix(np.zeros((J, J))), np.matrix(np.zeros((J, J)))
        Q0[:JA, :JA] = q0
        Q1[JA:, JA:] = q1
        Q = [Q0, Q1]
    return glm(Y, X, c, Q, roi=roi)