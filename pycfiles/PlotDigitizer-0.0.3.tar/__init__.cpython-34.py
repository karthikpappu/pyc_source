# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.4/dist-packages/plotdf/__init__.py
# Compiled at: 2015-09-12 02:33:38
# Size of source mod 2**32: 3726 bytes
__doc__ = '\nPlot phase portraits of 2D differential equations.\n\nExample:\n  from math import sin\n  from plotdf import plotdf\n  \n  def f(x,g=1,l=1,m=1,b=1):\n    return np.array([x[1],-g*sin(x[0])/l-b*x[1]/m/l])\n\n  plotdf(f, # Function giving the rhs of the diff. eq. system\n         np.array([-10,2]), # [xmin,xmax]\n         np.array([-14,14]),# [ymin,ymax]\n         [(1.05,-9),(0,5)], # list of initial values for trajectories (optional)\n         # Additional parameters for `f` (optional)\n         parameters={"g":9.8,"l":0.5,"m":0.3,"b":0.05})\n'
import numpy as np, scipy.integrate as scint, matplotlib.pyplot as plt

def plotdf(f, xbound, ybound, inits=None, tmax=10, nsteps=100, tdir='both', gridsteps=10, parameters=dict(), axes=None):
    """
  Plot a direction field and optional trajectories of a planar differential
  equation system.

  Arguments
  -----

  f: A function of of the form f(x) where 'x' is a 2-element numpy
     array denoting the current state, 't' is the current time and
     we expect 'f' to return the rhs of the differential equation system.

  xbound: a two-element sequence giving the minimum and maximum values of 
     'x' to plot.

  ybound: a two-element sequence giving the minimum and maximum values of 
     'y' to plots.

  inits: if not None, gives the set of initial values to plot trajectories from.
  
  tmax: the maximum value of 't' for which to calculate trajectories

  tdir = "forward", "backward" or "both", time direction in which to 
         plot trajectories

  nsteps: number of steps in trajectories

  gridsteps: number of steps in the x-y grid

  parameters: additional keyword arguments for 'f'

  axes: the matplot axes in which to draw the plot. If not provided
        use the current axes.

  Return Value
  ------
  A list the first element of which is the matplotlib Quiver object
  representing the arrows of the direction field and the rest are the 
  Lines2D objects representing the trajectories.
  """
    if tdir not in ('forward', 'backward', 'both'):
        raise ValueError("'tdir' must be 'forward', 'backward' or 'both'")
    if axes is None:
        axes = plt.gca()
    x = np.linspace(xbound[0], xbound[1], gridsteps)
    y = np.linspace(ybound[0], ybound[1], gridsteps)
    xx, yy = np.meshgrid(x, y)
    uu = np.empty_like(xx)
    vv = np.empty_like(yy)
    for i in range(gridsteps):
        for j in range(gridsteps):
            res = f(np.array([xx[(i, j)], yy[(i, j)]]), **parameters)
            uu[(i, j)] = res[0]
            vv[(i, j)] = res[1]

    artists = []
    artists.append(axes.quiver(xx, yy, uu, vv, color='darkred', width=0.002))
    if inits is not None:

        def g(x, t):
            return f(x, **parameters)

        def bg(x, t):
            return -f(x, **parameters)

        t = np.linspace(0, tmax, nsteps)
        for y0 in inits:
            traj_f = np.empty((0, 2))
            traj_b = np.empty((0, 2))
            if tdir in ('forward', 'both'):
                traj_f = scint.odeint(g, y0, t)
            if tdir in ('backward', 'both'):
                traj_b = scint.odeint(bg, y0, t)
            traj = np.vstack((np.flipud(traj_b), traj_f))
            artists.extend(axes.plot(traj[:, 0], traj[:, 1], linewidth=1.2))

    plt.xlim(xbound)
    plt.ylim(ybound)
    return artists