import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.font_manager import FontProperties
import numpy as np

def plot(data, result, training_set, categories, axis_labels, colors):
    xs = np.array([data[i][0] for i in range(len(data))])
    ys = np.array([data[i][1] for i in range(len(data))])
    cs = np.array([colors[r] for r in result])

    fig, ax = plt.subplots()

    mo = plt.scatter(xs, ys, c=cs, marker='o')

    xs = np.array([training_set[i][0] for i in range(len(training_set))])
    ys = np.array([training_set[i][1] for i in range(len(training_set))])
    cs = np.array([colors[r] for r in categories])

    mt = plt.scatter(xs, ys, c=cs, marker='^')

    ax.set_xlabel(axis_labels[0])
    ax.set_ylabel(axis_labels[1])

    mc = []
    for cat in colors:
        mc.append(mpatches.Patch(color=colors[cat]))

    handles = [mo, mt] + mc
    plt.legend(
        handles,
        ["Classified data", "Training data"] + [cat for cat in colors],
        scatterpoints=1,
        fontsize='small',
        bbox_to_anchor=(0., 1., 1., .024),
        loc=3,
        fancybox=False,
        ncol= 3,
        mode="expand",
        borderaxespad=0.,
        edgecolor='black'
    )

    plt.show()
    plt.close(fig)

def plot_voronoi(voronoi, training_set, categories, axis_labels, colors, show_legend = True):
    from scipy.spatial import Voronoi, voronoi_plot_2d
    voronoi_plot_2d(voronoi, show_points=False, show_vertices=False)

    ys = np.array([training_set[i][1] for i in range(len(training_set))])
    xs = np.array([training_set[i][0] for i in range(len(training_set))])
    cs = np.array([colors[r] for r in categories])

    plt.scatter(xs, ys, c=cs)
    ax = plt.gca()

    ax.set_xlabel(axis_labels[0])
    ax.set_ylabel(axis_labels[1])

    if show_legend:
        mc = []
        for cat in colors:
            mc.append(mpatches.Patch(color=colors[cat]))

        # handles = [mt] + mc
        handles = mc
        plt.legend(
            handles,
            [cat for cat in colors],
            scatterpoints=1,
            fontsize='small',
            bbox_to_anchor=(0., 1., 1., .024),
            loc=3,
            fancybox=False,
            ncol= 3,
            mode="expand",
            borderaxespad=0.,
            edgecolor='black'
        )

    plt.show()
