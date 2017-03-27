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

def without_column(data, index):
    if index == -1:
        return data[:-1]
    else:
        return data[0:index] + data[(index+1):]

def tuple_difference(first, second):
    result = ()
    for i in range(len(first)):
        result += (first[i] - second[i],)
    return result
