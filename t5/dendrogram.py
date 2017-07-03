import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

linewidth = 1.5
xoffset = 0.5
color = "k"
xgrid = False

def visit_cluster(tree, labels, xticks, counter = 0):
    if isinstance(tree[0], tuple):
        (blx, bly) = visit_cluster(tree[0], labels, xticks)
    else:
        (blx, bly) = (0, len(labels))
        labels.append(tree[0])
    if isinstance(tree[1], tuple):
        (brx, bry) = visit_cluster(tree[1], labels, xticks)
    else:
        (brx, bry) = (0, len(labels))
        labels.append(tree[1])

    (ulx, uly) = (tree[2], bly)
    (urx, ury) = (tree[2], bry)

    plt.plot(
        [blx, ulx, urx, brx],
        [bly, uly, ury, bry],
        color,
        linewidth = linewidth)

    xticks.append(tree[2])

    return (tree[2], (bly + bry) / 2)

# tree = (((A, B, dist), C, dist), ...)
def plot(tree):
    labels = []
    xticks = [0]
    
    fig, ax = plt.subplots()

    visit_cluster(tree, labels, xticks)

    ml = MultipleLocator(xoffset)
    ax.set_yticks(list(range(len(labels))))
    ax.set_yticklabels(labels)
    ax.set_xlim(0, max(xticks) + xoffset)
    ax.set_xticks(xticks)
    ax.xaxis.set_minor_locator(ml)
    ax.yaxis.set_tick_params(width = linewidth)
    
    if xgrid:
        ax.xaxis.grid()

    fig.show()

    return fig