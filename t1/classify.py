#!/bin/python

import argparse
import sys
from math import floor, sqrt
from matplotlib.colors import cnames

import classifiers as cl
import utils
from spiral import *

parser = argparse.ArgumentParser(description='Classify some data.')

parser.add_argument('-k', type=int, default=1, help='k Nearest Neighbor classifier')
parser.add_argument('-d', '--distance', required=True, choices=['euclidian', 'hamming+', 'linear_mahalanobis', 'quadratic_mahalanobis'], help='Distance metric algorithm')
parser.add_argument('-t', '--training_set', type=str, help='Filename of the training set, must be a CSV file')
parser.add_argument('-i', '--input', type=str, help='Filename of the input to classify, must be a CSV file')
parser.add_argument('-o', '--output', required=True, type=str, default='out', help='Output file')
parser.add_argument('-c', '--category', type=int, help='Column of the class')
parser.add_argument('-I', '--ignore', action='append', type=int, help='Columns to be ignored')
parser.add_argument('-s', '--spiral', type=str, choices=['single', 'double'], help='Number of spirals')
parser.add_argument('-g', '--grid_size', type=int, help='Grid size (used for spirals only)')
parser.add_argument('-n', '--noise', type=int, default=0, help='Noise for the spiral(s).')
parser.add_argument('-v', '--verbose', action='store_true', help='Print additional statistics')
parser.add_argument('-p', '--plot', action='store_true', help='Plot the classified patterns (if 2D)')
parser.add_argument('-l', '--slice', type=float, help='Automatically pick the given approximate percentage of the input set to use as the training set')
parser.add_argument('-S', '--save_image', action='store_true', help='Save the resulting spiral as an image')

args = parser.parse_args()

# TODO: validate the input flags if it's mahalanobis
if not args.output or\
  (not args.spiral and args.category == None) or\
  (not args.spiral and not args.input) or\
  (not args.spiral and args.noise) or\
  (args.spiral and (args.training_set or args.input)) or\
  (args.spiral and not args.grid_size) or\
  (args.input and not args.training_set and not args.slice) or\
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
if args.distance == 'euclidian':
    distance_function = cl.euclidian_dist
elif args.distance == 'hamming+':
    distance_function = cl.hamming_dist

if args.slice:
    num_picked_entries = floor(len(input_set) * args.slice / 100)
    num_entries = len(input_set)
    i = 0
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

if args.ignore:
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

target_file = args.output

output = []
if args.distance == 'linear_mahalanobis' or args.distance == 'quadratic_mahalanobis':
    # TODO: show an interactable plot and change the following
    # variables accordingly. Both should be (r, g, b) lists
    training_set = []
    pixels = []

    # TODO: find a better name for this function
    def deal_with_it(pixel, distance):
        # TODO: do something with distance (e.g color the pixel
        # according to the distance)
        print(pixel, "-> distance =", distance)

    if args.distance == 'linear_mahalanobis':
        utils.linear_mahalanobis(training_set, pixels, deal_with_it)
    else:
        utils.quadratic_mahalanobis(training_set, pixels, deal_with_it)

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