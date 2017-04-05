import csv
from math import sqrt
import math
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

class Classifier:
    hits = 0
    fails = 0
    descriptor = []
    def classify(self, entry, class_index=-1):
        max_similarity = -math.inf
        best_entry = None
        for internal_entry in self.descriptor:
            distance = euclidian_dist(entry, internal_entry)
            if distance > max_similarity:
                max_similarity = distance
                best_entry = internal_entry
        return best_entry[class_index]

    def add_random_entry(self, training_set):
        self.descriptor.append(self.pick_one(training_set))

    def pick_one(self, array):
        return array[round(np.random.uniform(0, len(array)))]

class IBL1(Classifier):
    def __init__(self, training_set, class_index=-1):
        if len(descriptor) == 0:
            self.add_random_entry(training_set)

        max_similarity = -math.inf
        best_entries = []
        for external_entry in training_set:
            for internal_entry in self.descriptor:
                similarity = -euclidian_dist(external_entry, internal_entry)
                if similarity > max_similarity:
                    max_similarity = similarity
                    best_entries = [internal_entry]
                elif similarity == max_similarity:
                    best_entries.append(internal_entry)
            best_entry = self.pick_one(best_entries)
            if internal_entry[class_index] == best_entry[class_index]:
                self.hits += 1
            else:
                self.fails += 1
            descriptor.append(external_entry)

class IBL2(Classifier):
    def __init__(self, training_set, class_index=-1):
        if len(descriptor) == 0:
            self.add_random_entry(training_set)

        max_similarity = -math.inf
        best_entries = []
        for external_entry in training_set:
            for internal_entry in self.descriptor:
                similarity = -euclidian_dist(external_entry, internal_entry)
                if similarity > max_similarity:
                    max_similarity = similarity
                    best_entries = [internal_entry]
                elif similarity == max_similarity:
                    best_entries.append(internal_entry)
            best_entry = self.pick_one(best_entries)
            if internal_entry[class_index] == best_entry[class_index]:
                self.hits += 1
            else:
                self.fails += 1
                descriptor.append(external_entry)
