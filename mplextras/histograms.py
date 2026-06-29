import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable


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
            0.5 * (__x[1:] + __x[:-1]), _n, yerr=err, fmt='none', ecolor=color
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
            0.5 * (__x[1:] + __x[:-1]), _n, yerr=err, fmt='none', ecolor=color
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

def hist2d(dataX, dataY, time=None, binscaling=True, cbarinfo="mean", cbarlabel="", marginals=False, **kwargs):
    """
    Plots a 2D histogram with options for time normalization and x/y normalization.
    - time: if provided, normalizes the histogram to counts per unit time.
    - binscaling: if True, normalizes the histogram to counts per unit x and y (bin surface).
    - marginals: if True, adds marginal histograms on top (X) and right (Y).
    - cbarinfo: if provided, adds visual indicators to the colorbar. Can be a combination of:
        "mean": a horizontal line at the mean count value across all bins.
        "box": a box spanning one standard deviation around the mean.
        "errorbar": error bars representing the standard deviation (can be split into "errorbar1"
                    for 1 std and "errorbar2" for 2 std).
    - cbarlabel: label for the colorbar.
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

    weights = np.ones_like(dataX, dtype=float) * weight

    if 'cmin' not in kwargs:
        kwargs['cmin'] = np.nextafter(0, 1) # avoid plotting empty bins

    # plot the histogram
    ax = plt.gca()
    ax_top = None
    ax_right = None
    if marginals:
        divider = make_axes_locatable(ax)
        ax_top = divider.append_axes('top', size='25%', pad=0.0, sharex=ax)
        ax_right = divider.append_axes('right', size='25%', pad=0.0, sharey=ax)
        ax.set_zorder(3)
        ax_top.set_zorder(1)
        ax_right.set_zorder(1)

    _n, __xedges, __yedges, im = ax.hist2d(dataX, dataY, weights=weights, **kwargs)
    plt.sca(ax)
    plt.sci(im) # set the current image for colorbar to work correctly

    if marginals:
        # use as color of the marginals hist the color corresponding to the mean count value across all bins in the 2D histogram
        cmap = kwargs.get('cmap', plt.get_cmap())
        if isinstance(cmap, str):
            cmap = plt.get_cmap(cmap)
        mean_n = np.nanmean(n * weight)
        normcolor = im.norm
        marginal_color = matplotlib.colors.to_rgba(cmap(normcolor(mean_n)), 1)

        marginal_kwargs = {
            key: value for key, value in kwargs.items()
            if key not in {'bins', 'range', 'cmap', 'norm', 'vmin', 'vmax', 'cmin', 'cmax'}
        }

        plt.sca(ax_top)
        hist(dataX, time=time, bins=xedges, color=marginal_color, fillalpha=0.25, **marginal_kwargs)
        plt.sca(ax_right)
        hist(dataY, time=time, bins=yedges, color=marginal_color, fillalpha=0.25, orientation='horizontal', **marginal_kwargs)
        plt.sca(ax) # restore the current axis to the main one
        #ax_top.hist(dataX, bins=xedges, weights=top_weights, color=marginal_color, **marginal_kwargs)
        #ax_right.hist(dataY, bins=yedges, weights=right_weights, orientation='horizontal', color=marginal_color, **marginal_kwargs)
        ax_top.set_xlim(ax.get_xlim())
        ax_right.set_ylim(ax.get_ylim())
        ax_top.set_facecolor('none')
        ax_right.set_facecolor('none')
        ax_top.tick_params(axis='both', which='both', bottom=False, top=False, left=False, right=False, labelbottom=False, labeltop=False, labelleft=False, labelright=False, length=0)
        ax_right.tick_params(axis='both', which='both', bottom=False, top=False, left=False, right=False, labelbottom=False, labeltop=False, labelleft=False, labelright=False, length=0)
        for spine in ax_top.spines.values():
            spine.set_visible(False)
        for spine in ax_right.spines.values():
            spine.set_visible(False)

    if cbarinfo or cbarlabel:
        # mean of all bins (flatten the 2D histogram to 1D and consider nans as 0's)
        mean_n = np.mean(np.nan_to_num(_n.flatten(), nan=0.0))
        std_n = np.std(np.nan_to_num(_n.flatten(), nan=0.0))

        if marginals:
            cbar = plt.colorbar(im, ax=ax, label=cbarlabel)
        else:
            cbar = plt.colorbar(im, label=cbarlabel)
        if "mean" in cbarinfo:
            cbar.ax.plot([0.05, 0.95], [mean_n, mean_n], color='white')

        box_plotted = False
        if "box" in cbarinfo:
            box_plotted = True
            std_box = plt.Rectangle((0.25, mean_n - std_n), 0.5, 2 * std_n, fill=False, edgecolor='white')
            cbar.ax.add_patch(std_box)

        if "errorbar" in cbarinfo:
            plot_both_errorbar = False
            if not "errorbar1" in cbarinfo and not "errorbar2" in cbarinfo:
                plot_both_errorbar = True
            if "errorbar1" in cbarinfo or plot_both_errorbar:
                if not box_plotted:
                    cbar.ax.errorbar([0.5], [mean_n], yerr=std_n, fmt='none', ecolor='white', label='Std', capsize=3, lw=2)
                else:
                    pass # if the box is plotted, the errorbar would be redundant, so we skip it to avoid cluttering the colorbar

            if "errorbar2" in cbarinfo or plot_both_errorbar:
                if not box_plotted:
                    cbar.ax.errorbar([0.5], [mean_n], yerr=2*std_n, fmt='none', ecolor='white', label='Std', capsize=0, lw=1)
                else:
                    # plot only from 1std to 2std to avoid cluttering the colorbar with the errorbar that would be redundant with the box
                    cbar.ax.errorbar([0.5], [mean_n + std_n], yerr=np.array([[0], [std_n]]), fmt='none', ecolor='white', label='Std', capsize=0, lw=1)
                    cbar.ax.errorbar([0.5], [mean_n - std_n], yerr=np.array([[std_n], [0]]), fmt='none', ecolor='white', label='Std', capsize=0, lw=1)

        plt.sca(ax) # restore the current axis

    return (_n, __xedges, __yedges), im
