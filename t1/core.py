import sys
from math import floor
from matplotlib.colors import cnames

import classifiers as cl
import utils
from spiral import *

def slice_data(input_set, slice_percentage):
    num_picked_entries = floor(len(input_set) * slice_percentage / 100)
    num_entries = len(input_set)
    i = 0
    training_set = []
    picked_indexes = set()
    while len(training_set) < num_picked_entries:
        if i >= num_entries:
            i = 1
        training_set.append(input_set[i])
        picked_indexes.add(i)
        i += 2

    for i in range(num_entries - 1, -1, -1):
        if i in picked_indexes:
            del input_set[i]
    return training_set

def ignore_columns(input_set, training_set, training_header, args):
    args.ignore.sort(reverse=True)
    for entry in training_set:
        for index in args.ignore:
            del entry[index]

    for entry in input_set:
        for index in args.ignore:
            del entry[index]

    for index in args.ignore:
        if index < args.category:
            args.category -= 1
        del training_header[index]

def mahalanobis(mahalanobis_type, filename):
    # TODO: show an interactive plot and change the following
    # variables accordingly. Both should be (r, g, b) lists
    training_set = []
    pixels = []

    if (len(training_set) == 0 or len(pixels) == 0):
        print("Error: empty image and/or training set")
        return

    # TODO: find a better name for this function
    def deal_with_it(pixel, distance):
        # TODO: do something with distance (e.g color the pixel
        # according to the distance)
        print(pixel, "-> distance =", distance)

    if mahalanobis_type == 'linear_mahalanobis':
        cl.linear_mahalanobis(training_set, pixels, deal_with_it)
    else:
        cl.quadratic_mahalanobis(training_set, pixels, deal_with_it)

def main(parser, args):
    is_mahalanobis = (args.distance == 'linear_mahalanobis' or args.distance == 'quadratic_mahalanobis')
    if not args.output or\
      (not args.spiral and not is_mahalanobis and args.category == None) or\
      (not args.spiral and not args.input) or\
      (not args.spiral and args.noise) or\
      (args.spiral and (args.training_set or args.input)) or\
      (args.spiral and not args.grid_size) or\
      (args.spiral and args.save_image and not args.output) or\
      (not args.voronoi and not is_mahalanobis and args.input and not args.training_set and not args.slice) or\
      (args.training_set and args.slice):

       parser.print_help()
       sys.exit(0)

    training_header = []
    training_set = []
    if args.training_set:
        data = utils.load(args.training_set)
        training_header = data[0]
        training_set = data[1:]

    input_set = []
    if args.input:
        data = utils.load(args.input)
        if not args.training_set:
            training_header = data[0]
        input_set = data[1:]

    distance_function = None
    if args.distance == 'euclidean':
        distance_function = cl.euclidian_dist
    elif args.distance == 'hamming+':
        distance_function = cl.hamming_dist

    if args.slice:
        training_set = slice_data(input_set, args.slice)

    if args.ignore:
        ignore_columns(input_set, training_set, training_header, args)

    target_file = args.output

    output = []
    if is_mahalanobis:
        mahalanobis(args.distance, args.input)
    elif args.voronoi:
        from scipy.spatial import Voronoi, voronoi_plot_2d
        if args.spiral:
            if args.spiral == "single":
                spiral = single_spiral(args.grid_size, args.noise)
                size = args.grid_size
                training_set = [(spiral[i][0] + size, spiral[i][1] + size, 0) \
                                 for i in range(len(spiral)) if not (i % 2)] + \
                                [(spiral[i][0] + size, spiral[i][1] + size, 1) \
                                 for i in range(len(spiral)) if (i % 2)]
            else:
                spirals = double_spiral(args.grid_size, args.noise)
                training_set = [(s[0] + args.grid_size, s[1] + args.grid_size, 0) for s in spirals[0]]\
                             + [(s[0] + args.grid_size, s[1] + args.grid_size, 1) for s in spirals[1]]
        elif len(training_set) == 0:
            training_set = input_set

        points = [(p[0], p[1]) for p in training_set]
        voronoi = Voronoi(points)
        voronoi_plot_2d(voronoi)
        plt.show()

    elif not args.spiral:
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
            import plotter as pl
            
            allcolors = [color for color in sorted(cnames)]
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
                class_value = cl.kNN(spiral_points, entry, distance_function, \
                                     2, args.k)
                if class_value == 0:
                    red_points.append(entry)
                else:
                    blue_points.append(entry)

        first = [(255, 0, 0) for point in red_points]
        second = [(0, 0, 255) for point in blue_points]

        if args.save_image:
            import imagesaver
            imagesaver.save(red_points + blue_points, first + second, neighborhood, args.output)

        if args.plot:
            import plotter as pl

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
