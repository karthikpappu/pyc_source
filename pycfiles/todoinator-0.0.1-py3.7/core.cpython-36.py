# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\tikon\Clima\PyKrige\core.py
# Compiled at: 2016-01-05 13:51:40
# Size of source mod 2**32: 17429 bytes
__doc__ = 'Code by Benjamin S. Murphy\nbscott.murphy@gmail.com\n\nDependencies:\n    numpy\n    scipy (scipy.optimize.minimize())\n\nFunctions:\n    adjust_for_anisotropy(x, y, xcenter, ycenter, scaling, angle):\n        Returns X and Y arrays of adjusted data coordinates. Angle is CCW.\n    adjust_for_anisotropy_3d(x, y, z, xcenter, ycenter, zcenter, scaling_y,\n                             scaling_z, angle_x, angle_y, angle_z):\n        Returns X, Y, Z arrays of adjusted data coordinates. Angles are CCW about\n        specified axes. Scaling is applied in rotated coordinate system.\n    initialize_variogram_model(x, y, z, variogram_model, variogram_model_parameters,\n                               variogram_function, nlags):\n        Returns lags, semivariance, and variogram model parameters as a list.\n    initialize_variogram_model_3d(x, y, z, values, variogram_model,\n                                  variogram_model_parameters, variogram_function, nlags):\n        Returns lags, semivariance, and variogram model parameters as a list.\n    variogram_function_error(params, x, y, variogram_function):\n        Called by calculate_variogram_model.\n    calculate_variogram_model(lags, semivariance, variogram_model, variogram_function):\n        Returns variogram model parameters that minimize the RMSE between the specified\n        variogram function and the actual calculated variogram points.\n    krige(x, y, z, coords, variogram_function, variogram_model_parameters):\n        Function that solves the ordinary kriging system for a single specified point.\n        Returns the Z value and sigma squared for the specified coordinates.\n    krige_3d(x, y, z, vals, coords, variogram_function, variogram_model_parameters):\n        Function that solves the ordinary kriging system for a single specified point.\n        Returns the interpolated value and sigma squared for the specified coordinates.\n    find_statistics(x, y, z, variogram_funtion, variogram_model_parameters):\n        Returns the delta, sigma, and epsilon values for the variogram fit.\n    calcQ1(epsilon):\n        Returns the Q1 statistic for the variogram fit (see Kitanidis).\n    calcQ2(epsilon):\n        Returns the Q2 statistic for the variogram fit (see Kitanidis).\n    calc_cR(Q2, sigma):\n        Returns the cR statistic for the variogram fit (see Kitanidis).\n\nReferences:\n    P.K. Kitanidis, Introduction to Geostatistcs: Applications in Hydrogeology,\n    (Cambridge University Press, 1997) 272 p.\n\nCopyright (c) 2015 Benjamin S. Murphy\n'
import numpy as np
from scipy.optimize import minimize

def adjust_for_anisotropy(x, y, xcenter, ycenter, scaling, angle):
    """Adjusts data coordinates to take into account anisotropy.
    Can also be used to take into account data scaling."""
    x -= xcenter
    y -= ycenter
    xshape = x.shape
    yshape = y.shape
    x = x.flatten()
    y = y.flatten()
    coords = np.vstack((x, y))
    stretch = np.array([[1, 0], [0, scaling]])
    rotate = np.array([[np.cos(-angle * np.pi / 180.0), -np.sin(-angle * np.pi / 180.0)],
     [
      np.sin(-angle * np.pi / 180.0), np.cos(-angle * np.pi / 180.0)]])
    rotated_coords = np.dot(stretch, np.dot(rotate, coords))
    x = rotated_coords[0, :].reshape(xshape)
    y = rotated_coords[1, :].reshape(yshape)
    x += xcenter
    y += ycenter
    return (
     x, y)


def adjust_for_anisotropy_3d(x, y, z, xcenter, ycenter, zcenter, scaling_y, scaling_z, angle_x, angle_y, angle_z):
    """Adjusts data coordinates to take into account anisotropy.
    Can also be used to take into account data scaling."""
    x -= xcenter
    y -= ycenter
    z -= zcenter
    xshape = x.shape
    yshape = y.shape
    zshape = z.shape
    x = x.flatten()
    y = y.flatten()
    z = z.flatten()
    coords = np.vstack((x, y, z))
    stretch = np.array([[1.0, 0.0, 0.0], [0.0, scaling_y, 0.0], [0.0, 0.0, scaling_z]])
    rotate_x = np.array([[1.0, 0.0, 0.0],
     [
      0.0, np.cos(-angle_x * np.pi / 180.0), -np.sin(-angle_x * np.pi / 180.0)],
     [
      0.0, np.sin(-angle_x * np.pi / 180.0), np.cos(-angle_x * np.pi / 180.0)]])
    rotate_y = np.array([[np.cos(-angle_y * np.pi / 180.0), 0.0, np.sin(-angle_y * np.pi / 180.0)],
     [
      0.0, 1.0, 0.0],
     [
      -np.sin(-angle_y * np.pi / 180.0), 0.0, np.cos(-angle_y * np.pi / 180.0)]])
    rotate_z = np.array([[np.cos(-angle_z * np.pi / 180.0), -np.sin(-angle_z * np.pi / 180.0), 0.0],
     [
      np.sin(-angle_z * np.pi / 180.0), np.cos(-angle_z * np.pi / 180.0), 0.0],
     [
      0.0, 0.0, 1.0]])
    rot_tot = np.dot(rotate_z, np.dot(rotate_y, rotate_x))
    rotated_coords = np.dot(stretch, np.dot(rot_tot, coords))
    x = rotated_coords[0, :].reshape(xshape)
    y = rotated_coords[1, :].reshape(yshape)
    z = rotated_coords[2, :].reshape(zshape)
    x += xcenter
    y += ycenter
    z += zcenter
    return (
     x, y, z)


def initialize_variogram_model(x, y, z, variogram_model, variogram_model_parameters, variogram_function, nlags, weight):
    """Initializes the variogram model for kriging according
    to user specifications or to defaults"""
    x1, x2 = np.meshgrid(x, x)
    y1, y2 = np.meshgrid(y, y)
    z1, z2 = np.meshgrid(z, z)
    dx = x1 - x2
    dy = y1 - y2
    dz = z1 - z2
    d = np.sqrt(dx ** 2 + dy ** 2)
    g = 0.5 * dz ** 2
    indices = np.indices(d.shape)
    d = d[(indices[0, :, :] > indices[1, :, :])]
    g = g[(indices[0, :, :] > indices[1, :, :])]
    dmax = np.amax(d)
    dmin = np.amin(d)
    dd = (dmax - dmin) / nlags
    bins = [dmin + n * dd for n in range(nlags)]
    dmax += 0.001
    bins.append(dmax)
    lags = np.zeros(nlags)
    semivariance = np.zeros(nlags)
    for n in range(nlags):
        if d[((d >= bins[n]) & (d < bins[(n + 1)]))].size > 0:
            lags[n] = np.mean(d[((d >= bins[n]) & (d < bins[(n + 1)]))])
            semivariance[n] = np.mean(g[((d >= bins[n]) & (d < bins[(n + 1)]))])
        else:
            lags[n] = np.nan
            semivariance[n] = np.nan

    lags = lags[(~np.isnan(semivariance))]
    semivariance = semivariance[(~np.isnan(semivariance))]
    if variogram_model_parameters is not None:
        if variogram_model == 'linear':
            if len(variogram_model_parameters) != 2:
                raise ValueError('Exactly two parameters required for linear variogram model')
            if (variogram_model == 'power' or variogram_model == 'spherical' or variogram_model == 'exponential' or variogram_model == 'gaussian') and len(variogram_model_parameters) != 3:
                raise ValueError('Exactly three parameters required for %s variogram model' % variogram_model)
    else:
        if variogram_model == 'custom':
            raise ValueError('Variogram parameters must be specified when implementing custom variogram model.')
        else:
            variogram_model_parameters = calculate_variogram_model(lags, semivariance, variogram_model, variogram_function, weight)
    return (lags, semivariance, variogram_model_parameters)


def initialize_variogram_model_3d(x, y, z, values, variogram_model, variogram_model_parameters, variogram_function, nlags, weight):
    """Initializes the variogram model for kriging according
    to user specifications or to defaults"""
    x1, x2 = np.meshgrid(x, x)
    y1, y2 = np.meshgrid(y, y)
    z1, z2 = np.meshgrid(z, z)
    val1, val2 = np.meshgrid(values, values)
    d = np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)
    g = 0.5 * (val1 - val2) ** 2
    indices = np.indices(d.shape)
    d = d[(indices[0, :, :] > indices[1, :, :])]
    g = g[(indices[0, :, :] > indices[1, :, :])]
    dmax = np.amax(d)
    dmin = np.amin(d)
    dd = (dmax - dmin) / nlags
    bins = [dmin + n * dd for n in range(nlags)]
    dmax += 0.001
    bins.append(dmax)
    lags = np.zeros(nlags)
    semivariance = np.zeros(nlags)
    for n in range(nlags):
        if d[((d >= bins[n]) & (d < bins[(n + 1)]))].size > 0:
            lags[n] = np.mean(d[((d >= bins[n]) & (d < bins[(n + 1)]))])
            semivariance[n] = np.mean(g[((d >= bins[n]) & (d < bins[(n + 1)]))])
        else:
            lags[n] = np.nan
            semivariance[n] = np.nan

    lags = lags[(~np.isnan(semivariance))]
    semivariance = semivariance[(~np.isnan(semivariance))]
    if variogram_model_parameters is not None:
        if variogram_model == 'linear':
            if len(variogram_model_parameters) != 2:
                raise ValueError('Exactly two parameters required for linear variogram model')
            if (variogram_model == 'power' or variogram_model == 'spherical' or variogram_model == 'exponential' or variogram_model == 'gaussian') and len(variogram_model_parameters) != 3:
                raise ValueError('Exactly three parameters required for %s variogram model' % variogram_model)
    else:
        if variogram_model == 'custom':
            raise ValueError('Variogram parameters must be specified when implementing custom variogram model.')
        else:
            variogram_model_parameters = calculate_variogram_model(lags, semivariance, variogram_model, variogram_function, weight)
    return (lags, semivariance, variogram_model_parameters)


def variogram_function_error(params, x, y, variogram_function, weight):
    """Function used to in fitting of variogram model.
    Returns RMSE between calculated fit and actual data."""
    diff = variogram_function(params, x) - y
    if weight:
        weights = np.arange(x.size, 0.0, -1.0)
        weights /= np.sum(weights)
        rmse = np.sqrt(np.average((diff ** 2), weights=weights))
    else:
        rmse = np.sqrt(np.mean(diff ** 2))
    return rmse


def calculate_variogram_model(lags, semivariance, variogram_model, variogram_function, weight):
    """Function that fits a variogram model when parameters are not specified."""
    if variogram_model == 'linear':
        x0 = [
         (np.amax(semivariance) - np.amin(semivariance)) / (np.amax(lags) - np.amin(lags)),
         np.amin(semivariance)]
        bnds = ((0.0, 1000000000.0), (0.0, np.amax(semivariance)))
    else:
        if variogram_model == 'power':
            x0 = [
             (np.amax(semivariance) - np.amin(semivariance)) / (np.amax(lags) - np.amin(lags)),
             1.1, np.amin(semivariance)]
            bnds = ((0.0, 1000000000.0), (0.01, 1.99), (0.0, np.amax(semivariance)))
        else:
            x0 = [
             np.amax(semivariance), 0.5 * np.amax(lags), np.amin(semivariance)]
            bnds = ((0.0, 10 * np.amax(semivariance)), (0.0, np.amax(lags)), (0.0, np.amax(semivariance)))
    res = minimize(variogram_function_error, x0, args=(lags, semivariance, variogram_function, weight), method='SLSQP',
      bounds=bnds)
    return res.x


def krige(x, y, z, coords, variogram_function, variogram_model_parameters):
    """Sets up and solves the kriging matrix for the given coordinate pair.
        This function is now only used for the statistics calculations."""
    zero_index = None
    zero_value = False
    x1, x2 = np.meshgrid(x, x)
    y1, y2 = np.meshgrid(y, y)
    d = np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    bd = np.sqrt((x - coords[0]) ** 2 + (y - coords[1]) ** 2)
    if np.any(np.absolute(bd) <= 1e-10):
        zero_value = True
        zero_index = np.where(bd <= 1e-10)[0][0]
    n = x.shape[0]
    a = np.zeros((n + 1, n + 1))
    a[:n, :n] = -variogram_function(variogram_model_parameters, d)
    np.fill_diagonal(a, 0.0)
    a[n, :] = 1.0
    a[:, n] = 1.0
    a[(n, n)] = 0.0
    b = np.zeros((n + 1, 1))
    b[:n, 0] = -variogram_function(variogram_model_parameters, bd)
    if zero_value:
        b[(zero_index, 0)] = 0.0
    b[(n, 0)] = 1.0
    x_ = np.linalg.solve(a, b)
    zinterp = np.sum(x_[:n, 0] * z)
    sigmasq = np.sum(x_[:, 0] * -b[:, 0])
    return (
     zinterp, sigmasq)


def krige_3d(x, y, z, vals, coords, variogram_function, variogram_model_parameters):
    """Sets up and solves the kriging matrix for the given coordinate pair.
        This function is now only used for the statistics calculations."""
    zero_index = None
    zero_value = False
    x1, x2 = np.meshgrid(x, x)
    y1, y2 = np.meshgrid(y, y)
    z1, z2 = np.meshgrid(z, z)
    d = np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)
    bd = np.sqrt((x - coords[0]) ** 2 + (y - coords[1]) ** 2 + (z - coords[2]) ** 2)
    if np.any(np.absolute(bd) <= 1e-10):
        zero_value = True
        zero_index = np.where(bd <= 1e-10)[0][0]
    n = x.shape[0]
    a = np.zeros((n + 1, n + 1))
    a[:n, :n] = -variogram_function(variogram_model_parameters, d)
    np.fill_diagonal(a, 0.0)
    a[n, :] = 1.0
    a[:, n] = 1.0
    a[(n, n)] = 0.0
    b = np.zeros((n + 1, 1))
    b[:n, 0] = -variogram_function(variogram_model_parameters, bd)
    if zero_value:
        b[(zero_index, 0)] = 0.0
    b[(n, 0)] = 1.0
    x_ = np.linalg.solve(a, b)
    zinterp = np.sum(x_[:n, 0] * vals)
    sigmasq = np.sum(x_[:, 0] * -b[:, 0])
    return (
     zinterp, sigmasq)


def find_statistics(x, y, z, variogram_function, variogram_model_parameters):
    """Calculates variogram fit statistics."""
    delta = np.zeros(z.shape)
    sigma = np.zeros(z.shape)
    for n in range(z.shape[0]):
        if n == 0:
            delta[n] = 0.0
            sigma[n] = 0.0
        else:
            z_, ss_ = krige(x[:n], y[:n], z[:n], (x[n], y[n]), variogram_function, variogram_model_parameters)
            d = z[n] - z_
            delta[n] = d
            sigma[n] = np.sqrt(ss_)

    delta = delta[1:]
    sigma = sigma[1:]
    epsilon = delta / sigma
    return (
     delta, sigma, epsilon)


def find_statistics_3d(x, y, z, vals, variogram_function, variogram_model_parameters):
    """Calculates variogram fit statistics for 3D problems."""
    delta = np.zeros(vals.shape)
    sigma = np.zeros(vals.shape)
    for n in range(z.shape[0]):
        if n == 0:
            delta[n] = 0.0
            sigma[n] = 0.0
        else:
            z_, ss_ = krige_3d(x[:n], y[:n], z[:n], vals[:n], (x[n], y[n], z[n]), variogram_function, variogram_model_parameters)
            d = z[n] - z_
            delta[n] = d
            sigma[n] = np.sqrt(ss_)

    delta = delta[1:]
    sigma = sigma[1:]
    epsilon = delta / sigma
    return (
     delta, sigma, epsilon)


def calcQ1(epsilon):
    return abs(np.sum(epsilon) / (epsilon.shape[0] - 1))


def calcQ2(epsilon):
    return np.sum(epsilon ** 2) / (epsilon.shape[0] - 1)


def calc_cR(Q2, sigma):
    return Q2 * np.exp(np.sum(np.log(sigma ** 2)) / sigma.shape[0])