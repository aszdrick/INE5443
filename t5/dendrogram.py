import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import math
from sys import maxsize

linewidth = 1.5
xoffset = 0.5
color = "k"
xgrid = False

class Classifier:
    # weights = (size weight, average weight, stddev weight)
    # priority = desirable value of size
    def __init__(self, weights, priority, interval):
        self.weights = weights
        self.priority = priority
        self.interval = interval

    def __call__(self, values):
        vs = []
        vs.append(1 / (abs(self.priority - values[0]) + 1))
        vs.append(self.min_average / values[1])
        vs.append(self.min_stddev / values[2])
        return sum([w * v for w, v in zip(self.weights, vs)])

def __visit_cluster(tree, labels, xticks, counter = 0):
    if isinstance(tree[0], tuple):
        (blx, bly) = __visit_cluster(tree[0], labels, xticks)
    else:
        (blx, bly) = (0, len(labels))
        labels.append(tree[0])
    if isinstance(tree[1], tuple):
        (brx, bry) = __visit_cluster(tree[1], labels, xticks)
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


# def plot_twist(tree):
#     labels = []
#     xticks = [0]
#     label_xs = {}

#     for node in tree:
#         if len(node[0]) == 1:
#             label_xs[node[0][0]] = len(labels)
#             labels.append(node[0][0])
#             (blx, bly) = (0, len(labels))
#         else:
#             values = [label_xs[l] for l in node[0]]
#             blx = (max(values) + min(values)) / 2
#         if len(node[1]) == 1:
#             label_xs[node[1][0]] = len(labels)
#             labels.append(node[1][0])
#             (brx, bry) = (0, len(labels))
#         else:
#             values = [label_xs[l] for l in node[1]]
#             middle = (max(values) + min(values)) / 2

def __plot_tree(tree)
    labels = []
    xticks = [0]

    __visit_cluster(tree, labels, xticks)

    return (labels, xticks)

def __plot_subtrees(trees):
    labels = []
    xticks = [0]

    for tree in trees:
        if isinstance(tree, str):
            labels.append(tree)
        else:
            __visit_cluster(tree, labels, xticks)
    return (labels, xticks)


# tree = (((A, B, dist), C, dist), )
def plot(data):
    if isinstance(data, list)
        (labels, xticks) = __plot_subtrees(data)
    else:
        (labels, xticks) = __plot_tree(data)

    __visit_cluster(tree, labels, xticks)

    ml = MultipleLocator(xoffset)
    ax = plt.axes()
    ax.set_yticks(list(range(len(labels))))
    ax.set_yticklabels(labels)
    ax.set_xlim(0, max(xticks) + xoffset)
    ax.set_xticks(xticks)
    ax.xaxis.set_minor_locator(ml)
    ax.yaxis.set_tick_params(width = linewidth)
    
    if xgrid:
        ax.xaxis.grid()

def labels_of(tree):
    labels = []
    if isinstance(tree[0], tuple):
        labels += labels_of(tree[0])
    else:
        labels.append(tree[0])
    if isinstance(tree[1], tuple):
        labels += labels_of(tree[1])
    else:
        labels.append(tree[1])
    return labels

def __levelize(tree, levels, counter = 0):
    if isinstance(tree[0], tuple):
        __levelize(tree[0], levels, counter + 1)
    if isinstance(tree[1], tuple):
        __levelize(tree[1], levels, counter + 1)
    if counter not in levels.keys():
        levels[counter] = []
    levels[counter].append(tree)

def levels_of(tree):
    levels = {}
    __levelize(tree, levels)
    return levels

def best_level(levels, weights, interval, priority):
    score_it = Classifier(weights, priority, interval)
    statistics = {}
    min_average = maxsize
    min_stddev = maxsize

    for (i, level) in levels.items():
        distances = list(map((lambda x: x[2]), level))
        groups = len(distances)
        xm = sum(distances) / groups
        stddev = math.sqrt(sum(map(lambda x: (x - xm) ** 2, distances)))
        statistics[i] = (groups, xm, stddev)
        if xm < min_average:
            min_average = xm
        if stddev < min_stddev:
            min_stddev = stddev

    score_it.min_average = min_average
    score_it.min_stddev = min_stddev
    best_level = -1
    best_score = 0

    for (i, values) in statistics.items():
        score = score_it(values)
        if score > best_score:
            best_score = score
            best_level = i

    print(levels)
    print("best level is", best_level)
    print("best score is", best_score)
    return best_level

def cut(tree, weights, interval, priority = None):
    labels = labels_of(tree)
    levels = levels_of(tree)
    max_level = max(levels.keys())
    if not priority:
        priority = round((interval[0] + interval[1]) / 2)

    for i in range(max_level + 1):
        level_labels = []
        for tup in levels[i]:
            level_labels += labels_of(tup)
        length = len(levels[i])
        # len(level_labels) != len(labels)
        if length > interval[1] or length < interval[0]:
            del levels[i]

    chosen_level = best_level(levels, weights, interval, priority)

    trees = [tree]
    for i in range(chosen_level):
        new_trees = []
        for j in range(len(trees)):
            if isinstance(trees[j], tuple):
                new_trees.append(trees[j][0])
                new_trees.append(trees[j][1])
            else:
                new_trees.append(trees[j])
        trees = new_trees

    return trees
