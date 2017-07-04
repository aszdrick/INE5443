import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import math
from sys import maxsize

linewidth = 1.5
xoffset = 0.5
color = "k"
xgrid = False

# class to encapsulate the fitness function, i.e.,
# how good is a level using the specified set of weights and
# interval.
class Classifier:
    # weights = (size weight, average weight, stddev weight)
    def __init__(self, weights, interval):
        self.weights = weights
        self.interval = interval

    def __call__(self, values):
        vs = []
        vs.append(self.min_average / values[0])
        vs.append(self.min_stddev / values[1])
        return sum([w * v for w, v in zip(self.weights, vs)])

def __visit_cluster(tree, labels, xticks, counter = 0):
    if isinstance(tree, tuple):
        bottom_left = __visit_cluster(tree[0], labels, xticks)
        bottom_right = __visit_cluster(tree[1], labels, xticks)
    else:
        labels.append(tree)
        return (0, len(labels) - 1)

    plt.plot(
        [bottom_left[0], tree[2], tree[2], bottom_right[0]],
        [bottom_left[1], bottom_left[1], bottom_right[1], bottom_right[1]],
        color,
        linewidth = linewidth)

    xticks.append(tree[2])

    return (tree[2], (bottom_left[1] + bottom_right[1]) / 2)

def __plot_tree(tree):
    labels = []
    xticks = [0]

    __visit_cluster(tree, labels, xticks)

    return (labels, xticks)

def __plot_subtrees(trees):
    labels = []
    xticks = [0]

    for tree in trees:
        if isinstance(tree, tuple):
            __visit_cluster(tree, labels, xticks)
        else:
            labels.append(tree)
    return (labels, xticks)


def plot(data):
    if isinstance(data, list):
        (labels, xticks) = __plot_subtrees(data)
    else:
        (labels, xticks) = __plot_tree(data)

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
    if isinstance(tree, tuple):
        labels += labels_of(tree[0])
        labels += labels_of(tree[1])
    else:
        labels.append(tree)
    return labels

def __levelize(tree, levels, counter = 0):
    if isinstance(tree, tuple):
        __levelize(tree[0], levels, counter + 1)
        __levelize(tree[1], levels, counter + 1)
    if counter not in levels.keys():
        levels[counter] = []
    levels[counter].append(tree)

def __levels_of(tree):
    levels = {}
    __levelize(tree, levels)
    return levels

def __best_level(levels, weights, interval):
    score_it = Classifier(weights, interval)
    statistics = {}
    min_average = maxsize
    min_stddev = maxsize

    for (i, level) in levels.items():
        distances = list(map((lambda x: x[2]), level))
        groups = len(distances)
        xm = sum(distances) / groups
        stddev = math.sqrt(sum(map(lambda x: (x - xm) ** 2, distances)))
        statistics[i] = (xm, stddev)
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

def cut(tree, weights, interval):
    labels = labels_of(tree)
    levels = __levels_of(tree)
    max_level = max(levels.keys())

    for i in range(max_level + 1):
        level_labels = []
        for tup in levels[i]:
            level_labels += labels_of(tup)
        length = len(levels[i])
        if length > interval[1] or length < interval[0]:
            del levels[i]

    chosen_level = __best_level(levels, weights, interval)

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
