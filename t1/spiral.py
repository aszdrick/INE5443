import random
import math
import numpy as np
import matplotlib.pyplot as plt

def single_spiral(grid_size, direction = 1):
	step = 1
	noise = 0
	radius = float(grid_size)
	theta = 0
	result = []
	for i in range(int(grid_size / step)):
		theta_rad = theta * math.pi / 180
		actual_noise = noise * math.sqrt(radius / grid_size)
		visual_radius = radius + random.uniform(-actual_noise, actual_noise)
		x = visual_radius * math.cos(theta_rad)
		y = visual_radius * math.sin(theta_rad)
		result.append((x, y))
		theta += 5 * direction
		radius -= step
	return result

data1 = single_spiral(400)
data2 = single_spiral(400, -1)
plt.scatter([tp[0] for tp in data1], [tp[1] for tp in data1], color="r")
plt.scatter([tp[0] for tp in data2], [tp[1] for tp in data2], color="b")
plt.show()