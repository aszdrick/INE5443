#!/bin/python

from math import floor
from spiral import *

import argparse
import classifiers as cl
import sys
import utils

parser = argparse.ArgumentParser(description='Classify some data.')

parser.add_argument('-k', type=int, default=1, help='k Nearest Neighbor classifier')
parser.add_argument('-d', '--distance', choices=['euclidian', 'hamming+'], help='Distance metric algorithm')
parser.add_argument('-t', '--training_set', type=str, help='Filename of the training set, must be a CSV file')
parser.add_argument('-i', '--input', type=str, help='Filename of the input to classify, must be a CSV file')
parser.add_argument('-o', '--output', type=str, help='Output file')
parser.add_argument('-c', '--category', type=int, help='Column of the class')
parser.add_argument('-I', '--ignore', action='append', type=int, help='Columns to be ignored')
parser.add_argument('-s', '--spiral', type=str, choices=['single', 'double'], help='Number of spirals')
parser.add_argument('-g', '--grid_size', type=int, help='Grid size (used for spirals only)')
parser.add_argument('-n', '--noise', type=int, default=0, help='Noise for the spiral(s).')
parser.add_argument('-v', '--verbose', action='store_true', help='Print additional statistics')
parser.add_argument('-p', '--plot', action='store_true', help='Plot the classified patterns (if 2D)')
parser.add_argument('-l', '--slice', type=float, help='Automatically pick the given approximate percentage of the input set to use as the training set')

args = parser.parse_args()

if not args.distance or\
   not args.category or\
   not args.output or\
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
else:
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

category_offset = 0
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
            category_offset += 1
        del training_header[index]

target_file = args.output

output = []
if not args.spiral:
    output.append(training_header)
    for entry in input_set:
        prepared_entry = utils.without_column(entry, args.category - category_offset)
        class_value = cl.kNN(training_set, prepared_entry, distance_function, \
                             args.category - category_offset, args.k)
        output.append(prepared_entry + [class_value])

    utils.save(target_file, output)
else:
    if args.spiral == "single":
        single_spiral(args.grid_size, args.noise)
    else:
        double_spiral(args.grid_size, args.noise)
