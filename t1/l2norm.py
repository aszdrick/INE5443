#!/bin/python3

import argparse
import os

parser = argparse.ArgumentParser(description="Applies the L2-norm to a given image.")

parser.add_argument("-i", "--input", required=True, type=str, help="Filename of the base image")
parser.add_argument("-o", "--output", type=str, help="Output file")
parser.add_argument("-c", "--compare", nargs='+', choices=['l2norm', 'quadratic_mahalanobis', 'linear_mahalanobis'], help="Compare different algorithms")

args = parser.parse_args()

command = "python3 classify.py --input " + args.input + " --distance l2norm"
if args.compare:
    command += " --compare " + " ".join(args.compare)

if args.output:
    command += " --output %s --save_image" % (args.output)

os.system(command)
