#!/usr/bin/python3

from arguments import *
from dendrogram import *
import math
import utils

# Returns the mean value and the standard deviation of a dataset
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

# Normalizes a dataset
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

# Returns a symmetric matrix representing the distance
# between every pair of elements in the dataset
def distance_matrix(dataset):
    num_entries = len(dataset)
    dist_matrix = [[0 for x in range(num_entries)] for y in range(num_entries)]
    min_dist = (1, 0)

    for first in range(num_entries):
        for second in range(0, first):
            a = dataset[first]
            b = dataset[second]
            distance = eucl_dist(a, b)
            dist_matrix[first][second] = distance

            if distance < dist_matrix[min_dist[0]][min_dist[1]]:
                min_dist = (first, second)

    # Fills the upper right corner of
    # the matrix, preserving symmetry.
    for i in range(num_entries):
        for j in range(i + 1, num_entries):
            dist_matrix[i][j] = dist_matrix[j][i]

    return (dist_matrix, min_dist)

# Applies a linkage heuristic to two distances
def apply_linkage(first, second, linkage):
    if linkage == "nearest":
        return min(first, second)
    elif linkage == "complete":
        return max(first, second)
    elif linkage == "average":
        return (first + second) / 2
    return None

# Removes a row/column from a matrix, merging the remaining
# elements according to a linkage heuristic
def table_merge(matrix, coords, linkage):
    (row_index, column_index) = coords

    # The matrix is always square
    order = len(matrix)

    # Merges the relevant cells
    for i in range(order):
        # Skips reflective comparisons
        if i != row_index and i != column_index:
            row = matrix[i]
            row[row_index] = apply_linkage(row[row_index], row[column_index], linkage)
            row[column_index] = apply_linkage(row[column_index], row[row_index], linkage)

    # Preserves symmetry
    for i in range(order):
        for j in range(i + 1, order):
            matrix[i][j] = matrix[j][i]

    # Reduces the resulting distance matrix
    highest = max(row_index, column_index)
    for i in range(order):
        del matrix[i][highest]
    del matrix[row_index]

# Turns all unary lists in a recursive tuple into scalars
def remove_lists(merge_tuple):
    (first, second, distance) = merge_tuple
    if isinstance(first, tuple):
        first = remove_lists(first)
    else:
        first = first[0]

    if isinstance(second, tuple):
        second = remove_lists(second)
    else:
        second = second[0]

    return (first, second, distance)

# Transforms a merge list into a recursive tuple
def tuple_format(merge_list):
    # Stores a tuple -> tuple mapping representing
    # which merge originated each tuple
    mappings = {}

    for merge in merge_list:
        mappings[tuple(sorted(merge[0] + merge[1]))] = merge

    for index in range(len(merge_list)):
        merge = merge_list[index]
        (old_first, old_second, distance) = merge
        (new_first, new_second) = (old_first, old_second)
        if len(new_first) > 1:
            new_first = mappings[tuple(sorted(new_first))]
        if len(new_second) > 1:
            new_second = mappings[tuple(sorted(new_second))]

        merge_list[index] = (new_first, new_second, distance)

        mappings[tuple(sorted(list(old_first) + list(old_second)))] = merge_list[index]

    # The last element in the merge_list
    # is completely unrolled
    result = merge_list[len(merge_list) - 1]

    # The resulting recursive tuple contains unary lists
    # of elements, so turn them into scalars and return them
    return remove_lists(result)

# Clusterizes a dataset according to a linkage heuristic,
# returning a tree-like recursive tuple representing the
# resulting dendrogram
def clusterize(dataset, linkage):
    (dist_matrix, coords) = distance_matrix(dataset)

    labels = [[i] for i in range(len(dist_matrix))]

    # Stores a list of all merges performed
    merges = []
    merges.append((labels[coords[0]][:], labels[coords[1]][:], dist_matrix[coords[0]][coords[1]]))

    # Glues the labels used in the first merge
    labels[coords[1]] += labels[coords[0]]
    del labels[coords[0]]

    # Executes the first merge
    table_merge(dist_matrix, coords, linkage)

    size = len(dist_matrix)
    # Continue merging until there is only one group
    while size != 1:
        # Finds the minimum element in the distance matrix
        lowest = (1, 0)
        for i in range(size):
            for j in range(0, i):
                if dist_matrix[i][j] < dist_matrix[lowest[0]][lowest[1]]:
                    lowest = (i, j)

        min_dist = dist_matrix[lowest[0]][lowest[1]]

        # Registers a new merge where the minimum element is
        merges.append((labels[lowest[0]][:], labels[lowest[1]][:], min_dist))

        # Glues the labels used in the merge
        labels[lowest[1]] += labels[lowest[0]]
        del labels[lowest[0]]

        # Executes the merge
        table_merge(dist_matrix, lowest, linkage)
        size = len(dist_matrix)

    # Transforms the resulting merge list into a
    # tree-like recursive tuple and returns it
    return tuple_format(merges)

def main():
    args = parser.parse_args()
    header, dataset = utils.load_csv(args.input)
    if len(dataset) == 0:
        parser.error("Invalid input: file does not exist or is empty.")

    dataset = standardize(dataset)
    dendrogram_info = clusterize(dataset, args.linkage)
    # print("dendrogram_info:", dendrogram_info)

    plot(dendrogram_info)
    plt.show()

    trees = cut(dendrogram_info, [1, 0], [2, 10])
    plot(trees)
    plt.show()

if __name__ == "__main__":
    main()
