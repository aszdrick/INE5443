#!/bin/python

from math import floor
from utils import empty

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
parser.add_argument('-v', '--verbose', action='store_true', help='Print additional statistics')
parser.add_argument('-p', '--plot', action='store_true', help='Plot the classified patterns (if 2D)')
parser.add_argument('-l', '--slice', type=float, help='Automatically pick the given approximate percentage of the input set to use as the training set')

args = parser.parse_args()

if not args.distance or\
   not args.category or\
   empty(args.output) or\
  (empty(args.spiral) and empty(args.input)) or\
  (not empty(args.spiral) and (not empty(args.training_set) or not empty(args.input))) or\
  (not empty(args.spiral) and empty(args.grid_size)) or\
  (not empty(args.input) and empty(args.training_set) and empty(args.slice)) or\
  (not empty(args.training_set) and not empty(args.slice)):

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

    offset = 0
    for i in range(num_entries):
        if i in picked_indexes:
            del input_set[i - offset]
            offset += 1

target_file = args.output;

output = []
if not args.spiral:
    output.append(training_header)
    for entry in input_set:
        prepared_entry = utils.without_column(entry, args.category)
        class_value = cl.kNN(training_set, prepared_entry, distance_function, \
                             args.category, args.k)
        output.append(prepared_entry + [class_value])

    utils.save(target_file, output)
