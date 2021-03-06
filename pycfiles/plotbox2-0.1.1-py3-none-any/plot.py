# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.5-x86_64/egg/plotbox/plot.py
# Compiled at: 2015-12-03 14:37:24
import numpy as np, pandas as pd, matplotlib.pyplot as plt, seaborn as sns, plotly, plotly.plotly as py, plotly.graph_objs as go
from .utils import df_to_arrays, arrays_to_df
sns.set_style('whitegrid')

def dist_plot(distObj, saveAs=None, title='Probability Dashboard', logscale=False):
    """
    Generates a plot object which is either displayed or saved.
    The plot includes 4 subplots:

    * a probability plot generated using scipy.stats "probplot",
      comparing the theoretical distribution and its data X

    * a scatter plot of the data sample

    * the CDF of the distribution

    * the PDF of the distribution

    """
    Xsub = distObj.Xsub
    x = np.linspace(np.minimum(math.floor(min(distObj.rv.rvs(size=200))), min(Xsub)), np.maximum(math.ceil(max(distObj.rv.rvs(size=200))), max(Xsub)))
    fig = plt.figure(figsize=(16, 9))
    plt.suptitle(title, fontsize=16, fontweight='bold')
    if 'weib' in distObj.dist_name:
        ax1 = probplot(distObj, logscale=logscale, subplot=221)
    else:
        ax1 = plt.subplot(221)
        scipy.stats.probplot(x=Xsub, sparams=distObj.rv.args, dist=distObj.rv.dist.name, fit=False, plot=plt)
        plt.title(distObj.rv.dist.name + ' Pr')
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        txtStr = ''
        for k, v in distObj.parameter_dict.iteritems():
            txtStr = k + ' = ' + str(v) + '\n' + txtStr

        textstr = txtStr[:-2]
        ax1.text(0.05, 0.95, textstr, transform=ax1.transAxes, fontsize=14, verticalalignment='top', bbox=props)
    ax2 = plt.subplot(222)
    ax2.plot(x, distObj.rv.cdf(x))
    plt.title(distObj.dist_name + ' CDF')
    ax2.hist(Xsub, bins=50, normed=1, alpha=0.3, cumulative=True)
    ax4 = plt.subplot(224)
    ax4.plot(x, distObj.rv.pdf(x))
    plt.title(distObj.dist_name + ' PDF')
    ax4.hist(Xsub, bins=50, normed=1, alpha=0.3)
    ax3 = plt.subplot(223)
    ax3.scatter(range(len(Xsub)), Xsub, alpha=0.3)
    plt.title('Scatter Plot')
    if saveAs is None:
        plt.show()
    else:
        save_plot(fig, saveAs)
    return


def wblPlots(distList, title=None, labelList=None, saveAs=None, xlabel='Miles to Failure', min_x=None, max_x=None, ylim=(None, None), xlim=(None, None), use_sci=False, show=True):
    """Produces a weibull probability plot from a list of dist objects
    labelList is a list of strings the same size and order as distList that provides
    label information for each distribution
    """
    distList = relpy.utils.general.obj_to_list(distList)
    colors = [
     'c', 'r', 'g', 'b', 'm', 'y', 'k']
    shapes = ['o', '*', 's', 'x', 'D', '^', 'h', 'p', '+', '.']
    yScale = 1.0
    yt_F = np.array([0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.99]) * yScale
    yt_lnF = np.log(-np.log(1 - yt_F))
    fig = plt.figure(figsize=(16, 9))
    ax = plt.subplot(111)
    ax.set_xscale('log')
    plt.legend(numpoints=1)
    objCount = 0
    shapeCount = 0
    colorCount = 0
    if min_x is None:
        minXList = [ min(distObj.Xsub) for distObj in distList ]
        min_x = np.max([0.01, np.min(minXList)])
    if max_x is None:
        maxXList = [ max(distObj.Xsub) for distObj in distList ]
        max_x = relpy.utils.number.next_round_log(np.max(maxXList))
    x_ideal = np.linspace(min_x, max_x)
    for distObj in distList:
        Xsub = distObj.Xsub
        try:
            t = distObj.X
            f = distObj.Xbool
            if f is not None:
                f = np.array(f)
                f = f[(~np.isnan(t))]
            t = t[(~np.isnan(t))]
            t[t <= 0] = 0.1
            rank, y = relpy.model.statistics.rank.adjusted(t, f)
            nF = sum(f)
            nS = sum(f == False)
            nStr = 'F=' + str(nF) + ', S=' + str(nS)
        except:
            x = Xsub[Xsub.argsort()]
            rank, y = relpy.model.statistics.rank.adjusted(x)
            nStr = 'F=' + str(len(x))

        if distObj.dist_name == 'mixed_weibull':
            betaStr = '$\\beta$ = ' + str(distObj.theta[:, 1]).replace('[ ', '').replace(']', '').replace('  ', ' ').replace('  ', ' ').replace(' ', ', ')
            etaStr = '$\\eta$ = ' + str(distObj.theta[:, 2]).replace('[ ', '').replace(']', '').replace('  ', ' ').replace('  ', ' ').replace(' ', ', ')
        else:
            betaStr = '$\\beta$ = %5G' % distObj.theta[1]
            etaStr = '$\\eta$ = %.5G' % distObj.theta[3]
        if labelList is None:
            labelStr = betaStr + '\n' + etaStr + '\n' + nStr
        else:
            labelStr = str(labelList[objCount]) + '\n' + betaStr + '\n' + etaStr + '\n' + nStr
        x = Xsub[Xsub.argsort()]
        x[x <= 0] = 0.1
        F = distObj.rv.cdf(x_ideal)
        y_ideal = np.log(-np.log(1 - F))
        plt.plot(x, y, colors[colorCount] + shapes[shapeCount], label=labelStr, mec='k', mew=1, alpha=0.5)
        plt.plot(x_ideal, y_ideal, colors[colorCount] + '-')
        objCount += 1
        colorCount += 1
        if colorCount % 6 == 0:
            colorCount = 0
            shapeCount += 1

    if title is None:
        title = 'Weibull Probability Plot on Log Scale'
    plt.title(title, weight='bold')
    plt.xlabel(xlabel, weight='bold')
    plt.ylabel('Unreliability', weight='bold')
    plt.legend(numpoints=1, loc='lower right', bbox_to_anchor=(1.12, 0))
    plt.yticks(yt_lnF)
    ax.set_yticklabels(yt_F)
    ax.yaxis.grid(b=True, which='major')
    ax.xaxis.grid(b=True, which='both')
    if not use_sci:
        ax.xaxis.set_major_formatter(FormatStrFormatter('%.0f'))
    if ylim[0] is None:
        y_min = plt.ylim()[0]
    else:
        y_min = np.log(-np.log(1 - ylim[0]))
    if ylim[1] is None:
        y_max = plt.ylim()[1]
    else:
        y_max = np.log(-np.log(1 - ylim[1]))
    plt.ylim(y_min, y_max)
    if xlim[0] is None:
        x_min = plt.xlim()[0]
    else:
        x_min = 1 - xlim[0]
    if xlim[1] is None:
        x_max = plt.xlim()[1]
    else:
        x_max = xlim[1]
    plt.xlim(x_min, x_max)
    if saveAs is not None:
        save_plot(fig, saveAs, show=show)
    return


def scatter_plot(x, y, data=None, hue=None, title='Scatter Plot', xlabel='X-Values', ylabel='Y-Values', alpha=0.3, figsize=(
 14.25,
 9.0), saveAs=None, vlines=None, hlines=None, xlim=(None, None), ylim=(None, None), legend=True, model=None, plotly=False, show=True):
    """
    scatter_plot uses matplotlib.pyplot.scatter in a seaborn like functional paridigm

    Parameters
    ----------
    x, y : strings
            Column names in ``data``.
    data : DataFrame
            Long-form (tidy) dataframe with variables in columns and observations
            in rows.
    hue, col, row : strings, optional
            Variable names to facet on the hue, col, or row dimensions (see
            :class:`FacetGrid` docs for more information).
    title, xlabel, ylabel : strings
            labels of scatter plot.
    alpha : float
            opacity of scatter points.
    figsize : touple, (width, height)
    saveAs : optional
            filename to save figure as
    vlines : list
            list of x points to make vertical lines in the plot
    xlim : touple (xmin, xmax)
            horizontal boundries of the figure
    ylim : tuple (ymin, ymax)
            vertical boundries of the plot
    legend : boolean, optional
            Draw a legend for the data when using a `hue` variable.
    model : str, optional
            regression on given data.

    Examples
    --------

    .. plot:: pyplots/scatter_plot.py
                    :include-source:

    .. todo::

            Add arguments:

            * dropna : boolean, optional
            Drop missing values from the data before plotting.

            * add regression :
            f, popt, pcov = rp.statBox.regression_model(x,y, model)
            plt.plot(np.linspace(0,max(x)+100,50), f(np.linspace(0,max(x)+100,50), *popt), 'r-', label="Fitted Curve")

    Notes
    -----
    This function can be used in 2 different ways:

            * Using the arguments to generate titles, legends, etc... and then save/display the plot

            * Incorporate the plot in a script and overriding the plotting features this way:

                    >>> import matplotlib.pyplot as plt
                    >>>
                    >>> f = 1000
                    >>> hue = ['one' for i in range(50*f)] + ['two' for i in range(30*f)] + ['three' for i in range(20*f)]
                    >>> rp.plotBox.scatter_plot(x = np.random.randn(100*f), y = np.random.randn(100*f), hue = hue, vlines = 0, alpha= .1, hlines = 0)
                    >>> plt.title('My title')
                    >>> plt.xlabel('X label I want')
                    >>>
                    >>> # To change the figure size :
                    >>> fig = plt.gcf() # get the figure object
                    >>> fig.set_size_inches(5,10)
                    >>>
                    >>> plt.show()

    """
    if isinstance(x, basestring):
        if xlabel == 'X-Values':
            xlabel = x
        x = list(data[x])
    else:
        x = list(x)
    if isinstance(y, basestring):
        if ylabel == 'Y-Values':
            ylabel = y
        y = list(data[y])
    else:
        y = list(y)
    if hue is None:
        hue = [ 'Data' for i in range(len(x)) ]
    else:
        if isinstance(hue, basestring):
            hue = list(data[hue])
        else:
            hue = list(hue)
        hue_count_set = []
        for h in set(hue):
            hue_count_set.append((hue.count(h), h))

        hue_labels = [ t[1] for t in sorted(hue_count_set, reverse=True) ]
        if len(hue_labels) > 7:
            color_list = list(np.random.rand(len(hue_labels)))
        else:
            color_list = [
             'c', 'r', 'g', 'b', 'm', 'y', 'k']
        inc = 0
        fig = plt.figure(figsize=figsize)
        for h in hue_labels:
            idx = list(np.where(np.array(hue) == h)[0])
            x_idx = [ x[i] for i in idx ]
            y_idx = [ y[i] for i in idx ]
            plt.scatter(x_idx, y_idx, c=color_list[inc], alpha=alpha)
            if model:
                f, popt, pcov = relpy.model.optimization.regression.fit_curve(x=x_idx, y=y_idx, model=model)
                x_model = np.linspace(plt.xlim()[0], plt.xlim()[1], 1000)
                plt.plot(x_model, f(x_model, *popt), color_list[inc] + '-')
            inc += 1

    if legend:
        plt.legend(hue_labels)
    plt.title(title, size=16)
    plt.xlabel(xlabel, fontsize=14)
    plt.ylabel(ylabel, fontsize=14)
    if ylim[0] is None:
        y_min = plt.ylim()[0]
    else:
        y_min = ylim[0]
    if ylim[1] is None:
        y_max = plt.ylim()[1]
    else:
        y_max = ylim[1]
    plt.ylim(y_min, y_max)
    if xlim[0] is None:
        x_min = plt.xlim()[0]
    else:
        x_min = xlim[0]
    if xlim[1] is None:
        x_max = plt.xlim()[1]
    else:
        x_max = xlim[1]
    plt.xlim(x_min, x_max)
    if vlines is not None:
        plt.vlines(vlines, y_min, y_max)
    if hlines is not None:
        plt.hlines(hlines, x_min, x_max)
    if saveAs is not None:
        save_plot(fig, saveAs, show=show)
    return


def plotScatter(x, y, data=None, hue=None, bestfit=False, ci=95, alpha=1, size=20, xlab='x', ylab='y', axFontSize=9, title='', saveAs=None, figsize=(9.5, 6), snssize=5, label=None):
    """
    Robust scatterplot tool.
    Takes x and y as names of columns if given a df (you also get proper x/y labels),
    else takes x and y as arrays.
    Also takes hue as a way to color points as well as facet the bestfit, CI, alpha, size, x/y labels, and title.
    If given a date array (as x), draws simple scatterplot."""
    if data is None:
        x = list(x)
        y = list(y)
    if data is None and isinstance(x[0], (pd.tslib.Timestamp, dt.datetime, dt.date)):
        plt.subplots(figsize=figsize)
        plt.scatter(x, y, s=size, alpha=alpha, label=label)
        if xlab == 'x':
            plt.xlabel('Date', fontsize=axFontSize)
        else:
            plt.xlabel(xlab, fontsize=axFontSize)
    else:
        if snssize == 5 and figsize is not None:
            snssize = figsize[1]
            aspect = float(figsize[0]) / figsize[1]
        if data is None:
            if hue is not None:
                df = pd.DataFrame([x, y, hue]).T
                df.columns = ['x', 'y', 'hue']
                sns.lmplot('x', 'y', df, hue='hue', fit_reg=bestfit, ci=ci, scatter_kws={'s': size, 
                   'alpha': alpha}, size=snssize, aspect=aspect)
            else:
                df = pd.DataFrame([x, y]).T
                df.columns = ['x', 'y']
                sns.lmplot('x', 'y', df, fit_reg=bestfit, ci=ci, scatter_kws={'s': size, 
                   'alpha': alpha}, size=snssize, aspect=aspect)
        else:
            sns.lmplot(x, y, data, hue=hue, fit_reg=bestfit, ci=ci, scatter_kws={'s': size, 
               'alpha': alpha}, size=snssize, aspect=aspect)
        if xlab != 'x':
            plt.xlabel(xlab, fontsize=axFontSize)
    if ylab != 'y':
        plt.ylabel(ylab, fontsize=axFontSize)
    plt.title(title)
    if saveAs is not None:
        plt.savefig(saveAs, bbox_inches='tight')
    return


def violinOne(X, col=None, subplot=111, alpha=0.2):
    """
    Given a sample of data (and optionnally a boolean vector),
    returns a pyplot axis object which is the violin plot of the data.

    Parameters
    ----------
    X : array-like
            Vector
    col : array-like
            Indicates suspension and failure times
    subplot : int
            Subplot value for the axis to return
    alpha : float (0<=,=>1)
            Transparency of the dots

    Returns
    -------
    ax : pyplot axis
            Violin plot

    """
    if col is None:
        Xbool = np.ones(len(X), dtype=bool)
    else:
        Xbool = np.array(col, dtype=bool)
    Xsample = np.array(X)
    Yabs = np.linspace(np.min(Xsample), np.max(Xsample), 1001)
    Xabs = np.zeros(len(Xsample))
    density = []
    for i in range(1000):
        IND = np.where((Xsample > Yabs[i]) * (Xsample < Yabs[(i + 1)]))[0]
        density.append(len(IND))

    density = np.array(density, dtype=float)
    density /= float(np.max(density))
    for i in range(1000):
        IND = np.where((Xsample > Yabs[i]) * (Xsample < Yabs[(i + 1)]))[0]
        for ind in IND:
            Xabs[ind] = np.random.randn(1) * density[i]

    ax = plt.subplot(subplot)
    plt.scatter(Xabs[(~Xbool)], Xsample[(~Xbool)], alpha=alpha, color='grey')
    plt.scatter(Xabs[Xbool], Xsample[Xbool], alpha=2 * alpha, color='r', s=30)
    plt.xlim((-3, 3))
    return ax


def violinPlot(savefig=None, **kwargs):
    """
    Given a set of n data samples with their boolean vectors,
    returns n subplots with the violin plot of each sample.

    Usage: violinPlot(sample1=(X1,Xbool1), sample2=(X2,Xbool2), etc...)

    Parameters
    ----------
    savefig : string (default is None)
            If given, save the figure using savefig as the file name.
    kwargs : tuples
            For each sample, the data sample and the boolean vector must be provided in a tuple.

    """
    s = len(kwargs)
    fig = plt.figure(figsize=(10 * s, 20))
    plt.suptitle('Violin plot for %i samples' % s, fontsize=20)
    i = 1
    for name, (X, Xb) in kwargs.iteritems():
        violinOne(X, col=Xb, subplot=100 + 10 * s + i)
        plt.title(name)
        i += 1

    if savefig is not None:
        save_plot(fig, saveAs)
    else:
        plt.show()
    return


def hist_box(ar, perc=0, val=None, type='sym', annotation=True, distplot=False, trunc=False, bins=30, normed=True, alpha=0.6, color='b', kde=True, legend='', xmax=None):
    """
    Plots a histogram highlighting or filtering out the given percentage of data,
    according to the given type of filtering.

    3 different types available:

    * 'left': filter out the lower given percentage of data
    * 'right': filter out the upper given percentage of data
    * 'sym': both left and right filtering

    Parameters
    ----------
    ar : array-like
            Array of data
    perc : float in [0,100] (defaults to 0)
            Percentage of data to filter
    val : float
            An alternative to perc, gives the threshold value instead of percentage
    type: string (defaults to 'sym')
            Type of filtering
    annotation : bool (defaults to True)
            If True, writes complementary annotations on the plot
    distplot : bool (defaults to False)
            If True, uses seaborn distplot
    trunc : bool (defaults to False)
            If True, filters out the data and only displays remaining data. Otherwise, only highlight the selected data.
    bins : int (default is 30)
            Number of bins to use
    normed : bool (defaults to True)
            If True, histogram is normed
    alpha : float in [0,1] (defaults is 0.6)
            Transparency of the plot (0 is completely transparent, 1 is opaque)
    color : string (default is 'b')
            Color of the plot
    kde : bool (defaults to True)
            If using seaborn distplot, tells wether or not to plot the kernel density estimation ef the distribution    legend : string (default is '')
            Legend to use
    xmax : float
            Maximum x-value of the plot. If none is given, chooses the maximum value of the data.

    """
    ar_m = np.mean(ar)
    ar_std = np.std(ar)
    if type == 'sym':
        ar_ld = np.percentile(ar, perc)
        ar_ud = np.percentile(ar, 100 - perc)
        annot = str(100 - 2 * perc) + ' %'
    elif type == 'left':
        ar_ld = np.percentile(ar, perc)
        ar_ud = np.max(ar)
        if val is not None:
            ar_ld = float(val)
            perc = 100 * round(len(np.where(ar < val)[0]) / float(len(ar)), 3)
        annot = str(100 - perc) + ' %'
    elif type == 'right':
        ar_ld = np.min(ar)
        ar_ud = np.percentile(ar, 100 - perc)
        if val is not None:
            ar_ud = float(val)
            perc = 100 * round(len(np.where(ar > val)[0]) / float(len(ar)), 3)
        annot = str(100 - perc) + ' %'
    if trunc or perc == 0 and val is None:
        ar = ar.copy()
        ar, _ = relpy.model.statistics.frequentist.filter_dist(ar, low_b=ar_ld, up_b=ar_ud)
    elif annotation:
        plt.axvspan(ar_ld, ar_ud, alpha=0.15, color='grey')
    if distplot:
        sns.distplot(ar, bins=bins, color=color, kde=kde, hist_kws={'alpha': alpha, 'normed': normed})
    else:
        plt.hist(ar, bins=bins, normed=normed, alpha=alpha, color=color)
    if xmax is None:
        xmax = np.max(ar)
    plt.xlim(0, xmax)
    plt.legend([legend])
    if annotation:
        plt.axvline(ar_m, alpha=0.6, color='r', lw=5)
        plt.annotate(annot, (
         min(1, float(ar_ud / xmax)),
         0.85), xycoords='axes fraction', size=15, color='black', horizontalalignment='right')
        plt.annotate('$Mean =' + str(round(ar_m, 1)) + ' $', (1, 0.78), xycoords='axes fraction', size=18, fontweight='bold', color='black', horizontalalignment='right')
        if float((ar_m + ar_std / 2) / xmax) < 1:
            plt.axvspan(ar_m - ar_std / 2, ar_m + ar_std / 2, alpha=0.4, color='grey')
            plt.annotate('$1 \\sigma$', (
             float((ar_m + ar_std / 2) / xmax),
             0.9), xycoords='axes fraction', size=15, color='black', horizontalalignment='right')
            plt.annotate('$\\sigma =' + str(round(ar_std, 1)) + ' $', (1, 0.73), xycoords='axes fraction', size=18, fontweight='bold', color='black', horizontalalignment='right')
    return (
     ar_m, ar_std, ar_ld, ar_ud)


def make_readable_ticks(type='x'):
    """
    Turn your unreadable plot ticks (x-ticks or y-ticks)
    into nice, clean ticks.

    Works only for floats for now.

    Parameters
    ----------
    type : 'x' or 'y' (default is 'x')
            Choose 'x' if you want to change your x-ticks, 'y' for your y-ticks

    Notes
    -----
    Must be incorporated as part of a "regular" plot script
    (see example)

    Examples
    --------

    >>>

    """
    if type == 'x':
        locs, labels = plt.xticks()
    else:
        if type == 'y':
            locs, labels = plt.yticks()
        for i, lab in enumerate(labels):
            s = lab.get_text()
            new_s = str_float(float(new_val))
            lab.set_text(new_s)
            labels[i] = new_s

    if type == 'x':
        plt.xticks(locs, labels)
    elif type == 'y':
        plt.yticks(locs, labels)


def prepare_plot(xticks, yticks, figsize=(10.5, 6), hideLabels=False, gridColor='#999999', gridWidth=1.0):
    """function for generating pretty plot layout

    """
    plt.close()
    fig, ax = plt.subplots(figsize=figsize, facecolor='white', edgecolor='white')
    ax.axes.tick_params(labelcolor='#999999', labelsize='10')
    for axis, ticks in [(ax.get_xaxis(), xticks), (ax.get_yaxis(), yticks)]:
        axis.set_ticks_position('none')
        axis.set_ticks(ticks)
        axis.label.set_color('#999999')
        if hideLabels:
            axis.set_ticklabels([])

    plt.grid(color=gridColor, linewidth=gridWidth, linestyle='-')
    map(lambda position: ax.spines[position].set_visible(False), ['bottom', 'top', 'left', 'right'])
    return (
     fig, ax)


def save_plot(fig, path, filename=None, show=True, filetype='.png', dpi=270):
    """Function to save plots at high resolution and clean crop
    Requires a matplotlib figure object and a save path.

    """
    if filename:
        path = path + filename
    fig.savefig(path + filetype, bbox_inches='tight', dpi=dpi)
    try:
        if show:
            plt.show()
        plt.close()
    except:
        pass