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

    # ml = MultipleLocator(xoffset)
    ax = plt.gca()
    ax.set_yticks(list(range(len(leafs))))
    ax.set_yticklabels(leafs)
    ax.set_xlim(0, max(xticks) + xoffset)
    ax.set_xticks(xticks)
    # ax.xaxis.set_minor_locator(ml)
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

# Gather statistics about the level, i.e., distances, average and
# standard deviation of distances.
def __statistics(subtrees):
    distances = list(map(__distance_of, subtrees))
    avg = sum(distances) / len(distances)
    sd = math.sqrt(sum(map(lambda x: (x - avg) ** 2, distances)))
    return (avg, sd, distances)

# Gather information of each level and its derivative levels.
# A derivative level is a level with at least one of its clusters splitted in
# its children. For complete analysis, it would be required to combine all
# possible derivative levels and split more than one time. For simplicity,
# only one cluster is splitted in each derivative level and only one time.
def __gather_info(subtrees, interval, current_level):
    levels = {}
    min_avg = maxsize
    min_sd = maxsize

    while len(subtrees) <= interval[1]:
        (avg, sd, distances) = __statistics(subtrees)
        # Keep mininum average and standard deviation updated
        if avg < min_avg:
            min_avg = avg
        if sd < min_sd:
            min_sd = sd
        # Each level has as key its avg, sd, current level and derivation. 
        levels[(avg, sd, current_level, 0)] = subtrees
        # if it is possible to derivate the level, since it adds one cluster
        # in size...
        if len(subtrees) < interval[1]:
            # For each distance, checks if is worth derivate it, i.e.,
            # if the distance is above the average.
            for (i, distance) in enumerate(distances):
                if distance > avg:
                    diff = distance - avg
                    chosen = subtrees[i]
                    d0 = __distance_of(chosen[0])
                    d1 = __distance_of(chosen[1])
                    # If one of the new clusters are more distant from average,
                    # does not count this derivation.
                    if abs(d0 - avg) > diff or abs(d1 - avg) > diff:
                        continue
                    # Mount derivation
                    derivation = subtrees[:i]
                    derivation.append(chosen[0])
                    derivation.append(chosen[1])
                    derivation += subtrees[i+1:]
                    # Do the same analysis for the derivation, storing in levels
                    # as well.
                    (avg, sd, d) = __statistics(derivation)
                    if avg < min_avg:
                        min_avg = avg
                    if sd < min_sd:
                        min_sd = sd
                    levels[(avg, sd, current_level, i)] = derivation
        # Descend one level
        subtrees = __split_trees(subtrees)
        current_level += 1

    return (levels, min_avg, min_sd)

# Cut a tree in subtrees according to weights and interval specified.
def cut(tree, weights, interval):
    subtree_counter = 1
    subtrees = [tree]
    level = 1

    # Aproximate the division of tree to the minimum number of clusters,
    # since it is useless to analyse this levels.
    while len(subtrees) <= interval[0] / 2:
        new_subtrees = []
        subtrees = __split_trees(subtrees)
        subtree_counter = len(subtrees)
        level += 1

    # Analyse all other levels and derivatives.
    (levels, min_avg, min_sd) = __gather_info(subtrees, interval, level)
    
    # Create a evaluator to classify how good a level is.
    evaluator = LevelEvaluator(weights, interval, min_avg, min_sd)
    best_score = 0
    best_level = None

    # Discover which level is better.
    for key in levels:
        score = evaluator(key[0:2])
        if score > best_score:
            best_level = key

    return levels[best_level]

# Returns a map of leaf -> cluster id.
# As leaf identifies the instance, it can be used as a map
# of instance -> class.
def get_clusters(trees):
    clusters = {}
    for i, tree in enumerate(trees):
        for instance in __leafs_of(tree):
            clusters[instance] = i
    return clusters

# -----------------------------------------------------------------------------
# The functions below are not used. It is an old version of cut.

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

def pure_cut(tree, weights, interval):
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
