import csv
import numpy as np

def kNN(dataset, new_data, dfn, k=1):
    dist = []
    for data in dataset:
        dist.append((dfn(data[:-1], new_data), data[-1]))

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

def hamming_dist(v1, v2):
    dist = 0
    for i in range(len(v1)):
        dist += abs(v1[i] - v2[i])
    return dist

def euclidian_dist(v1, v2):
    dist = 0
    for i in range(len(v1)):
        dist += (v1[i] - v2[i]) ** 2
    return np.sqrt(dist)

zeros = np.zeros((10000, 10000))
ones = np.ones((10000, 10000))

print(hamming_dist(zeros.tolist(), ones.tolist()))
#print(hamming_dist([10, 2000, 20, 4, 0, 0, 0], [2, 3000, 40, 5, 100, 4, 1]))
