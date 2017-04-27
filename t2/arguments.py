import argparse

common = argparse.ArgumentParser(add_help=False)
common.add_argument("-s", "--show", action="store_true", help="Show the classified patterns (only works with 2D data)")

dataparsers = common.add_subparsers(help="Type of data to be classified", dest="data_type")
dataparsers.required = True

dataset = dataparsers.add_parser("dataset")
dataset.add_argument("-i", "--input", type=str, required=True, metavar="FILE", help="Filename of the dataset")
dataset.add_argument("-c", "--category", type=int, required=True, metavar="INDEX", help="Column of the class")
dataset.add_argument("-d", "--data", type=str, metavar="FILE", help="Filename of the data to be classified")

dtstmtx = dataset.add_mutually_exclusive_group()
dtstmtx.add_argument("-e", "--test_set", type=str, metavar="FILE", help="Filename of the test set")
dtstmtx.add_argument("-s", "--split", type=float, metavar="PERCENTAGE", help="Automatically pick the given approximate percentage of the input dataset to use as the test set")

dataset.add_argument("-o", "--output", type=str, default="out", metavar="FILE", help="Save classified data as <FILE>.csv")
dataset.add_argument("-I", "--ignore", nargs="+", type=int, metavar="INDEX", help="Columns to be ignored")

spiral = dataparsers.add_parser("spiral")
spiral.add_argument("-t", "--spiral_type", type=str, choices=["single", "double"], default="single", help="Type of spiral")
spiral.add_argument("-g", "--grid_size", type=int, default=50, help="Grid size to generate spiral (default 50)")
spiral.add_argument("-n", "--noise", type=int, default=0, help="Noise for the spiral.")
spiral.add_argument("-o", "--output", type=str, default="out", metavar="FILE", help="Save classified data as <FILE>.png")

zargs = argparse.ArgumentParser(add_help=False)
zargs.add_argument("-zpa", "--z_precision_acceptance", type=float, default=0.9, metavar="FLOAT", help="z-Value for Acceptance Precision Interval")
zargs.add_argument("-zpd", "--z_precision_dropping", type=float, default=0.75, metavar="FLOAT", help="z-Value for Dropping Precision Interval")
zargs.add_argument("-zfa", "--z_frequency_acceptance", type=float, default=0.9, metavar="FLOAT", help="z-Value for Acceptance Frquency Interval")
zargs.add_argument("-zfd", "--z_frequency_dropping", type=float, default=0.75, metavar="FLOAT", help="z-Value for Dropping Frquency Interval")

kdargs = argparse.ArgumentParser(add_help=False)
kdargs.add_argument("-k", "--knn", type=int, default=1, metavar="NUMBER", help="Use the k nearest neighbors to classify data")

parser = argparse.ArgumentParser(description="Instance-based Learning classificator")

algparsers = parser.add_subparsers(help="Classification algorithm", dest="algorithm")
algparsers.required = True

ib1 = algparsers.add_parser("IB1", parents=[common, kdargs])
ib2 = algparsers.add_parser("IB2", parents=[common, kdargs])
ib3 = algparsers.add_parser("IB3", parents=[common, kdargs, zargs])
ib4 = algparsers.add_parser("IB4", parents=[common, zargs])
