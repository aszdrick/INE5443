import random
import math
import numpy as np
import matplotlib.pyplot as plt

def single_spiral(grid_size):
	step = 1
	noise = 0
	radius = float(grid_size) + 15
	theta = 0
	result = []
	for i in range(int(grid_size / step)):
		theta_rad = theta * math.pi / 180
		actual_noise = noise * math.sqrt(radius / grid_size)
		x = radius * math.cos(theta_rad) + random.uniform(-actual_noise, actual_noise)
		y = radius * math.sin(theta_rad) + random.uniform(-actual_noise, actual_noise)
		result.append((x, y))
		theta += 4
		radius -= step
	return result

def double_spiral(grid_size):
	original = single_spiral(grid_size)
	result = []
	rotation = math.pi
	sin = math.sin(rotation)
	cos = math.cos(rotation)
	for i in range(len(original)):
		(x, y) = original[i]
		xn = x * cos - y * sin
		yn = x * sin + y * cos
		result.append((xn, yn))
	return [original, result]

data = double_spiral(400)
plt.scatter([tp[0] for tp in data[0]], [tp[1] for tp in data[0]], color="r")
plt.scatter([tp[0] for tp in data[1]], [tp[1] for tp in data[1]], color="b")
plt.show()
