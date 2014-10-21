import csv
import sys
import argparse
import random

parser = argparse.ArgumentParser(description='Normalize and transform to symbols.')

parser.add_argument('symbole', metavar='S', type=int, help='liczba symboli')

args = parser.parse_args()

r = csv.reader(sys.stdin)
data = [[int(v) for v in row] for row in r]

args.cechy = len(data[0]) - 1

minmax_cech = [(min(row[1 + i] for row in data), max(row[1 + i] for row in data) + 1) for i in range(0, args.cechy)]

# Normalizacja
data = [[row[0]] + [(v - minv)/(maxv - minv) for (minv, maxv), v in zip(minmax_cech, row[1:])] for row in data]

# Zamiana na symbole
data = [[row[0]] + [chr(int(ord("a") + v*args.symbole)) for v in row[1:]] for row in data]

w = csv.writer(sys.stdout)
for d in data:
	w.writerow(d)
