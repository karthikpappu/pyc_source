# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\pipeline\integration.py
# Compiled at: 2018-08-27 17:21:06
import numpy as np
from xicam import config
from PySide import QtCore
import multiprocessing, time, pyFAI, msg
pyFAI_method = 'cython'
from modpkgs import pyFAImod

def pixel_2Dintegrate(dimg, mask=None):
    centerx = dimg.experiment.getvalue('Center X')
    centery = dimg.experiment.getvalue('Center Y')
    if mask is None:
        msg.logMessage('No mask defined, creating temporary empty mask.', msg.INFO)
        mask = np.zeros_like(dimg.rawdata)
    data = dimg.transformdata * mask
    x, y = np.indices(data.shape)
    r = np.sqrt((x - centerx) ** 2 + (y - centery) ** 2)
    r = r.astype(np.int)
    tbin = np.bincount(r.ravel(), data.ravel())
    nr = np.bincount(r.ravel(), mask.ravel())
    radialprofile = tbin / nr
    return radialprofile


def chi_2Dintegrate(imgdata, cen, mu, mask=None, chires=30):
    """
    Integration over r for a chi range. Output is 30*
    """
    if mask is None:
        msg.logMessage('No mask defined, creating temporary empty mask..', msg.INFO)
        mask = np.zeros_like(imgdata)
    data = imgdata * (1 - mask)
    x, y = np.indices(data.shape).astype(np.float)
    r = np.sqrt((x - cen[0]) ** 2 + (y - cen[1]) ** 2)
    r = r.astype(np.int)
    delta = 3
    rinf = mu - delta / 2.0
    rsup = mu + delta / 2.0
    rmask = ((rinf < r) & (r < rsup) & (x < cen[0])).astype(np.int)
    data *= rmask
    chi = chires * np.arctan((y - cen[1]) / (x - cen[0]))
    chi += chires * np.pi / 2.0
    chi = np.round(chi).astype(np.int)
    chi *= chi > 0
    tbin = np.bincount(chi.ravel(), data.ravel())
    nr = np.bincount(chi.ravel(), rmask.ravel())
    angleprofile = tbin / nr
    return angleprofile


def radialintegratepyFAI(data, mask=None, AIdict=None, cut=None, color=[255, 255, 255], requestkey=None, qvrt=None, qpar=None):
    if mask is None:
        mask = config.activeExperiment.mask
    if AIdict is None:
        AI = config.activeExperiment.getAI()
    else:
        AI = pyFAI.AzimuthalIntegrator()
        AI.setPyFAI(**AIdict)
    if mask is not None:
        mask = mask.copy()
    msg.logMessage(('image:', data.shape), msg.DEBUG)
    msg.logMessage(('mask:', mask.shape), msg.DEBUG)
    if not mask.shape == data.shape:
        msg.logMessage('No mask match. Mask will be ignored.', msg.WARNING)
        mask = np.ones_like(data)
        msg.logMessage(('emptymask:', mask.shape), msg.DEBUG)
    if cut is not None and type(cut) is np.ndarray:
        msg.logMessage(('cut:', cut.shape), msg.DEBUG)
        mask = mask.astype(bool) & cut.astype(bool)
    q, radialprofile = AI.integrate1d(data.T, config.settings['Integration Bins (q)'], mask=1 - mask.T, method=pyFAI_method)
    q = q / 10.0
    return (
     q.tolist(), radialprofile.tolist(), color, requestkey)


def chiintegratepyFAI(data, mask, AIdict, cut=None, color=[255, 255, 255], requestkey=None, qvrt=None, qpar=None, xres=config.settings['Integration Bins (χ)'], yres=config.settings['Integration Bins (q)']):
    AI = pyFAI.AzimuthalIntegrator()
    AI.setPyFAI(**AIdict)
    if mask is not None:
        mask = mask.copy()
    msg.logMessage(('image:', data.shape), msg.DEBUG)
    msg.logMessage(('mask:', mask.shape), msg.DEBUG)
    if not mask.shape == data.shape:
        msg.logMessage('No mask match. Mask will be ignored.', msg.WARNING)
        mask = np.ones_like(data)
        msg.logMessage(('emptymask:', mask.shape), msg.DEBUG)
    if cut is not None:
        msg.logMessage(('cut:', cut.shape), msg.DEBUG)
        mask &= cut.astype(bool)
    cake, q, chi = AI.integrate2d(data.T, xres, yres, method=pyFAI_method)
    mask, q, chi = AI.integrate2d(mask.T, xres, yres, method=pyFAI_method)
    maskedcake = np.ma.masked_array(cake, mask=mask <= 0)
    chiprofile = np.ma.average(maskedcake, axis=1)
    return (
     chi.tolist(), chiprofile.tolist(), color, requestkey)


def xintegrate(data, mask, AIdict, cut=None, color=[255, 255, 255], requestkey=None, qvrt=None, qpar=None):
    if mask is not None:
        mask = mask.copy()
    msg.logMessage(('image:', data.shape), msg.DEBUG)
    msg.logMessage(('mask:', mask.shape), msg.DEBUG)
    if not mask.shape == data.shape:
        msg.logMessage('No mask match. Mask will be ignored.', msg.WARNING)
        mask = np.ones_like(data)
        msg.logMessage(('emptymask:', mask.shape), msg.INFO)
    if cut is not None:
        msg.logMessage(('cut:', cut.shape), msg.DEBUG)
        mask &= cut.astype(bool)
    maskeddata = np.ma.masked_array(data, mask=1 - mask)
    xprofile = np.ma.average(maskeddata, axis=1)
    AI = pyFAI.AzimuthalIntegrator()
    AI.setPyFAI(**AIdict)
    qx = AI.qArray(data.shape[::-1])[int(AI.getFit2D()['centerY']), :] / 10
    qx[:qx.argmin()] *= -1
    return (
     qx.tolist(), xprofile.tolist(), color, requestkey)


def zintegrate(data, mask, AIdict, cut=None, color=[255, 255, 255], requestkey=None, qvrt=None, qpar=None):
    if mask is not None:
        mask = mask.copy()
    msg.logMessage(('image:', data.shape), msg.DEBUG)
    msg.logMessage(('mask:', mask.shape), msg.DEBUG)
    if not mask.shape == data.shape:
        msg.logMessage('No mask match. Mask will be ignored.', msg.WARNING)
        mask = np.ones_like(data)
        msg.logMessage(('emptymask:', mask.shape), msg.DEBUG)
    if cut is not None:
        msg.logMessage(('cut:', cut.shape), msg.DEBUG)
        mask &= cut.astype(bool)
    maskeddata = np.ma.masked_array(data, mask=1 - mask)
    xprofile = np.ma.average(maskeddata, axis=0)
    AI = pyFAI.AzimuthalIntegrator()
    AI.setPyFAI(**AIdict)
    qz = AI.qArray(data.shape[::-1])[:, int(AI.getFit2D()['centerX'])] / 10
    qz[:qz.argmin()] *= -1
    return (
     qz.tolist(), xprofile.tolist(), color, requestkey)


def cake(imgdata, experiment, mask=None, xres=config.settings['Integration Bins (χ)'], yres=config.settings['Integration Bins (q)']):
    if mask is None:
        mask = np.zeros_like(imgdata)
    AI = experiment.getAI()
    return AI.integrate2d(imgdata.T, xres, yres, mask=1 - mask.T)


def GetArc(Imagedata, center, radius1, radius2, angle1, angle2):
    mask = np.zeros_like(Imagedata)
    centerx = center[0]
    centery = center[1]
    y, x = np.indices(Imagedata.shape)
    r = np.sqrt((x - centerx) ** 2 + (y - centery) ** 2)
    mask = (r > radius1) & (r < radius2)
    theta = np.arctan2(y - centery, x - centerx) / 2 / np.pi * 360
    mask &= (theta > angle1) & (theta < angle2)
    mask = np.flipud(mask)
    return mask * Imagedata


def qintegrate(*args, **kwargs):
    return radialintegratepyFAI(*args, **kwargs)


def cakexintegrate(data, mask, AIdict, cut=None, color=[255, 255, 255], requestkey=None, qvrt=None, qpar=None):
    AI = pyFAI.AzimuthalIntegrator()
    AI.setPyFAI(**AIdict)
    if not mask.shape == data.shape:
        msg.logMessage('No mask match. Mask will be ignored.', msg.WARNING)
        mask = np.ones_like(data)
        msg.logMessage(('emptymask:', mask.shape), msg.DEBUG)
    if cut is not None:
        msg.logMessage(('cut:', cut.shape), msg.DEBUG)
        mask &= cut.astype(bool)
    chi = np.arange(-180, 180, 360 / config.settings['Integration Bins (χ)'])
    maskeddata = np.ma.masked_array(data, mask=1 - mask)
    xprofile = np.ma.average(maskeddata, axis=1)
    return (
     chi.tolist(), xprofile.tolist(), color, requestkey)


def cakezintegrate(data, mask, AIdict, cut=None, color=[255, 255, 255], requestkey=None, qvrt=None, qpar=None):
    AI = pyFAI.AzimuthalIntegrator()
    AI.setPyFAI(**AIdict)
    if not mask.shape == data.shape:
        msg.logMessage('No mask match. Mask will be ignored.', msg.WARNING)
        mask = np.ones_like(data)
        msg.logMessage(('emptymask:', mask.shape), msg.DEBUG)
    if cut is not None:
        msg.logMessage(('cut:', cut.shape), msg.DEBUG)
        mask &= cut.astype(bool)
    q = np.arange(config.settings['Integration Bins (q)']) * np.max(qpar) / 10.0 / config.settings['Integration Bins (q)']
    maskeddata = np.ma.masked_array(data, mask=1 - mask)
    zprofile = np.ma.average(maskeddata, axis=0)
    return (
     q.tolist(), zprofile.tolist(), color, requestkey)


def remeshqintegrate(data, mask, AIdict, cut=None, color=[255, 255, 255], requestkey=None, qvrt=None, qpar=None):
    alphai = config.activeExperiment.getvalue('Incidence Angle (GIXS)')
    msg.logMessage('Incoming angle applied to remeshed q integration: ' + str(alphai), msg.DEBUG)
    if mask is None:
        mask = config.activeExperiment.mask
    if AIdict is None:
        AI = config.activeExperiment.getAI()
    else:
        AI = pyFAI.AzimuthalIntegrator()
        AI.setPyFAI(**AIdict)
    if mask is not None:
        mask = mask.copy()
    msg.logMessage(('image:', data.shape), msg.DEBUG)
    msg.logMessage(('mask:', mask.shape), msg.DEBUG)
    if not mask.shape == data.shape:
        msg.logMessage('No mask match. Mask will be ignored.', msg.WARNING)
        mask = np.ones_like(data)
        msg.logMessage(('emptymask:', mask.shape), msg.DEBUG)
    if cut is not None and type(cut) is np.ndarray:
        msg.logMessage(('cut:', cut.shape), msg.DEBUG)
        mask = mask.astype(bool) & cut.astype(bool)
    qsquared = qpar ** 2 + qvrt ** 2
    remeshcenter = np.unravel_index(qsquared.argmin(), qsquared.shape)
    print 'center?:', remeshcenter
    f2d = AI.getFit2D()
    f2d['centerX'] = remeshcenter[0]
    f2d['centerY'] = remeshcenter[1]
    AI.setFit2D(**f2d)
    AIdict = AI.getPyFAI()
    msg.logMessage('remesh corrected calibration: ' + str(AIdict))
    AI._cached_array['q_center'] = np.sqrt(qsquared).T / 10
    q, radialprofile = AI.integrate1d(data.T, config.settings['Integration Bins (q)'], mask=1 - mask.T, method=pyFAI_method)
    return (
     q, radialprofile, color, requestkey)


def remeshchiintegrate(data, mask, AIdict, cut=None, color=[255, 255, 255], requestkey=None, qvrt=None, qpar=None):
    AI = pyFAI.AzimuthalIntegrator()
    AI.setPyFAI(**AIdict)
    alphai = config.activeExperiment.getvalue('Incidence Angle (GIXS)')
    msg.logMessage('Incoming angle applied to remeshed q integration: ' + str(alphai), msg.DEBUG)
    qsquared = qpar ** 2 + qvrt ** 2
    remeshcenter = np.unravel_index(qsquared.argmin(), qsquared.shape)
    f2d = AI.getFit2D()
    f2d['centerX'] = remeshcenter[0]
    f2d['centerY'] = remeshcenter[1]
    AI.setFit2D(**f2d)
    AIdict = AI.getPyFAI()
    return chiintegratepyFAI(data, mask, AIdict, cut, color, requestkey, qvrt=None, qpar=None)


def remeshxintegrate(data, mask, AIdict, cut=None, color=[255, 255, 255], requestkey=None, qvrt=None, qpar=None):
    AI = pyFAI.AzimuthalIntegrator()
    AI.setPyFAI(**AIdict)
    if not mask.shape == data.shape:
        msg.logMessage('No mask match. Mask will be ignored.', msg.WARNING)
        mask = np.ones_like(data)
        msg.logMessage(('emptymask:', mask.shape), msg.DEBUG)
    if cut is not None:
        msg.logMessage(('cut:', cut.shape), msg.DEBUG)
        mask &= cut.astype(bool)
    center = np.where(np.abs(qpar) == np.abs(qpar).min())
    qx = qpar[:, center[0][0]] / 10.0
    maskeddata = np.ma.masked_array(data, mask=1 - mask)
    xprofile = np.ma.average(maskeddata, axis=1)
    return (
     qx.tolist(), xprofile.tolist(), color, requestkey)


def remeshzintegrate(data, mask, AIdict, cut=None, color=[255, 255, 255], requestkey=None, qvrt=None, qpar=None):
    AI = pyFAI.AzimuthalIntegrator()
    AI.setPyFAI(**AIdict)
    if not mask.shape == data.shape:
        msg.logMessage('No mask match. Mask will be ignored.', msg.WARNING)
        mask = np.ones_like(data)
        msg.logMessage(('emptymask:', mask.shape), msg.DEBUG)
    if cut is not None:
        msg.logMessage(('cut:', cut.shape), msg.DEBUG)
        mask &= cut.astype(bool)
    center = np.where(np.abs(qvrt) == np.abs(qvrt).min())
    qx = -qvrt[center[1][0]] / 10.0
    maskeddata = np.ma.masked_array(data, mask=1 - mask)
    xprofile = np.ma.average(maskeddata, axis=0)
    return (
     qx.tolist(), xprofile.tolist(), color, requestkey)