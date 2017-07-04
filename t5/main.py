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

# Returns the euclidean distance between two entries
def eucl_dist(first, second):
    result = 0

    for index in range(len(first)):
        result += (first[index] - second[index]) ** 2

    return math.sqrt(result)

# Returns a triangular matrix representing the distance
# between every pair of elements in the dataset
def distance_matrix(dataset):
    num_entries = len(dataset)
    dist_matrix = []
    min_dist = (1, 0)

    for first in range(num_entries):
        dist_matrix.append([])
        for second in range(0, first):
            a = dataset[first]
            b = dataset[second]
            distance = eucl_dist(a, b)
            dist_matrix[first].append(distance)

            if distance < dist_matrix[min_dist[0]][min_dist[1]]:
                min_dist = (first, second)

    return (dist_matrix, min_dist)
    # return dist_matrix

def apply_linkage(first, second, linkage):
    if linkage == "nearest":
        return min(first, second)
    elif linkage == "complete":
        return max(first, second)
    elif linkage == "average":
        return (first + second) / 2
    return None

def pretty_print(matrix):
    print("[")
    for row in matrix:
        print("  ", row)
    print("]")

# Removes a row/column from a matrix, merging the remaining
# elements according to a linkage heuristic
def table_merge(matrix, coords, linkage):
    (row_index, column_index) = coords

    print("\nOriginal:")
    pretty_print(matrix)
    print("Coords:", coords)

    # The matrix is always square
    order = len(matrix)

    # Merges the relevant cells
    row = matrix[row_index]
    for i in range(order):
        if i != row_index and i != column_index:
            # Skips reflective comparisons
            # print("linkage(%d, %d)" % (row[i], matrix[column_index][i]))
            row[i] = apply_linkage(row[i], matrix[row_index][i], linkage)
            # row[row_index] = apply_linkage(row[row_index], row[column_index], linkage)

            r = matrix[i]
            # print("linkage(%d, %d)" % (r[row_index], r[column_index]))
            r[row_index] = apply_linkage(r[row_index], r[column_index], linkage)
            r[column_index] = apply_linkage(r[column_index], r[row_index], linkage)

    for i in range(order):
        for j in range(i + 1, order):
            matrix[i][j] = matrix[j][i]

    print("After traversal:")
    pretty_print(matrix)

    highest = max(row_index, column_index)
    for i in range(order):
        del matrix[i][highest]
    del matrix[row_index]

    # del matrix[row_index]
    # for row in matrix:
    #     del row[column_index]

    print("After row/column removal:")
    pretty_print(matrix)

def clusterize(dataset, linkage):
    # (dist_matrix, coords) = distance_matrix(dataset)
    dist_matrix = [
        [0, 2, 6, 10, 9],
        [2, 0, 5, 1, 8],
        [6, 5, 0, 4, 5],
        [10, 1, 4, 0, 3],
        [9, 8, 5, 3, 0]
    ]

    # coords = (1, 0)
    coords = (3, 1)

    # labels = [[i] for i in range(len(dist_matrix))]
    labels = [["A"], ["B"], ["C"], ["D"], ["E"]]

    # merges = []
    # merges.append((coords[0], coords[1], dist_matrix[coords[0]][coords[1]]))

    print("dist_matrix:", dist_matrix)
    print("merge coords:", coords)
    print("min distance =", dist_matrix[coords[0]][coords[1]])

    tree = (labels[coords[0]], labels[coords[1]], dist_matrix[coords[0]][coords[1]])
    # print("Tree:", tree)

    labels[coords[1]] += labels[coords[0]]
    del labels[coords[0]]
    print("Labels:", labels)

    table_merge(dist_matrix, coords, linkage)

    size = len(dist_matrix)
    while size != 1:
        lowest = (1, 0)
        for i in range(size):
            for j in range(0, i):
                if dist_matrix[i][j] < dist_matrix[lowest[0]][lowest[1]]:
                    lowest = (i, j)

        print("------------------------")
        print("size:", size)
        print("dist_matrix:", dist_matrix)
        print("merge coords:", lowest)
        print("min distance =", dist_matrix[lowest[0]][lowest[1]])

        # tree = (labels[coords[0]], labels[coords[1]], dist_matrix[coords[0]][coords[1]])
        # print("Tree:", tree)

        labels[lowest[1]] += labels[lowest[0]]
        del labels[lowest[0]]
        print("Labels:", labels)

        table_merge(dist_matrix, lowest, linkage)
        size = len(dist_matrix)

def main():
    args = parser.parse_args()
    header, dataset = utils.load_csv(args.input)
    if len(dataset) == 0:
        parser.error("Invalid input: file does not exist or is empty.")

    dataset = standardize(dataset)
    dataset = clusterize(dataset, args.linkage)

if __name__ == "__main__":
    main()
