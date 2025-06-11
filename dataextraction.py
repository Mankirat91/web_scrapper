import csv

def read_csv(path):
    data = []
    csv_file = open(path, newline= '', encoding='utf-8')
    reader = csv.DictReader(csv_file)
    for row in reader:
        data.append(row)
    return data