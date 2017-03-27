#!/bin/python

import argparse
from core import main

parser = argparse.ArgumentParser(description='Classify some data.')

parser.add_argument('-k', type=int, default=1, help='k Nearest Neighbor classifier')
parser.add_argument('-d', '--distance', choices=['euclidean', 'hamming+', 'linear_mahalanobis', 'quadratic_mahalanobis'], help='Distance metric algorithm')
parser.add_argument('-t', '--training_set', type=str, help='Filename of the training set, must be a CSV file')
parser.add_argument('-i', '--input', type=str, help='Filename of the input to classify, must be a CSV file')
parser.add_argument('-o', '--output', type=str, default='out', help='Output file')
parser.add_argument('-c', '--category', type=int, help='Column of the class')
parser.add_argument('-I', '--ignore', action='append', type=int, help='Columns to be ignored')
parser.add_argument('-s', '--spiral', type=str, choices=['single', 'double'], help='Number of spirals')
parser.add_argument('-g', '--grid_size', type=int, help='Grid size (used for spirals only)')
parser.add_argument('-n', '--noise', type=int, default=0, help='Noise for the spiral(s).')
parser.add_argument('-v', '--verbose', action='store_true', help='Print additional statistics')
parser.add_argument('-p', '--plot', action='store_true', help='Plot the classified patterns (if 2D)')
parser.add_argument('-l', '--slice', type=float, help='Automatically pick the given approximate percentage of the input set to use as the training set')
parser.add_argument('-S', '--save_image', action='store_true', help='Save the resulting spiral as an image')
parser.add_argument('-V', '--voronoi', action='store_true', help='Plot the corresponding voronoi diagram')

args = parser.parse_args()
main(parser, args)
