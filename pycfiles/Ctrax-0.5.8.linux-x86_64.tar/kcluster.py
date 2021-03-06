# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/Ctrax/kcluster.py
# Compiled at: 2013-09-24 00:46:30
import numpy as num, scipy.cluster.vq as vq, scipy.linalg.decomp as decomp
from version import DEBUG

def clusterdistfun(x, c):
    n = x.shape[0]
    nclusts = c.shape[0]
    D = num.zeros((nclusts, n))
    for i in range(nclusts):
        D[i, :] = num.sum((x - c[i, :]) ** 2, axis=1)

    return D


def furthestfirst(x, k, mu0=None, start='mean'):
    n = x.shape[0]
    d = x.shape[1]
    mu = num.zeros((k, d))
    if num.any(mu0) == False:
        if start == 'mean':
            mu[0, :] = num.mean(x, axis=0)
        else:
            i = num.floor(num.random.uniform(0, 1, 1) * n)[0]
            mu[0, :] = x[i, :]
    else:
        mu[0, :] = mu0
    Dall = num.zeros((k, n))
    Dall[:] = num.inf
    for i in range(1, k):
        Dall[i - 1, :] = num.sum((x - mu[i - 1, :]) ** 2, axis=1)
        D = num.amin(Dall, axis=0)
        j = num.argmax(D)
        mu[i, :] = x[j, :]

    Dall[k - 1, :] = num.sum((x - mu[k - 1, :]) ** 2, axis=1)
    idx = num.argmin(Dall, axis=0)
    return (
     mu, idx)


def gmminit(x, k, weights=None, kmeansiter=20, kmeansthresh=0.001):
    n = x.shape[0]
    d = x.shape[1]
    mu, idx = furthestfirst(x, k, start='random')
    mu, dmin = vq.kmeans(x, mu, kmeansiter, kmeansthresh)
    D = clusterdistfun(x, mu)
    idx = num.argmin(D, axis=0)
    S = num.zeros((d, d, k))
    priors = num.zeros(k)
    if num.any(weights) == False:
        for i in range(k):
            nidx = num.sum(num.double(idx == i))
            priors[i] = nidx
            mu[i, :] = num.mean(x[idx == i, :], axis=0)
            diffs = x[idx == i, :] - mu[i, :].reshape(1, d)
            S[:, :, i] = num.dot(num.transpose(diffs), diffs) / priors[i]

    else:
        weights = weights.reshape(n, 1)
        for i in range(k):
            nidx = num.sum(num.double(idx == i))
            priors[i] = num.sum(weights[(idx == i)])
            try:
                mu[i, :] = num.sum(weights[(idx == i)] * x[idx == i, :], axis=0) / priors[i]
            except IndexError:
                print 'i %d priors[i] %f' % (i, priors[i])
                print idx
                raise

            diffs = x[idx == i, :] - mu[i, :].reshape(1, d)
            diffs *= num.sqrt(weights[(idx == i)])
            S[:, :, i] = num.dot(num.transpose(diffs), diffs) / priors[i]

    priors = priors / num.sum(priors)
    return (
     mu, S, priors)


def gmm(x, k, weights=None, nreplicates=10, kmeansiter=20, kmeansthresh=0.001, emiters=100, emthresh=0.001, mincov=0.01):
    n = x.shape[0]
    d = x.shape[1]
    minerr = num.inf
    for rep in range(nreplicates):
        mu, S, priors = gmminit(x, k, weights, kmeansiter, kmeansthresh)
        mu, S, priors, gamma, err = gmmem(x, mu, S, priors, weights, emiters, emthresh, mincov)
        if err < minerr:
            mubest = mu
            Sbest = S
            priorsbest = priors
            minerr = err
            gammabest = gamma

    return (
     mubest, Sbest, priorsbest, gammabest, minerr)


def gmmmemberships(mu, S, priors, x, weights=1, initcovars=None):
    if initcovars is None:
        initcovars = S.copy()
    n = x.shape[0]
    d = x.shape[1]
    k = mu.shape[0]
    gamma = num.zeros((n, k))
    normal = (2.0 * num.pi) ** (num.double(d) / 2.0)
    for j in range(k):
        diffs = x - mu[j, :]
        try:
            c = decomp.cholesky(S[:, :, j])
        except num.linalg.linalg.LinAlgError:
            if DEBUG:
                print 'S[:,:,%d] = ' % j + str(S[:, :, j]) + ' is singular'
            if DEBUG:
                print 'Reverting to initcovars[:,:,%d] = ' % j + str(initcovars[:, :, j])
            S[:, :, j] = initcovars[:, :, j]
            c = decomp.cholesky(S[:, :, j])

        temp = num.transpose(num.linalg.solve(num.transpose(c), num.transpose(diffs)))
        gamma[:, j] = num.exp(-0.5 * num.sum(temp ** 2, axis=1)) / (normal * num.prod(num.diag(c)))

    gamma *= priors
    e = -num.sum(num.log(num.sum(gamma, axis=1)) * weights)
    s = num.sum(gamma, axis=1)
    s[s == 0] = 1
    gamma /= s.reshape(n, 1)
    return (
     gamma, e)


def gmmupdate(mu, S, priors, gamma, x, weights=1, mincov=0.01, initcovars=None):
    if num.any(initcovars) == False:
        initcovars = S
    n = gamma.shape[0]
    k = gamma.shape[1]
    d = x.shape[1]
    gamma *= weights.reshape(n, 1)
    priors[:] = num.sum(gamma, axis=0)
    Z = priors.copy()
    sumpriors = num.sum(priors)
    if sumpriors > 0:
        priors /= sumpriors
        issmall = priors < 0.01
        issmall = issmall.any()
    else:
        if DEBUG:
            print 'All priors are too small, reinitializing'
        issmall = num.array((1, )).any()
    if issmall:
        fixsmallpriors(x, mu, S, priors, initcovars, gamma)
        priors[:] = num.sum(gamma, axis=0)
        Z = priors.copy()
        priors /= num.sum(priors)
        if DEBUG:
            print 'after fixsmallpriors, priors is ' + str(priors)
    if issmall:
        if DEBUG:
            print 'outside fixsmallpriors'
            print 'reset mu = ' + str(mu)
            for i in range(k):
                print 'reset S[:,:,%d] = ' % i + str(S[:, :, i])

            print 'reset priors = ' + str(priors)
    for i in range(k):
        mu[i, :] = num.sum(gamma[:, i].reshape(n, 1) * x, axis=0) / Z[i]
        if DEBUG:
            if issmall:
                print 'updated mu[%d,:] to ' % i + str(mu[i, :])
        diffs = x - mu[i, :]
        diffs *= num.sqrt(gamma[:, i].reshape(n, 1))
        S[:, :, i] = num.dot(num.transpose(diffs), diffs) / Z[i]
        if DEBUG:
            if issmall:
                print 'updated S[:,:,%d] to [%.4f,%.4f;%.4f,%.4f]' % (i, S[(0, 0, i)], S[(0, 1, i)], S[(1, 0, i)], S[(1, 1, i)])
        if mincov > 0:
            D, V = num.linalg.eig(S[:, :, i])
            if num.min(D) < mincov:
                S[:, :, i] = initcovars[:, :, i]
                if DEBUG:
                    print 'mineigval = %.4f' % num.min(D)
                    print 'reinitializing covariance'
                    print 'D = '
                    print D
                    print 'initcovars[:,:,%d] = [%.4f,%.4f;%.4f,%.4f]' % (i, initcovars[(0, 0, i)], initcovars[(0, 1, i)], initcovars[(1, 0, i)], initcovars[(1, 1, i)])


def gmmem(x, mu0, S0, priors0, weights=None, niters=100, thresh=0.001, mincov=0.01):
    mu = mu0.copy()
    S = S0.copy()
    priors = priors0.copy()
    e = num.inf
    if mincov > 0:
        for i in range(S.shape[2]):
            D, U = num.linalg.eig(S[:, :, i])
            D[D < mincov] = mincov
            S[:, :, i] = num.dot(num.dot(U, num.diag(D)), U.transpose())

    initcovars = S.copy()
    for iter in range(niters):
        gamma, newe = gmmmemberships(mu, S, priors, x, weights, initcovars)
        gmmupdate(mu, S, priors, gamma, x, weights, mincov, initcovars)
        if newe >= e - thresh:
            break
        e = newe

    gamma, e = gmmmemberships(mu, S, priors, x, weights, initcovars)
    return (
     mu, S, priors, gamma, e)


def fixsmallpriors(x, mu, S, priors, initcovars, gamma):
    MINPRIOR = 0.01
    issmall = priors < 0.01
    if not issmall.any():
        return
    n = x.shape[0]
    d = x.shape[1]
    k = mu.shape[0]
    smalli, = num.where(issmall)
    for i in smalli:
        if DEBUG:
            print 'fixing cluster %d with small prior = %f: ' % (i, priors[i])
        p = num.sum(gamma * priors, axis=1)
        j = p.argmin()
        if DEBUG:
            print 'lowest density sample: x[%d] = ' % j + str(x[j, :])
        mu[i, :] = x[j, :]
        S[:, :, i] = initcovars[:, :, i]
        priors *= (1.0 - MINPRIOR) / (1.0 - priors[i])
        priors[i] = MINPRIOR
        if DEBUG:
            print 'reset cluster %d to: ' % i
            print 'mu = ' + str(mu[i, :])
            print 'S = '
            print S[:, :, i]
            print 'S.shape: ' + str(S[:, :, i].shape)
            print 'priors = ' + str(priors)
        gamma[:], newe = gmmmemberships(mu, S, priors, x, 1, initcovars)