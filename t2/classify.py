#!/usr/bin/python3

import argparse
import utils
import core

parser = argparse.ArgumentParser(description="Classify some data")

mtlxcg = parser.add_mutually_exclusive_group()
mtlxcg.add_argument("-p", "--plot", action="store_true", help="Plot the classified patterns (only works with 2D data)")
mtlxcg.add_argument("-s", "--show", action="store_true", help="Plot the classified patterns (only works with 2D data)")
parser.add_argument("-v", "--verbose", action="store_true", help="Print additional statistics")

parser.add_argument("algorithm", choices=["IB1", "IB2"], help="Classification algorithm")

dataparsers = parser.add_subparsers(help="Specify type of data to be classified", dest="data_type")
dataparsers.required = True

dataset = dataparsers.add_parser("dataset", help="Classify a given dataset")
dataset.add_argument("-i", "--input", type=str, required=True, metavar="FILE", help="Filename of the dataset")
dataset.add_argument("-c", "--category", type=int, required=True, metavar="INDEX", help="Column of the class")
dataset.add_argument("-d", "--data", type=str, metavar="FILE", help="Filename of the data to be classified")

dtstmtx = dataset.add_mutually_exclusive_group()
dtstmtx.add_argument("-e", "--test_set", type=str, metavar="FILE", help="Filename of the test set")
dtstmtx.add_argument("-s", "--split", type=float, metavar="PERCENTAGE", help="Automatically pick the given approximate percentage of the input dataset to use as the test set")

dataset.add_argument("-o", "--output", type=str, default="out", metavar="FILE", help="Save classified data as <FILE>.csv")
dataset.add_argument("-I", "--ignore", nargs="+", type=int, metavar="INDEX", help="Columns to be ignored")

#image = dataparsers.add_parser("image", help="Classify a given image")

spiral = dataparsers.add_parser("spiral", help="Classify a given spiral")
spiral.add_argument("-t", "--type", type=str, choices=["single", "double"], default="single", help="Type of spiral")
spiral.add_argument("-g", "--grid_size", type=int, default=50, help="Grid size to generate spiral (default 50)")
spiral.add_argument("-n", "--noise", type=int, default=0, help="Noise for the spiral.")
spiral.add_argument("-o", "--output", type=str, default="out", metavar="FILE", help="Save classified data as <FILE>.png")

# parser.add_argument("-C", "--compare", nargs="+", choices=["l2norm", "quadratic_mahalanobis", "linear_mahalanobis"], help="Compare with other algorithms")

def process_dataset(args):
    training_header, training_set = utils.load_csv(args.input)
    if len(training_set) == 0:
        dataset.error("Invalid input: file does not exist or is empty.")
    
    test_set = []
    data = []
    if args.split:
        test_set = core.split_data(data=training_set, percentage=args.split)
    elif args.test_set:
        test_header, test_set = utils.load_csv(args.test_set)
        if len(test_set) == 0:
            dataset.error("Invalid test set: file does not exist or is empty.")
    elif args.data:
        data_header, data = utils.load_csv(args.data)
    else:
        dataset.error("one of the arguments -d/--data -e/--test_set -s/--split is required")

    if args.ignore:
        utils.ignore_columns(training_set, args.ignore)
        utils.ignore_columns(test_set, args.ignore)
        utils.ignore_columns(data, args.ignore)
        for index in args.ignore:
            if index < args.category:
                args.category -= 1

    return (training_header, training_set, test_set, data)

if __name__ == "__main__":
    args = parser.parse_args()
    if args.data_type == "dataset":
        header, training_set, test_set, data = process_dataset(args)
        params = {
            "algorithm": args.algorithm,
            "category": args.category,
            "output": args.output,
            "verbose": args.verbose,
        }

        core.IBL(header, training_set, test_set, data, **params)
        # output = core.magic_function_to_do_all(params, training_set, test_set, data, args.category)
    else:
        print("spiral")
