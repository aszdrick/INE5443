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
class LevelEvaluator:
    # weights = (average weight, sd weight)
    # interval = (min classes, max classes)
    def __init__(self, weights, interval, min_avg, min_sd):
        self.weights = weights
        self.interval = interval
        self.min_avg = min_avg
        self.min_sd = min_sd

    def __call__(self, values):
        vs = []
        vs.append(self.min_avg / (values[0] + 1))
        vs.append(self.min_sd / (values[1] + 1))
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

    if tree[2] not in xticks:
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
    ax = plt.gca()
    ax.set_yticks(list(range(len(labels))))
    ax.set_yticklabels(labels)
    ax.set_xlim(0, max(xticks) + xoffset)
    ax.set_xticks(xticks)
    ax.xaxis.set_minor_locator(ml)
    ax.yaxis.set_tick_params(width = linewidth)
    
    if xgrid:
        ax.xaxis.grid()

    return plt.gcf()

def __labels_of(tree):
    labels = []
    if isinstance(tree, tuple):
        labels += __labels_of(tree[0])
        labels += __labels_of(tree[1])
    else:
        labels.append(tree)
    return labels

def __break_by_two(trees):
    subtrees = []
    for st in trees:
        if isinstance(st, tuple):
            subtrees.append(st[0])
            subtrees.append(st[1])
        else:
            subtrees.append(st)
    return subtrees

def __distance_of(cluster):
    if isinstance(cluster, tuple):
        return cluster[2]
    return 0

def __statistics(subtrees):
    distances = list(map(__distance_of, subtrees))
    clusters = len(distances)
    avg = sum(distances) / clusters
    sd = math.sqrt(sum(map(lambda x: (x - avg) ** 2, distances)))
    return (avg, sd, distances)

def __gather_info(subtrees, interval, level):
    marked_subtrees = {}
    min_avg = maxsize
    min_sd = maxsize

    while len(subtrees) < interval[1]:
        (avg, sd, distances) = __statistics(subtrees)
        if avg < min_avg:
            min_avg = avg
        if sd < min_sd:
            min_sd = sd
        marked_subtrees[(avg, sd, level, 0)] = subtrees
        if len(subtrees) < interval[1]:
            for (i, distance) in enumerate(distances):
                if distance > avg:
                    diff = distance - avg
                    chosen = subtrees[i]
                    d0 = __distance_of(chosen[0])
                    d1 = __distance_of(chosen[1])
                    if abs(d0 - avg) > diff or abs(d1 - avg) > diff:
                        continue
                    derivation = subtrees[:i]
                    derivation.append(chosen[0])
                    derivation.append(chosen[1])
                    derivation += subtrees[i+1:]
                    (avg, sd, d) = __statistics(derivation)
                    if avg < min_avg:
                        min_avg = avg
                    if sd < min_sd:
                        min_sd = sd
                    marked_subtrees[(avg, sd, level, i)] = derivation
        # Descend one level
        subtrees = __break_by_two(subtrees)

    return (marked_subtrees, min_avg, min_sd)

def cut(tree, weights, interval):
    subtree_counter = 1
    subtrees = [tree]
    level = 1

    while len(subtrees) <= interval[0] / 2:
        new_subtrees = []
        subtrees = __break_by_two(subtrees)
        subtree_counter = len(subtrees)
        level += 1

    (marked_subtrees, min_avg, min_sd) = __gather_info(subtrees, interval, level)
    
    evaluator = LevelEvaluator(weights, interval, min_avg, min_sd)
    best_score = 0
    best_subtree = None

    for key in marked_subtrees:
        score = evaluator(key[0:2])
        if score > best_score:
            best_subtree = key

    print(key)
    return marked_subtrees[best_subtree]

def get_clusters(trees):
    clusters = {}
    for i, tree in enumerate(trees):
        for instance in __labels_of(tree):
            clusters[instance] = i
    return clusters

def __levelize(tree, levels, counter = 0):
    if isinstance(tree, tuple):
        __levelize(tree[0], levels, counter + 1)
        __levelize(tree[1], levels, counter + 1)
    if counter not in levels.keys():
        levels[counter] = []
    levels[counter].append(tree)

def __levels_of(tree, labels):
    labels_set = set(labels)
    levels = {}
    __levelize(tree, levels)
    for (i, level) in levels.items():
        level_labels = set()
        for t in level:
            level_labels |= set(__labels_of(t))
        diff = labels_set - level_labels
        levels[i] += list(diff)
    return levels

def __best_level(levels, weights, interval):
    def get_distances(x):
        if isinstance(x, tuple):
            return x[2]
        return 0
    statistics = {}
    min_avg = maxsize
    min_sd = maxsize

    for (i, level) in levels.items():
        distances = list(map(get_distances, level))
        clusters = len(distances)
        avg = sum(distances) / clusters
        sd = math.sqrt(sum(map(lambda x: (x - avg) ** 2, distances)))
        statistics[i] = (avg, sd)
        if avg < min_avg:
            min_avg = avg
        if sd < min_sd:
            min_sd = sd

    evaluator = LevelEvaluator(weights, interval, min_avg, min_sd)
    best_level = -1
    best_score = 0

    for (i, values) in statistics.items():
        score = evaluator(values)
        if score > best_score:
            best_score = score
            best_level = i

    return best_level

def cut_by_level(tree, weights, interval):
    labels = __labels_of(tree)
    levels = __levels_of(tree, labels)
    max_level = max(levels.keys())

    for i in range(max_level + 1):
        level_labels = []
        for tup in levels[i]:
            level_labels += __labels_of(tup)
        length = len(levels[i])
        if length > interval[1] or length < interval[0]:
            del levels[i]

    chosen_level = __best_level(levels, weights, interval)
    return levels[chosen_level]
