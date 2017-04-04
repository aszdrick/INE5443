import sys
from math import floor
from matplotlib.colors import cnames

import classifiers as cl
import imagecollector as ic
import utils
import plotter as pl
from spiral import *

allcolors = [color for color in sorted(cnames)]

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

def process_image_distances(filename, args, callbacks):
    training_set, pixels, width, height = ic.collect(filename)

    if (not len(training_set) or not len(pixels)):
        print("Error: empty image and/or training set")
        return

    positions = []
    colors = []
    def process_pixel_distance(position, pixel_color, distance):
        positions.append(position)
        colors.append((int(distance),) * 3)

    i = 0
    import imagesaver
    for callback in callbacks:
        callback(training_set, pixels, process_pixel_distance)

        print("Displaying the resulting image for " + args.compare[i])
        imagesaver.show(
            positions=positions,
            colors=colors,
            width=width,
            height=height,
            path=args.output + "_%s" % (args.compare[i]),
            save=args.save_image
        )
        i += 1

def main(parser, args):
    is_mahalanobis = (args.distance == 'linear_mahalanobis' or args.distance == 'quadratic_mahalanobis')

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
            if args.distance == 'linear_mahalanobis':
                fn = cl.linear_mahalanobis
            else:
                fn = cl.quadratic_mahalanobis

            process_image_distances(args.input, args, [fn])

        elif args.compare:
            fn_list = []
            callback_mapping = {
                'linear_mahalanobis': cl.linear_mahalanobis,
                'quadratic_mahalanobis': cl.quadratic_mahalanobis,
                'l2norm': cl.l2norm
            }

            for option in args.compare:
                fn_list.append(callback_mapping[option])

            process_image_distances(args.input, args, fn_list)

        elif args.voronoi:
            from scipy.spatial import Voronoi
            show_legend = True
            if args.spiral:
                args.category = 2
                training_header = ["x", "y"]
                if args.spiral == "single":
                    show_legend = False
                    spiral = single_spiral(args.grid_size, args.noise)
                    training_set = []
                    size = args.grid_size
                    for i in range(size):
                        training_set.append((spiral[i][0], spiral[i][1], i))
                else:
                    spirals = double_spiral(args.grid_size, args.noise)
                    training_set = [(s[0] + args.grid_size, s[1] + args.grid_size, 0) for s in spirals[0]]\
                                 + [(s[0] + args.grid_size, s[1] + args.grid_size, 1) for s in spirals[1]]
            elif len(training_set) == 0:
                training_set = input_set

            points = [(p[0], p[1]) for p in training_set]
            voronoi = Voronoi(points)
            categories = [p[2] for p in training_set]
            categories_pure = list(set(categories))
            num_cat = len(categories_pure)
            colors = {categories_pure[i]: allcolors[((i + 1) * 41) % len(allcolors)] for i in range(num_cat)}

            pl.plot_voronoi(
                voronoi,
                points,
                categories,
                utils.without_column(training_header, args.category),
                colors,
                show_legend
            )

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
