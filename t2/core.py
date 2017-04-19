import sys
from math import floor
from matplotlib.colors import cnames

import classifiers as cl
from IBL import *
import imagecollector as ic
import plotter as pl
from spiral import *
import utils

allcolors = [color for color in sorted(cnames)]

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

    if test_set:
        test(classifier, test_set, **kargs)

    if data:
        return classify(classifier, data, **kargs)

    return []

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

def main(parser, args):
    try:
        training_header = []
        training_set = []
        if args.training_set:
            data = utils.load(args.training_set)
            training_header = data[0]
            training_set = data[1:]

        input_set = []
        if not args.compare and not is_mahalanobis and args.input:
            data = utils.load(args.input)
            if not args.training_set:
                training_header = data[0]
            input_set = data[1:]

        if args.slice:
            training_set = slice_data(input_set, args.slice)

        if args.ignore:
            ignore_columns(input_set, training_set, training_header, args)

        target_file = args.output

        output = []
        if not args.spiral:
            hits = 0
            fails = 0
            output.append(training_header)
            for entry in input_set:
                prepared_entry = utils.without_column(entry, args.category)
                class_value = cl.kNN(training_set, prepared_entry, distance_function, \
                                     args.category, args.k)
                output.append(prepared_entry + [class_value])
                if entry[args.category] != None:
                    if entry[args.category] == class_value:
                        hits += 1
                    else:
                        fails += 1

            utils.save(target_file, output)
            if args.verbose and hits + fails > 0:
                print("Hits: %i" % (hits))
                print("Fails: %i" % (fails))
                print("Precision: %f%%" % (100 * hits / (hits + fails)))

            if args.plot and len(training_set[0]) == 3:
                categories = list(set([x[args.category] for x in training_set]))

                pl.plot(
                    [x[:2] for x in output[1:]],
                    [x[2] for x in output[1:]],
                    [x[:2] for x in training_set],
                    [x[2] for x in training_set],
                    utils.without_column(training_header, args.category),
                    {categories[i]: allcolors[((i + 1) * 41) % len(allcolors)] for i in range(len(categories))}
                )
        else:
            neighborhood = 2 * args.grid_size + 50
            if args.spiral == "single":
                spiral = single_spiral(args.grid_size, args.noise)
                size = args.grid_size
                spiral_points = [(spiral[i][0] + size, spiral[i][1] + size, 0) \
                                 for i in range(len(spiral)) if not (i % 2)] + \
                                [(spiral[i][0] + size, spiral[i][1] + size, 1) \
                                 for i in range(len(spiral)) if (i % 2)]
            else:
                spirals = double_spiral(args.grid_size, args.noise)
                spiral_points = [(s[0] + args.grid_size, s[1] + args.grid_size, 0) for s in spirals[0]]\
                              + [(s[0] + args.grid_size, s[1] + args.grid_size, 1) for s in spirals[1]]
            
            red_points = []
            blue_points = []
            for x in range(neighborhood):
                for y in range(neighborhood):
                    entry = (x, y)
                    class_value = cl.kNN(spiral_points, entry, distance_function, 2, args.k)
                    if class_value == 0:
                        red_points.append(entry)
                    else:
                        blue_points.append(entry)

            first = [(255, 0, 0) for point in red_points]
            second = [(0, 0, 255) for point in blue_points]

            if args.save_image:
                import imagesaver
                imagesaver.show(
                    positions=red_points + blue_points,
                    colors=first + second,
                    width=neighborhood,
                    height=neighborhood,
                    path=args.output,
                    save=True
                )

            if args.plot:
                output = red_points + blue_points
                result = first + second

                pl.plot(
                    output,
                    result,
                    spiral_points[:1],
                    [(255, 0, 0) for point in spiral_points if point[2] == 0] + \
                    [(0, 0, 255) for point in spiral_points if point[2] == 1],
                    ['x', 'y'],
                    {(255, 0, 0) : 'red', (0, 0, 255) : 'blue'}
                )
    except:
       parser.print_help()
       sys.exit(0)
