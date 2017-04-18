#!/usr/bin/python3

import argparse
#from core import main

parser = argparse.ArgumentParser(description="Classify some data")
parser.add_argument("-v", "--verbose", action="store_true", help="Print additional statistics")

subparsers = parser.add_subparsers(help="Specify type of data to be classified")

dataset = subparsers.add_parser("dataset", help="Classify a given dataset")

dgroup0 = dataset.add_argument_group("splited input files (CSV only)")
dgroup0.add_argument("-t", "--training_set", type=str, help="Filename of the training set")
dg0exc0 = dgroup0.add_mutually_exclusive_group(required=True)
dg0exc0.add_argument("-e", "--test_set", type=str, help="Filename of the test set")
dg0exc0.add_argument("-d", "--data", type=str, help="Filename of the data to be classified")

dgroup1 = dataset.add_argument_group("single input file (CSV only)")
dgroup1.add_argument("-l", "--slice", type=float, help="Automatically pick the given approximate percentage of the input set to use as the training set")
dgroup1.add_argument("-i", "--input", type=str, help="Filename of the input to classify")

dataset.add_argument("-o", "--output", type=str, default="out.csv", help="Output file")

image = subparsers.add_parser("image", help="Classify a given image")

spiral = subparsers.add_parser("spiral", help="Classify a given spiral")
spiral.add_argument("-t", "--type", type=str, choices=["single", "double"], default="single", help="Number of spirals")
spiral.add_argument("-g", "--grid_size", type=int, default=50, help="Grid size to generate spiral (default 50)")


# spirals = parser.add_argument_group("Spirals")

# parser.add_argument("-k", type=int, default=1, help="k Nearest Neighbor classifier")
# parser.add_argument("-i", "--input", type=str, help="Filename of the input to classify, must be a CSV file")
# parser.add_argument("-o", "--output", type=str, default="out", help="Output file")
# parser.add_argument("-c", "--category", type=int, help="Column of the class")
# parser.add_argument("-I", "--ignore", action="append", type=int, help="Columns to be ignored")
# parser.add_argument("-n", "--noise", type=int, default=0, help="Noise for the spiral(s).")
# parser.add_argument("-p", "--plot", action="store_true", help="Plot the classified patterns (if 2D)")
# parser.add_argument("-S", "--save_image", action="store_true", help="Save the resulting spiral as an image")
# parser.add_argument("-C", "--compare", nargs="+", choices=["l2norm", "quadratic_mahalanobis", "linear_mahalanobis"], help="Compare with other algorithms")

args = parser.parse_args()
print(args)
# main(parser, args)
