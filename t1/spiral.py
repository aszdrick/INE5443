import random
import math
import numpy as np
import matplotlib.pyplot as plt

def single_spiral(grid_size, noise = 0):
	step = 1
	radius = float(grid_size)
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

def double_spiral(grid_size, noise = 0):
	original = single_spiral(grid_size, noise)
	result = []
	rotation = math.pi
	sin = math.sin(rotation)
	cos = math.cos(rotation)
	for i in range(len(original)):
		(x, y) = original[i]
		xn = x * cos - y * sin
		yn = x * sin + y * cos
		result.append((xn, yn))
	return [single_spiral(grid_size, noise), result]
