# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: heatrapy/solvers/explicit_k.py
# Compiled at: 2018-04-20 07:46:00
from __future__ import unicode_literals
import numpy as np, copy

def explicit_k(obj):
    """explicit_k solver.

    Used to compute one time step of systems with x-dependent thermal
    contuctivity.

    """
    x = copy.copy(obj.temperature)
    for i in range(1, obj.num_points - 1):
        eta = obj.dt / (2.0 * obj.rho[i] * obj.Cp[i] * obj.dx * obj.dx)
        beta = obj.dt / (obj.rho[i] * obj.Cp[i])
        Tnew = (1 + beta * obj.Q[i]) * obj.temperature[i][0] + eta * ((obj.k[(i + 1)] + obj.k[i]) * obj.temperature[(i + 1)][0] - (obj.k[(i - 1)] + obj.k[(i + 1)] + 2 * obj.k[i]) * obj.temperature[i][0] + (obj.k[(i - 1)] + obj.k[i]) * obj.temperature[(i - 1)][0]) + beta * (obj.Q0[i] - obj.Q[i] * obj.amb_temperature)
        x[i][1] = Tnew

    if obj.boundaries[0] == 0:
        x[0][1] = obj.temperature[1][1]
    else:
        x[0][1] = obj.boundaries[0]
    if obj.boundaries[1] == 0:
        x[(obj.num_points - 1)][1] = obj.temperature[(obj.num_points - 2)][1]
    else:
        x[(obj.num_points - 1)][1] = obj.boundaries[1]
    for i in range(0, obj.num_points):
        x[i][0] = x[i][1]

    return x