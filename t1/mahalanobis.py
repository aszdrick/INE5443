#!/bin/python

import argparse
import os

parser = argparse.ArgumentParser(description="Applies the mahalanobis distance to a given image.")

parser.add_argument("-i", "--input", required=True, type=str, help="Filename of the base image")
parser.add_argument("-q", "--quadratic", action="store_true", help="Use quadratic mahalanobis instead of linear")
parser.add_argument("-o", "--output", type=str, help="Output file")
parser.add_argument("-c", "--compare", nargs='+', choices=['l2norm', 'quadratic_mahalanobis', 'linear_mahalanobis'], help="Compare different algorithms")

args = parser.parse_args()

command = "python3 classify.py --input " + args.input
if args.compare:
    command += " --compare " + " ".join(args.compare)
else:
    if args.quadratic:
        command += " --distance quadratic_mahalanobis"
    else:
        command += " --distance linear_mahalanobis"

if args.output:
    command += " --output %s --save_image" % (args.output)

os.system(command)
