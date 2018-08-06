import os
import csv


files = os.listdir('data')


for file in files:
    with open(os.path.join('data', file), 'r') as f:
        data = list(csv.reader(f.readlines()))

    print(data[0], data[1])
