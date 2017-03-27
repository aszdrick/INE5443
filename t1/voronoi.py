#!/bin/python

import argparse
import os
import sys

parser = argparse.ArgumentParser(description='Displays a voronoi diagram for a given dataset.')

parser.add_argument('-i', '--input', type=str, help='Filename of the input to classify, must be a CSV file')
parser.add_argument('-c', '--category', type=int, help='Column of the class')
parser.add_argument('-s', '--singlespiral', type=int, help='Single spiral with a given grid size')
parser.add_argument('-d', '--doublespiral', type=int, help='Double spiral with a given grid size')
parser.add_argument('-n', '--noise', type=int, default=0, help='Noise for the spiral(s).')

args = parser.parse_args()

command = "python3 classify.py --voronoi"
if args.input and args.category:
	command += " --input " + args.input
	command += " --category " + str(args.category)
elif args.singlespiral or args.doublespiral:
	command += " --spiral "
	if args.singlespiral:
		command += "single"
	else:
		command += "double"
	if args.noise:
		command += " --noise " + args.noise
else:
	parser.print_help()
	sys.exit(0)

os.system(command)
