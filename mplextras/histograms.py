import matplotlib.pyplot as plt
import matplotlib
import numpy as np


def hist(data, time=None, norm=True, errors=False, **kwargs):
    """
    Adds options to plot histograms with matplotlib.pyplot.hist:
    - time: if provided, normalizes the histogram to counts per unit time.
    - norm: if True, normalizes the histogram to counts per unit x (bin width).
    - errors: if True, adds error bars assuming Poisson statistics.
    """

    dummy_fig = matplotlib.figure.Figure()
    dummy_ax = matplotlib.axes.Axes(dummy_fig, (0,0,0,0))
    n, x, _ = dummy_ax.hist(data, **kwargs)
    del dummy_ax, dummy_fig

    # get the width of each bin, number of bins and range
    width = x[1] - x[0]
    bins = len(x) - 1 # -1 because x has the edges of the bins
    x_range = (x[0], x[-1])

    # calculate the weights
    weights = None
    weight = 1.0
    if time:
        weight /= time
    if norm:
        weight /= width
    weights = np.ones_like(data) * weight
    
    # calculate error bars
    err = None
    if errors:
        if time:
            err = np.sqrt(n) / time
        else:
            err = np.sqrt(n)
        if norm:
            err /= width
    
    if 'histtype' not in kwargs:
        kwargs['histtype'] = 'step'
    
    # plot the histogram
    ax = plt.gca()
    _n, __x, patches = ax.hist(data, weights=weights, **kwargs)
    color = patches[0].get_edgecolor()
    if errors:
        ax.errorbar(
            0.5 * (x[1:] + x[:-1]), n*weight, yerr=err, fmt='none', ecolor=color
        )

    


