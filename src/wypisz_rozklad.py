import csv
import sys
import argparse
import random

parser = argparse.ArgumentParser(description='Wypisz rozkład danej cechy.')

parser.add_argument('cecha', metavar='C', type=int, help='numer cechy')

args = parser.parse_args()

r = csv.reader(sys.stdin)
data = [[v for v in row] for row in r]

args.symbole = ord(max(max(v for v in row[1:]) for row in data)) - ord("a") + 1

litery = [sum(1 for r in data if r[1 + args.cecha] == chr(ord("a") + i)) for i in range(0, args.symbole)]

for litera, liczba in enumerate(litery):
	print(chr(ord("a") + litera) + " - " + str(liczba))
