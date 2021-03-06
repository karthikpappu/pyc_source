# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ffnet/_mpprop.py
# Compiled at: 2018-10-28 11:56:52
"""
Parallel training functions
"""
from fortran import _ffnet as netprop
nets = {}
inputs = {}
targets = {}

def initializer(key, net, input, target):
    """
    This initializer will be used on WINDOWS ONLY (because of no fork())

    key, net, input, target have to be serialized to reach this place
    this means that:
    a) initialization process might be time consuming
    b) each process receives its own copy of data so the whole training might be memory hungry.
    These drawbacks can only be ommited if net, input, target
    will live in shared memory
    """
    nets[key] = net
    inputs[key] = input
    targets[key] = target


def splitdata(N, nproc):
    """
    Creates splitters for dataset of length *N* for *nproc* processes.

    Splits to *nproc* equal data chunks.
    """
    n = N // nproc
    i = (nproc - N % nproc) * n
    idx = range(n, i, n) + range(i, N, n + 1)
    idx1 = [0] + idx
    idx2 = idx + [N]
    return zip(idx1, idx2)


func = netprop.func

def procfunc(x, splitter, key):
    """
    Per process function netprop.func function
    """
    start, end = splitter
    net = nets[key]
    inp = inputs[key][start:end]
    trg = targets[key][start:end]
    return func(x, net.conec, net.bconecno, net.units, net.inno, net.outno, inp, trg)


def mpfunc(x, pool, splitters, key):
    """
    Execute netprop.func in parallel on multiprocessing *pool*
    """
    res = []
    for splitter in splitters:
        res += [pool.apply_async(procfunc, (x, splitter, key))]

    return sum([ r.get() for r in res ])


grad = netprop.grad

def procgrad(x, splitter, key):
    """
    Per process function netprop.grad function
    """
    start, end = splitter
    net = nets[key]
    inp = inputs[key][start:end]
    trg = targets[key][start:end]
    return grad(x, net.conec, net.bconecno, net.units, net.inno, net.outno, inp, trg)


def mpgrad(x, pool, splitters, key):
    """
    Execute netprop.grad in parallel on multiprocessing *pool*
    """
    res = []
    for splitter in splitters:
        res += [pool.apply_async(procgrad, (x, splitter, key))]

    return sum([ r.get() for r in res ])


func2 = netprop.func2

def procfunc2(x, splitter, key):
    """
    Per process function netprop.func2 function
    """
    start, end = splitter
    net = nets[key]
    inp = inputs[key][start:end]
    trg = targets[key][start:end]
    return func2(x, net.conec, net.bconecno, net.units, net.inno, net.outno, inp, trg)


def mpfunc2(x, pool, splitters, key):
    """
    Execute netprop.func2 in parallel on multiprocessing *pool*
    """
    res = []
    for splitter in splitters:
        res += [pool.apply_async(procfunc2, (x, splitter, key))]

    return map(sum, zip(*[ r.get() for r in res ]))