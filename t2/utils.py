import os
import csv

def normalize(value):
    try:
        return float(value)
    except ValueError:
        return value

def save_csv(filename, dataset):
    with open(filename, "w") as file:
        writer = csv.writer(file, delimiter=',',
                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for row in dataset:
            writer.writerow(row)

def load_csv(filename):
    rows = []
    if os.path.isfile(filename):
        with open(filename, "r", newline='') as file:
            reader = csv.reader(file, delimiter=',', quotechar='|')
            for row in reader:
                rows.append([normalize(value) for value in row])
    header = rows[0]
    del rows[0]
    return header, rows

def without_column(data, index):
    if index == -1:
        return data[:-1]
    else:
        return data[0:index] + data[(index+1):]

def ignore_columns(dataset, columns):
    columns.sort(reverse=True)
    for entry in dataset:
        for index in columns:
            del entry[index]

def tuple_difference(first, second):
    result = ()
    for i in range(len(first)):
        result += (first[i] - second[i],)
    return result
