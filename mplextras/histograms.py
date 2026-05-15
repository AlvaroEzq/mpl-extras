import matplotlib.pyplot as plt
import matplotlib
import numpy as np


def hist(data, time=None, binscaling=True, errors=False, fillalpha=None, **kwargs):
    """
    Adds options to plot histograms with matplotlib.pyplot.hist:
    - time: if provided, normalizes the histogram to counts per unit time.
    - binscaling: if True, normalizes the histogram to counts per unit x (bin width).
    - errors: if True, adds error bars assuming Poisson statistics.
    - fillalpha: if provided, sets the alpha of the histogram fill (face) color. If no facecolor is given,
                it uses the edgecolor or color to apply the alpha.
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
    if binscaling:
        weight /= width
    weights = np.ones_like(data) * weight
    
    # calculate error bars
    err = None
    if errors:
        if time:
            err = np.sqrt(n) / time
        else:
            err = np.sqrt(n)
        if binscaling:
            err /= width
    
    # Parse the color for fillalpha application and histtype adjustment
    facecolor = None
    edgecolor = None
    no_color_given = False
    if fillalpha is not None:
        # set alpha of the given facecolor by the user
        if 'facecolor' in kwargs or 'facecolors' in kwargs:
            facecolor = matplotlib.colors.to_rgba(kwargs.get('facecolor') or kwargs.get('facecolors'), fillalpha)
            kwargs['facecolor'] = facecolor
            if 'color' in kwargs: # move the color to the edgecolor to avoid overriden the facecolor
                edgecolor = kwargs['color'] # keep the color priority as in matplotlib behaviour
                kwargs['edgecolor'] = edgecolor
                kwargs.pop('color', None)
        # if no facecolor is given, use the color or edgecolor as the facecolor to apply the alpha
        elif 'color' in kwargs or 'edgecolor' in kwargs or 'edgecolors' in kwargs:
            edgecolor = kwargs.get('color') or kwargs.get('edgecolor') or kwargs.get('edgecolors')
            facecolor = matplotlib.colors.to_rgba(edgecolor, fillalpha)
            kwargs['facecolor'] = facecolor
            kwargs['edgecolor'] = edgecolor
            kwargs.pop('color', None)
        else:
            no_color_given = True

    # set the default histtype
    if 'histtype' not in kwargs:
        if fillalpha is None:
            kwargs['histtype'] = 'step' # default to 'step'
        else:
            kwargs['histtype'] = 'stepfilled' # default to 'stepfilled' if fillalpha is provided
    elif kwargs['histtype'] == 'step' and fillalpha is not None:
        raise ValueError("Cannot use fillalpha with histtype='step'. Use histtype='stepfilled' instead.")

    # plot the histogram
    ax = plt.gca()
    _n, __x, patches = ax.hist(data, weights=weights, **kwargs)
    color = patches[0].get_edgecolor()
    if no_color_given and fillalpha is not None:
        color = patches[0].get_facecolor() # I dont know why but when no color is given, the edgecolor is set to (0, 0, 0, 0)
        facecolor = matplotlib.colors.to_rgba(color, fillalpha)
        for p in patches:
            p.set_edgecolor(color)
            p.set_facecolor(facecolor)

    if errors:
        ax.errorbar(
            0.5 * (x[1:] + x[:-1]), n*weight, yerr=err, fmt='none', ecolor=color
        )
    
    return (_n, __x, patches), err if errors else None


def sumhist(data_list, times=None, binscaling=True, errors=False, fillalpha=None, **kwargs):
    """
    Plots the sum of several histograms (with the same binning) with different times.
    - data_list: list of data arrays to be histogrammed and summed.
    - times: list of times for each dataset. If provided, normalizes each histogram to counts per unit time before summing.
    - binscaling: if True, normalizes the histogram to counts per unit x (bin width).
    - errors: if True, adds error bars assuming Poisson statistics.
    - fillalpha: if provided, sets the alpha of the histogram fill (face) color. If no facecolor is given,
                it uses the edgecolor or color to apply the alpha.
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
    if binscaling:
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

    # Parse the color for fillalpha application and histtype adjustment
    facecolor = None
    edgecolor = None
    no_color_given = False
    if fillalpha is not None:
        # set alpha of the given facecolor by the user
        if 'facecolor' in kwargs or 'facecolors' in kwargs:
            facecolor = matplotlib.colors.to_rgba(kwargs.get('facecolor') or kwargs.get('facecolors'), fillalpha)
            kwargs['facecolor'] = facecolor
            if 'color' in kwargs: # move the color to the edgecolor to avoid overriden the facecolor
                edgecolor = kwargs['color'] # keep the color priority as in matplotlib behaviour
                kwargs['edgecolor'] = edgecolor
                kwargs.pop('color', None)
        # if no facecolor is given, use the color or edgecolor as the facecolor to apply the alpha
        elif 'color' in kwargs or 'edgecolor' in kwargs or 'edgecolors' in kwargs:
            edgecolor = kwargs.get('color') or kwargs.get('edgecolor') or kwargs.get('edgecolors')
            facecolor = matplotlib.colors.to_rgba(edgecolor, fillalpha)
            kwargs['facecolor'] = facecolor
            kwargs['edgecolor'] = edgecolor
            kwargs.pop('color', None)
        else:
            no_color_given = True

    # set the default histtype
    if 'histtype' not in kwargs:
        if fillalpha is None:
            kwargs['histtype'] = 'step' # default to 'step'
        else:
            kwargs['histtype'] = 'stepfilled' # default to 'stepfilled' if fillalpha is provided
    elif kwargs['histtype'] == 'step' and fillalpha is not None:
        raise ValueError("Cannot use fillalpha with histtype='step'. Use histtype='stepfilled' instead.")
    
    #plot
    ax = plt.gca()
    _n, __x, patches = ax.hist(data, weights=concat_weights, **kwargs)
    color = patches[0].get_edgecolor()
    if no_color_given and fillalpha is not None:
        color = patches[0].get_facecolor() # I dont know why but when no color is given, the edgecolor is set to (0, 0, 0, 0)
        facecolor = matplotlib.colors.to_rgba(color, fillalpha)
        for p in patches:
            p.set_edgecolor(color)
            p.set_facecolor(facecolor)

    if errors:
        ax.errorbar(
            0.5 * (x[1:] + x[:-1]), _n, yerr=err, fmt='none', ecolor=color
        )

    return (_n, __x, patches), err if errors else None

def diffhist(data1, data2, time1=None, time2=None, binscaling=True, errors=False, fillalpha=None, **kwargs):
    """
    Plots the difference between histograms with identical binning:
        hist(data1) - sum(hist(d) for d in data2)
    - data2: array-like or list of array-like datasets to subtract.
    - time1/time2: if provided, normalize each histogram independently to counts per unit time.
      For multiple datasets in data2, time2 can be a scalar or a list with matching length.
    - binscaling: if True, normalize to counts per unit x (bin width).
    - errors: if True, add propagated Poisson errors.
    - fillalpha: if provided, sets the alpha of the histogram fill (face) color. If no facecolor is given,
                it uses the edgecolor or color to apply the alpha.
    """

    data2_list = list(data2) if isinstance(data2, (list, tuple)) else [data2]
    if len(data2_list) == 0:
        raise ValueError('data2 must contain at least one dataset')

    if time2 is None:
        time2_list = [None] * len(data2_list)
    elif np.isscalar(time2):
        time2_list = [time2] * len(data2_list)
    else:
        time2_list = list(time2)
        if len(time2_list) != len(data2_list):
            raise ValueError('time2 must be a scalar or a list with same length as data2')

    dummy_fig = matplotlib.figure.Figure()
    dummy_ax = matplotlib.axes.Axes(dummy_fig, (0,0,0,0))
    kwargs_bins = kwargs.get('bins', None)
    kwargs_range = kwargs.get('range', None)
    ns, x, _ = dummy_ax.hist([data1] + data2_list, bins=kwargs_bins, range=kwargs_range)
    del dummy_ax, dummy_fig

    n1 = ns[0]
    n2_list = ns[1:]
    width = x[1] - x[0]

    def _get_weight(time_value):
        w = 1.0
        if time_value is not None:
            if time_value != 0:
                w /= time_value
            else:
                w = 0.0
        if binscaling:
            w /= width
        return w

    w1 = _get_weight(time1)
    w2_list = [_get_weight(t) for t in time2_list]

    all_data = [data1] + data2_list
    all_weights = [np.ones_like(data1, dtype=float) * w1]
    for d2, w2 in zip(data2_list, w2_list):
        all_weights.append(np.ones_like(d2, dtype=float) * (-w2))
    data = np.concatenate(all_data)
    weights = np.concatenate(all_weights)

    err = None
    if errors:
        err2_sum = np.zeros_like(n1, dtype=float)
        for n2, w2 in zip(n2_list, w2_list):
            err2_sum += (np.sqrt(n2) * w2) ** 2
        err = np.sqrt((np.sqrt(n1) * w1) ** 2 + err2_sum)

    # Parse the color for fillalpha application and histtype adjustment
    facecolor = None
    edgecolor = None
    no_color_given = False
    if fillalpha is not None:
        # set alpha of the given facecolor by the user
        if 'facecolor' in kwargs or 'facecolors' in kwargs:
            facecolor = matplotlib.colors.to_rgba(kwargs.get('facecolor') or kwargs.get('facecolors'), fillalpha)
            kwargs['facecolor'] = facecolor
            if 'color' in kwargs: # move the color to the edgecolor to avoid overriden the facecolor
                edgecolor = kwargs['color'] # keep the color priority as in matplotlib behaviour
                kwargs['edgecolor'] = edgecolor
                kwargs.pop('color', None)
        # if no facecolor is given, use the color or edgecolor as the facecolor to apply the alpha
        elif 'color' in kwargs or 'edgecolor' in kwargs or 'edgecolors' in kwargs:
            edgecolor = kwargs.get('color') or kwargs.get('edgecolor') or kwargs.get('edgecolors')
            facecolor = matplotlib.colors.to_rgba(edgecolor, fillalpha)
            kwargs['facecolor'] = facecolor
            kwargs['edgecolor'] = edgecolor
            kwargs.pop('color', None)
        else:
            no_color_given = True

    # set the default histtype
    if 'histtype' not in kwargs:
        if fillalpha is None:
            kwargs['histtype'] = 'step' # default to 'step'
        else:
            kwargs['histtype'] = 'stepfilled' # default to 'stepfilled' if fillalpha is provided
    elif kwargs['histtype'] == 'step' and fillalpha is not None:
        raise ValueError("Cannot use fillalpha with histtype='step'. Use histtype='stepfilled' instead.")

    ax = plt.gca()
    _n, __x, patches = ax.hist(data, weights=weights, **kwargs)
    color = patches[0].get_edgecolor()
    if no_color_given and fillalpha is not None:
        color = patches[0].get_facecolor() # I dont know why but when no color is given, the edgecolor is set to (0, 0, 0, 0)
        facecolor = matplotlib.colors.to_rgba(color, fillalpha)
        for p in patches:
            p.set_edgecolor(color)
            p.set_facecolor(facecolor)

    if errors:
        ax.errorbar(
            0.5 * (x[1:] + x[:-1]), _n, yerr=err, fmt='none', ecolor=color
        )

    return (_n, __x, patches), err if errors else None

def hist2d(dataX, dataY, time=None, binscaling=True, **kwargs):
    """
    Plots a 2D histogram with options for time normalization and x/y normalization.
    - time: if provided, normalizes the histogram to counts per unit time.
    - binscaling: if True, normalizes the histogram to counts per unit x and y (bin surface).
    """

    dummy_fig = matplotlib.figure.Figure()
    dummy_ax = matplotlib.axes.Axes(dummy_fig, (0,0,0,0))
    n, xedges, yedges, _ = dummy_ax.hist2d(dataX, dataY, **kwargs)
    del dummy_ax, dummy_fig

    # get the width of each bin in x and y
    xwidth = xedges[1] - xedges[0]
    ywidth = yedges[1] - yedges[0]

    # calculate the weights
    weight = 1.0
    if time:
        weight /= time
    if binscaling:
        weight /= (xwidth * ywidth)

    weights = np.ones_like(dataX) * weight

    if 'cmin' not in kwargs:
        kwargs['cmin'] = np.nextafter(0, 1) # avoid plotting empty bins

    # plot the histogram
    ax = plt.gca()
    _n, __xedges, __yedges, im = ax.hist2d(dataX, dataY, weights=weights, **kwargs)
    plt.sci(im) # set the current image for colorbar to work correctly

    return _n, __xedges, __yedges, im
