import csv

def normalize(value):
    try:
        return float(value)
    except ValueError:
        return value

def save(filename, dataset):
    with open(filename, "w") as file:
        writer = csv.writer(file, delimiter=',',
                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for row in dataset:
            writer.writerow(row)

def load(filename):
    with open(filename, "r", newline='') as file:
        reader = csv.reader(file, delimiter=',', quotechar='|')
        rows = []
        for row in reader:
            rows.append([normalize(value) for value in row])
        return rows

def empty(value):
    if value is None:
        return True
    t = type(value)
    if t == type(0) or t == type(0.):
        return False
    return len(value) == 0

def without_column(data, index):
    if index == -1:
        return data[:-1]
    else:
        return data[0:index] + data[(index+1):]