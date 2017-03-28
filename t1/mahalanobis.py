#!/bin/python

import argparse
import os

parser = argparse.ArgumentParser(description='Applies the mahalanobis distance to a given image.')

parser.add_argument('-i', '--input', required=True, type=str, help='Filename of the base image')
parser.add_argument('-q', '--quadratic', action='store_true', help='Use quadratic mahalanobis instead of linear')

args = parser.parse_args()

command = "python3 classify.py --input " + args.input
if args.quadratic:
	command += " --distance quadratic_mahalanobis"
else:
	command += " --distance linear_mahalanobis"

os.system(command)
