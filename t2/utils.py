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

# def aglutinate(dataset, columns):
#     result = []
#     for entry in dataset:
#         new_entry = []
#         aglutination = ""
#         last_column = -1
#         for i in reversed(range(len(entry))):
#             if i not in columns:
#                 new_entry.append(entry[i])
#             elif last_column == -1:
#                 last_column = i
#                 print(entry[i])
#                 entry[i] = str(entry[i])
#             else:
#                 entry[last_column] += str(entry[i])
#                 del entry[i]
#         new_entry.append(aglutination)
#         result.append(new_entry)
#     dataset = result
#     return last_column

def tuple_difference(first, second):
    result = ()
    for i in range(len(first)):
        result += (first[i] - second[i],)
    return result

def hex_to_tuple(rgb):
    rgb = rgb[1:]
    return (int(rgb[:2], 16), int(rgb[2:4], 16), int(rgb[4:], 16))
