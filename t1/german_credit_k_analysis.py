from main import *

data = load("german_credit.csv")[1:]
for row in data:
    del row[0]

training = data[0:len(data):2]
test = data[1:len(data):2]

hit_table = {}
for k in range(1, 15):
    attempts = []
    for entry in test:
        attempts.append(entry[:-1])

    for entry in attempts:
        entry.append(kNN(training, entry, euclidian_dist, 0, k))

    hits = 0
    fails = 0
    for i in range(len(attempts)):
        if attempts[i][-1] == test[i][-1]:
            hits += 1
        else:
            fails += 1
    hit_table[k] = (hits, fails)

print(hit_table)
