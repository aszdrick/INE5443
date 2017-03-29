#!/bin/python

import argparse
import os

parser = argparse.ArgumentParser(description="Applies the L2-norm to a given image.")

parser.add_argument("-i", "--input", required=True, type=str, help="Filename of the base image")
parser.add_argument("-o", "--output", type=str, help="Output file")

args = parser.parse_args()

command = "python3 classify.py --input " + args.input + " --distance l2norm"
if args.output:
    command += " --output %s --save_image" % (args.output)

os.system(command)
