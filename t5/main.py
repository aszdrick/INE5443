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
    for row in data:
        for index in range(len(row)):
            row[index] = (row[index] - averages[index]) / stdevs[index]

    return data

def tuple_dist(first, second):
    result = 0
    for index in range(len(first)):
        result += (first[index] - second[index]) ** 2

    return math.sqrt(result)

def cluster_dist(first, second, linkage):
    min_dist = float("inf")
    max_dist = -1
    avg_dist = 0
    for first_row in first:
        for second_row in second:
            dist = tuple_dist(first_row, second_row)
            avg_dist += dist
            if dist < min_dist:
                min_dist = dist
            if dist > max_dist:
                max_dist = dist

    avg_dist /= len(first)

    if linkage == "complete":
        return max_dist
    else if linkage == "nearest":
        return min_dist
    else if linkage == "average":
        return avg_dist

    return None

def clusterize(dataset, linkage):
    clusters = []
    # Each cluster initially contains only the instance
    for row in dataset:
        clusters.append([row])

    num_clusters = len(clusters)
    dist_matrix = [[0] * num_clusters] * num_clusters
    for first in range(num_clusters):
        for second in range(num_clusters):
            a = clusters[first]
            b = clusters[second]
            dist_matrix[first][second] = cluster_dist(a, b, linkage)

    print(dist_matrix)

def main():
    args = parser.parse_args()
    header, dataset = utils.load_csv(args.input)
    if len(dataset) == 0:
        parser.error("Invalid input: file does not exist or is empty.")

    dataset = standardize(dataset)
    dataset = clusterize(dataset, args.linkage)

if __name__ == "__main__":
    main()
