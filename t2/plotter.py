import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.font_manager import FontProperties
import numpy as np

def plot(training_set, test_set, data, axis_labels, colors):
    fig, ax = plt.subplots()
    ax.set_xlabel(axis_labels[0])
    ax.set_ylabel(axis_labels[1])

    xs = np.array([entry[0] for entry in training_set])
    ys = np.array([entry[1] for entry in training_set])
    cs = np.array([colors[entry[2]] for entry in training_set])
    mt = plt.scatter(xs, ys, c=cs, marker='^')
    handles = [mt]
    labels = ["Training set"]

    if len(test_set) > 0:
        xs = np.array([entry[0] for entry in test_set])
        ys = np.array([entry[1] for entry in test_set])
        cs = np.array([colors[entry[2]] for entry in test_set])
        mo = plt.scatter(xs, ys, c=cs, marker='o')
        handles.append(mo)
        labels.append("Test set")

    if len(data) > 0:
        xs = np.array([entry[0] for entry in test_set])
        ys = np.array([entry[1] for entry in test_set])
        cs = np.array([colors[entry[2]] for entry in test_set])
        md = plt.scatter(xs, ys, c=cs, marker='o')
        handles.append(md)
        labels.append("Classified data")

    mc = []
    for cat in colors:
        mc.append(mpatches.Patch(color=colors[cat]))

    handles += mc
    plt.legend(
        handles,
        labels + [cat for cat in colors],
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
