import csv
from math import sqrt
import numpy as np
import sys
import utils

def kNN(dataset, new_data, dfn, c_index=-1, k=1):
    dist = []
    for data in dataset:
        if c_index == -1:
            without_class = data[:-1]
        else:
            without_class = data[0:c_index] + data[(c_index+1):]
        dist.append((dfn(without_class, new_data), data[c_index]))

    dist.sort(key=lambda tup: tup[0])

    scoreboard = {}

    for vote in dist[:k]:
        if vote[1] not in scoreboard:
            scoreboard[vote[1]] = 0
        scoreboard[vote[1]] += 1

    winner = (0, None)
    for key, value in scoreboard.items():
        if value > winner[0]:
            winner = (value, key)

    return winner[1]

def hamming_dist(v1, v2):
    return np.sum(abs(np.array(v1) - np.array(v2)))

def euclidian_dist(v1, v2):
    return np.sqrt(np.sum((np.array(v1) - np.array(v2)) ** 2))
