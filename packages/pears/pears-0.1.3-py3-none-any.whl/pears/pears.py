from typing import Any, Dict, List, Optional, Tuple

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from fastkde import fastKDE


def kde(data):
    return fastKDE.pdf(data[~np.isnan(data)])[::-1]


def kde2d(x, y):
    mask = np.isnan(x) | np.isnan(y)
    return fastKDE.pdf(x[~mask], y[~mask])[::-1]


def _min_max(x):
    return np.nanmin(x), np.nanmax(x)


def _set_axis_edge_color(ax, color):
    ax.tick_params(color=color, labelcolor=color)
    for spine in ax.spines.values():
        spine.set_edgecolor(color)


def pears(
    dataset,
    indices: Optional[Any] = None,
    labels: Optional[str] = None,
    truths: Optional[List[float]] = None,
    marginal_color: str = "#5E81AC",
    marginal_lw: float = 3.0,
    annotate: bool = False,
    scatter: bool = True,
    scatter_color: str = "#5E81AC",
    scatter_alpha: float = 0.2,
    scatter_thin: int = 1,
    scatter_rasterized: bool = True,
    scatter_kwargs: Optional[Dict] = None,
    truths_color: str = "#2E3440",
    truths_linestyle: str = "--",
    truths_kwargs: Optional[Dict] = None,
    kde_color: str = "#8FBCBB",
    kde_cmap: str = "copper",
    kde_levels: List[float] = [0.5, 1.0, 1.5, 2.0],
    kde_fill: bool = False,
    xlim_quantiles: Optional[List[float]] = None,
    ylim_quantiles: Optional[List[float]] = None,
    figsize_scaling: float = 2.2,
    hspace: float = 0.05,
    wspace: float = 0.05,
    fontsize_ticks: float = 13.0,
    fontsize_labels: float = 22.0,
    fontsize_annotation: float = 22.0,
) -> Tuple[matplotlib.figure.Figure, matplotlib.axes.SubplotBase]:
    """
    Creates a pairs plot with marginal distributions along the diagonals and
    pairwise scatterplots with kernel density estimates in the lower diagonal
    panels.

    Inputs:
    -------
    dataset: obj
        Indexable dataset to plot (e.g., jax/numpy array, dict).

    indices (optional):
        List of indices to access data in `dataset`. Pass this if you only want
        to plot a subset of the data. If None, then uses all indices in `dataset`.

    labels: Optional[str]
        Labels for the axes. If None, then uses the indices of `dataset`.

    marginal_color: str = "#5E81AC"
        Color of the marginal KDE line.

    marginal_lw: float
        Linewidth of the marginal KDE line.

    annotate: bool
        Whether to annotate the marginal panels with the labels.

    scatter: bool
        Whether to plot the scatterplots.

    scatter_color: str
        Color of the scatterplot points.

    scatter_alpha: float
        Alpha of the scatterplot points.

    scatter_thin: int
        Thin the dataset by this factor before plotting the scatterplot.
        Use this to speed up plotting.

    scatter_rasterized: bool
        Whether to rasterize the scatterplot.

    scatter_kwargs: Optional[Dict]
        Additional keyword arguments to pass to `plt.scatter`.

    truths_color: str
        Color of the truth lines.

    truths_linestyle: str
        Linestyle of the truth lines.

    truths_kwargs: Optional[Dict]
        Additional keyword arguments to pass to `plt.axvline/plt.axhline`
        for the truth lines.

    kde_color: str
        Color of the KDE contours. Only used if `kde_cmap` is None.

    kde_cmap: str
        Colormap of the KDE contours. Takes precedence over `kde_color` if both
        are passed.

    kde_levels: List[float]
        Sigma levels to plot for the KDE contours.

    kde_fill: bool
        Whether to fill the KDE contours (using plt.contourf instead of plt.contour).

    xlim_quantiles: Optional[List[float]]
        Quantiles to use for the x-axis limits. If None, uses the
        range of the data (min and max).

    ylim_quantiles: Optional[List[float]]
        Quantiles to use for the y-axis limits. If None, uses the
        range of the data (min and max).

    figsize_scaling: float
        Scaling factor for the figure size.

    hspace: float
        Gridspec vertical (height) spacing between subplots.

    wspace: float
        Gridspec horizontal (width) spacing between subplots.

    fontsize_ticks: float
        Fontsize of the tick labels.

    fontsize_labels: float
        Fontsize of the axis labels.

    fontsize_annotation: float
        Fontsize of the annotation text.

    Outputs:
    --------

    fig: matplotlib.figure.Figure
        Top level container with all the plot elements.

    ax: matplotlib.axes.SubplotBase
        Axes with matplotlib subplots (2D array of panels).
    """

    marginal_kwargs = dict(
        color=marginal_color,
        linewidth=marginal_lw,
    )

    scatter_args = dict(
        color=scatter_color,
        alpha=scatter_alpha,
        rasterized=scatter_rasterized,
        edgecolor=scatter_color,
        s=10,
    )

    if scatter_kwargs:
        scatter_args.update(scatter_kwargs)

    kde_kwargs = dict(
        cmap=kde_cmap,  # cmap has priority
        colors=None if kde_cmap else kde_color,
    )

    truths_args = dict(
        color=truths_color,
        linestyle=truths_linestyle,
        zorder=5,
    )

    if truths_kwargs:
        truths_args.update(truths_kwargs)

    # levels outside of kde_kwargs because they need to be scaled later
    levels = 1.0 - np.exp(-0.5 * np.array(kde_levels) ** 2)

    if indices is None:
        if isinstance(dataset, dict):
            indices = list(dataset.keys())
        else:
            indices = np.arange(dataset.shape[0])

    assert indices is not None

    n = len(indices)

    if truths is not None:
        assert len(truths) == n

    fig, ax = plt.subplots(
        n,
        n,
        figsize=(n * figsize_scaling + 1, n * figsize_scaling + 1),
        gridspec_kw=dict(hspace=hspace, wspace=wspace),  # fmt: skip
    )

    for i in np.arange(n):

        # turn off upper panels
        for j in np.arange(i + 1, n):
            ax[i, j].axis("off")

        # marginal densities in diagonals
        x, y = kde(dataset[indices[i]])
        ax[i, i].plot(x, y, **marginal_kwargs)

        if truths is not None:
            ax[i, i].axvline(truths[i], **truths_args)

        _set_axis_edge_color(ax[i, i], "black")

        if xlim_quantiles:
            xlim = np.nanquantile(dataset[indices[i]], np.array(xlim_quantiles))
        else:
            xlim = _min_max(dataset[indices[i]])

        ax[i, i].set_xlim(*xlim)

        if annotate:
            ax[i, i].annotate(
                labels[i] if labels is not None else indices[i],
                fontsize=fontsize_annotation,
                xy=(0.8, 0.8),
                xycoords="axes fraction",
            )

        # lower diagonal panels
        for j in np.arange(i):
            # scatter pairs
            if scatter:
                ax[i, j].scatter(
                    dataset[indices[j]][::scatter_thin],
                    dataset[indices[i]][::scatter_thin],
                    **scatter_args,
                )

                if truths is not None:
                    ax[i, j].axvline(truths[j], **truths_args)
                    ax[i, j].axhline(truths[i], **truths_args)

                if xlim_quantiles:
                    xlim = np.nanquantile(dataset[indices[j]], np.array(xlim_quantiles))
                else:
                    xlim = _min_max(dataset[indices[j]])

                ax[i, j].set_xlim(*xlim)

                if ylim_quantiles:
                    ylim = np.nanquantile(dataset[indices[i]], np.array(ylim_quantiles))
                else:
                    ylim = _min_max(dataset[indices[i]])

                ax[i, j].set_ylim(*ylim)

                _set_axis_edge_color(ax[i, j], "black")

            # kde contours on top
            xy, z = kde2d(dataset[indices[j]], dataset[indices[i]])
            x, y = xy
            if kde_fill:
                ax[i, j].contourf(x, y, z, levels=levels, **kde_kwargs)
            else:
                ax[i, j].contour(x, y, z, levels=levels, **kde_kwargs)

        for j in np.arange(n):

            # hacky way to try to make tick positions consistent
            ax[i, j].yaxis.set_major_locator(plt.MaxNLocator(4))
            ax[i, j].xaxis.set_major_locator(plt.MaxNLocator(4))

            # left column:
            #   add label if not diagonal
            #   make the tick labels bigger
            #   rotate tick labels
            if j == 0:
                if i != j:
                    ax[i, j].set_ylabel(
                        labels[i] if labels else indices[i], fontsize=fontsize_labels
                    )
                ax[i, j].tick_params(
                    labelsize=fontsize_ticks, labelrotation=45, axis="y"
                )

            # not left column: turn off y tick labels
            else:
                ax[i, j].set_yticklabels([])

            # bottom row:
            #   add labels
            #   make tick labels bigger
            #   rotate tick labels
            if i == n - 1:
                ax[i, j].set_xlabel(
                    labels[j] if labels else indices[j], fontsize=fontsize_labels
                )
                ax[i, j].tick_params(
                    labelsize=fontsize_ticks, labelrotation=45, axis="x"
                )

            # not bottom row: turn off x tick labels
            else:
                ax[i, j].set_xticklabels([])

            # diagonals are special
            if i == j:
                # unless bottom one, remove x labels
                if j != n - 1:
                    ax[i, j].set_xticklabels([])
                    ax[i, j].xaxis.label.set_visible(False)

                # remove y ticks for all
                ax[i, j].set_yticks([])
                ax[i, j].set_yticklabels([])
                ax[i, j].yaxis.label.set_visible(False)

    return fig, ax
