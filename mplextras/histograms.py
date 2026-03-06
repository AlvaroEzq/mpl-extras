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
        err_container = ax.errorbar(
            0.5 * (x[1:] + x[:-1]), n*weight, yerr=err, fmt='none', ecolor=color
        )
    
    return (_n, __x, patches), err_container if errors else None


def sumhist(data_list, times=None, norm=True, errors=False, **kwargs):
    """
    Plots the sum of several histograms (with the same binning) with different times.
    - data_list: list of data arrays to be histogrammed and summed.
    - times: list of times for each dataset. If provided, normalizes each histogram to counts per unit time before summing.
    - norm: if True, normalizes the histogram to counts per unit x (bin width).
    - errors: if True, adds error bars assuming Poisson statistics.
    """

    dummy_fig = matplotlib.figure.Figure()
    dummy_ax = matplotlib.axes.Axes(dummy_fig, (0,0,0,0))
    kwargs_bins = kwargs.get('bins', None)
    kwargs_range = kwargs.get('range', None)
    ns, x, _ = dummy_ax.hist(data_list, bins=kwargs_bins, range=kwargs_range)
    del dummy_ax, dummy_fig

    data = np.concatenate(data_list)

    # get the width of each bin, number of bins and range
    width = x[1] - x[0]
    bins = len(x) - 1 # -1 because x has the edges of the bins
    x_range = (x[0], x[-1])

    # calculate the weights
    weight_list = np.ones_like(times) * 1.0
    if times:
        weight_list /= times
    if norm:
        weight_list /= width
    
    weights = []
    for w, d in zip(weight_list, data_list):
        weights.append(np.ones_like(d) * w)
    concat_weights = np.concatenate(weights)
    
    # calculate error bars    err = None
    if errors:
        err = []
        for w, n in zip(weight_list, ns):
            if w != 0:
                err.append(np.sqrt(n) * w)
            else:
                err.append(np.zeros_like(n))
        err = np.sqrt(np.sum(np.array(err)**2, axis=0))

    if 'histtype' not in kwargs:
        kwargs['histtype'] = 'step'
    
    #plot
    ax = plt.gca()
    _n, __x, patches = ax.hist(data, weights=concat_weights, **kwargs)
    color = patches[0].get_edgecolor()
    if errors:
        err_container = ax.errorbar(
            0.5 * (x[1:] + x[:-1]), _n, yerr=err, fmt='none', ecolor=color
        )

    return (_n, __x, patches), err_container if errors else None
