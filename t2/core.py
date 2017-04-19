import itertools
import sys
from math import floor
from matplotlib.colors import cnames

import classifiers as cl
from IBL import *
import image
import plotter as pl
from spiral import *
import utils

# allcolors = [color for color in sorted(cnames)]
allcolors = [color for key, color in sorted(cnames.items())]

def plot(training_set, test_set, data, header, category):
    categories = list(set([x[category] for x in training_set]))
    pl.plot(
        training_set,
        test_set,
        data,
        utils.without_column(header, category),
        {categories[i]: allcolors[((i + 1) * 41) % len(allcolors)] for i in range(len(categories))}
    )

def save_spirals(training_set, output, filename, size, show):
    colors = [utils.hex_to_tuple(x[2]) for x in output[1]]

    image.save(
        positions=[(x[0], x[1]) for x in training_set],
        colors=[utils.hex_to_tuple(x[2]) for x in training_set],
        width=size,
        height=size,
        path=filename + "_original.png",
        show=show
    )

    image.save(
        positions=[(x[0], x[1]) for x in output[1]],
        colors=colors,
        width=size,
        height=size,
        path=filename + ".png",
        show=show
    )

def process_spiral(spiral_type, size, noise):
    half = size / 2
    spiral = []
    remove = set()
    if spiral_type == "single":
        color = lambda i: allcolors[((i + 1) * 41) % len(allcolors)]
        s = single_spiral(size, noise)
        remove = set(s)
        spiral = [(s[i][0] + half, s[i][1] + half, color(i)) for i in range(len(s))]
    else:
        s = double_spiral(size, noise)
        remove = set(s[0]) | set(s[1])
        spiral = [(s[0][i][0] + half, s[0][i][1] + half, "#FF0000") for i in range(len(s[0]))]
        spiral += [(s[1][i][0] + half, s[1][i][1] + half, "#0000FF") for i in range(len(s[1]))]

    data = set(itertools.product(range(size), repeat=2)) - remove
    data = [[t[0], t[1], None] for t in data]

    return (["x", "y", "color"], sorted(spiral), sorted(data), size)

def test(classifier, test_set, **kargs):
    hits = 0
    fails = 0
    for entry in test_set:
        chosen = classifier.classify(entry, kargs["category"])
        if chosen == entry[kargs["category"]]:
            hits += 1
        else:
            fails += 1
        entry[kargs["category"]] = chosen

    print("---------------------")
    print("Test statistics:")
    print("Hits: %i" % (hits))
    print("Fails: %i" % (fails))
    print("Precision: %f%%" % (100 * hits / (hits + fails)))
    return test_set

def classify(classifier, data, **kargs):
    output = []
    for entry in data:
        chosen = classifier.classify(entry, kargs["category"])
        entry[kargs["category"]] = chosen
        output.append(entry)
    return output;

def IBL(training_set, test_set, data, **kargs):
    algorithms = {
        "IB1": IBL1,
        "IB2": IBL2
    }

    classifier = algorithms[kargs["algorithm"]](training_set, kargs["category"])

    print("Training statistics:")
    print("Hits: %i" % (classifier.hits))
    print("Fails: %i" % (classifier.fails))
    print("Precision: %f%%" % (100 * classifier.hits / (classifier.hits + classifier.fails)))

    output = [[], []]
    if test_set:
        output[0] = test(classifier, test_set, **kargs)

    if data:
        output[1] = classify(classifier, data, **kargs)

    return output

def split_data(data, percentage):
    num_picked_entries = floor(len(data) * percentage / 100)
    num_entries = len(data)
    i = 0
    second_part = []
    picked_indexes = set()
    while len(second_part) < num_picked_entries:
        if i >= num_entries:
            i = 1
        second_part.append(data[i])
        picked_indexes.add(i)
        i += 2

    for i in range(num_entries - 1, -1, -1):
        if i in picked_indexes:
            del data[i]
    return second_part
