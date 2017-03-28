import csv
from math import sqrt
import numpy as np
import sys

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

# def hamming_dist(v1, v2):
#     dist = 0
#     for i in range(len(v1)):
#         dist += abs(v1[i] - v2[i])
#     return dist

# def euclidian_dist(v1, v2):
#     dist = 0
#     for i in range(len(v1)):
#         dist += (v1[i] - v2[i]) ** 2
#     return np.sqrt(dist)

def linear_mahalanobis(training_set, pixels, callback):
    r = []
    g = []
    b = []
    r_sum = 0
    g_sum = 0
    b_sum = 0

    for (red, green, blue) in training_set:
        r.append(red)
        g.append(green)
        b.append(blue)

        r_sum += red
        g_sum += green
        b_sum += blue

    size = len(training_set)
    center = (r_sum / size, g_sum / size, b_sum / size)
    A = np.cov(np.array([r, g, b]))
    try:
        Ainv = np.linalg.inv(A)
    except:
        print("Error: failed to invert the pixel matrix")
        sys.exit(0)
    for pixel in pixels:
        delta = utils.tuple_difference(pixel, center)
        deltaT = np.array([delta]).transpose()
        result = np.dot([delta], Ainv)
        result = np.dot(result, deltaT)
        distance = sqrt(result[0][0])
        callback(pixel, distance)

def quadratic_mahalanobis(training_set, pixels, callback):
    r = []
    g = []
    b = []
    r2 = []
    g2 = []
    b2 = []
    rg = []
    rb = []
    gb = []
    r_sum = 0
    g_sum = 0
    b_sum = 0
    r2_sum = 0
    g2_sum = 0
    b2_sum = 0
    rg_sum = 0
    rb_sum = 0
    gb_sum = 0

    for (red, green, blue) in training_set:
        # TODO: is this the right way to calculate the parameters?
        r.append(red)
        g.append(green)
        b.append(blue)
        r2.append(red * red)
        g2.append(green * green)
        b2.append(blue * blue)
        rg.append(red * green)
        rb.append(red * blue)
        gb.append(green * blue)

        r_sum += r[-1]
        g_sum += g[-1]
        b_sum += b[-1]
        r2_sum += r2[-1]
        g2_sum += g2[-1]
        b2_sum += b2[-1]
        rg_sum += rg[-1]
        rb_sum += rb[-1]
        gb_sum += gb[-1]

    size = len(training_set)
    center = (r_sum / size, g_sum / size, b_sum / size,\
              r2_sum / size, g2_sum / size, b2_sum / size,\
              rg_sum / size, rb_sum / size, gb_sum / size)
    A = np.cov(np.array([r, g, b, r2, g2, b2, rg, rb, gb]))
    try:
        Ainv = np.linalg.inv(A)
    except:
        print("Error: failed to invert the pixel matrix")
        sys.exit(0)
    for (r, g, b) in pixels:
        pixel = (r, g, b, r * r, g * g, b * b, r * g, r * b, g * b)
        delta = utils.tuple_difference(prepared_pixel, center)
        deltaT = np.array([delta]).transpose()
        result = np.dot([delta], Ainv)
        result = np.dot(result, deltaT)
        distance = sqrt(result[0][0])
        callback(pixel, distance)
