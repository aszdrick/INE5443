import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import math
from sys import maxsize

linewidth = 1.5
xoffset = 0.5
color = "k"
xgrid = False

# Recursively plots each cluster of dendrogram.
def __visit_cluster(tree, leafs, xticks, counter = 0):
    if isinstance(tree, tuple):
        bottom_left = __visit_cluster(tree[0], leafs, xticks)
        bottom_right = __visit_cluster(tree[1], leafs, xticks)
    else:
        leafs.append(tree)
        return (0, len(leafs) - 1)

    plt.plot(
        [bottom_left[0], tree[2], tree[2], bottom_right[0]],
        [bottom_left[1], bottom_left[1], bottom_right[1], bottom_right[1]],
        color,
        linewidth = linewidth)

    if tree[2] not in xticks:
        xticks.append(tree[2])

    return (tree[2], (bottom_left[1] + bottom_right[1]) / 2)

# Plots a single tree in format of dendrogram.
def __plot_tree(tree):
    leafs = []
    xticks = [0]

    __visit_cluster(tree, leafs, xticks)

    return (leafs, xticks)

# Plots a forest in format of dendrogram.
def __plot_subtrees(trees):
    leafs = []
    xticks = [0]

    for tree in trees:
        if isinstance(tree, tuple):
            __visit_cluster(tree, leafs, xticks)
        else:
            leafs.append(tree)
    return (leafs, xticks)

# Plot dendrograms, either a single tree or forest.
def plot(data):
    if isinstance(data, list):
        (leafs, xticks) = __plot_subtrees(data)
    else:
        (leafs, xticks) = __plot_tree(data)

    ml = MultipleLocator(xoffset)
    ax = plt.gca()
    ax.set_yticks(list(range(len(leafs))))
    ax.set_yticklabels(leafs)
    ax.set_xlim(0, max(xticks) + xoffset)
    ax.set_xticks(xticks)
    ax.xaxis.set_minor_locator(ml)
    ax.yaxis.set_tick_params(width = linewidth)
    
    if xgrid:
        ax.xaxis.grid()

    return plt.gcf()

# class to encapsulate the fitness function, i.e.,
# how good is a level (or derivative level) using the specified
# set of weights and interval.
class LevelEvaluator:
    # weights = (average weight, standard deviation weight)
    # interval = (min classes, max classes)
    # min_avg = minimum average found in analysed levels
    # min_sd = minimum standard deviation found in analysed levels
    def __init__(self, weights, interval, min_avg, min_sd):
        self.weights = weights
        self.interval = interval
        self.min_avg = min_avg
        self.min_sd = min_sd

    # Evaluate how good a level (or derivative level) is.
    def __call__(self, values):
        vs = []
        # Normalizes average and standard deviation using the
        # minimum values.
        vs.append(self.min_avg / (values[0] + 1))
        vs.append(self.min_sd / (values[1] + 1))
        # Multiply each value by its weight and sum all
        return sum([w * v for w, v in zip(self.weights, vs)])

# Returns all leafs. Each leaf is a tuple of dataset.
def __leafs_of(tree):
    leafs = []
    if isinstance(tree, tuple):
        leafs += __leafs_of(tree[0])
        leafs += __leafs_of(tree[1])
    else:
        leafs.append(tree)
    return leafs

# Given a list of trees, each tree is splitted in its children.
def __split_trees(trees):
    subtrees = []
    for st in trees:
        if isinstance(st, tuple):
            subtrees.append(st[0])
            subtrees.append(st[1])
        else:
            subtrees.append(st)
    return subtrees

# Given a cluster, returns its distance.
# Needed to handle cases of unitary cluster, where distance is 0.
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
        subtrees = __split_trees(subtrees)

    return (marked_subtrees, min_avg, min_sd)

def cut(tree, weights, interval):
    subtree_counter = 1
    subtrees = [tree]
    level = 1

    while len(subtrees) <= interval[0] / 2:
        new_subtrees = []
        subtrees = __split_trees(subtrees)
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

    return marked_subtrees[best_subtree]

def get_clusters(trees):
    clusters = {}
    for i, tree in enumerate(trees):
        for instance in __leafs_of(tree):
            clusters[instance] = i
    return clusters

def __levelize(tree, levels, counter = 0):
    if isinstance(tree, tuple):
        __levelize(tree[0], levels, counter + 1)
        __levelize(tree[1], levels, counter + 1)
    if counter not in levels.keys():
        levels[counter] = []
    levels[counter].append(tree)

def __levels_of(tree, leafs):
    leafs_set = set(leafs)
    levels = {}
    __levelize(tree, levels)
    for (i, level) in levels.items():
        level_leafs = set()
        for t in level:
            level_leafs |= set(__leafs_of(t))
        diff = leafs_set - level_leafs
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
    leafs = __leafs_of(tree)
    levels = __levels_of(tree, leafs)
    max_level = max(levels.keys())

    for i in range(max_level + 1):
        level_leafs = []
        for tup in levels[i]:
            level_leafs += __leafs_of(tup)
        length = len(levels[i])
        if length > interval[1] or length < interval[0]:
            del levels[i]

    chosen_level = __best_level(levels, weights, interval)
    return levels[chosen_level]
