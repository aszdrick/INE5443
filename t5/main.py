#!/usr/bin/python3

from arguments import *
import math
import utils

def analyse(data):
    num_columns = len(data[0])
    sums = [0] * num_columns
    num_rows = len(data)
    for row in data:
        for index in range(len(row)):
            value = row[index]
            sums[index] += value

    averages = [0] * num_columns
    for index in range(num_columns):
        averages[index] = sums[index] / num_rows

    squareDevs = [0] * num_columns
    for row in data:
        for index in range(len(row)):
            squareDevs[index] += (row[index] - averages[index]) ** 2

    stdevs = [0] * num_columns
    for index in range(num_columns):
        stdevs[index] = math.sqrt(squareDevs[index] / (num_rows - 1))

    return (averages, stdevs)

def standardize(data):
    (averages, stdevs) = analyse(data)
    print(averages)
    print(stdevs)
    for row in data:
        for index in range(len(row)):
            row[index] = (row[index] - averages[index]) / stdevs[index]

    return data

def main():
    args = parser.parse_args()
    header, dataset = utils.load_csv(args.input)
    if len(dataset) == 0:
        parser.error("Invalid input: file does not exist or is empty.")

    dataset = standardize(dataset)

if __name__ == "__main__":
    main()
