import csv
import sys
import argparse
import random

from lib.set_generator import DataSetGenerator, UnifiedForeignObjectsSetGenerator, PermutedForeignObjectsSetGenerator
from lib.io import save_to_csv

parser = argparse.ArgumentParser(description='Generate random data.')

parser.add_argument('klasy', metavar='K', type=int, help='liczba klas')
parser.add_argument('cechy', metavar='C', type=int, help='liczba cech')
parser.add_argument('wiersze', metavar='N', type=int, help='liczba wierszy dla każdej klasy')
parser.add_argument('learning', metavar='L', type=str, help='plik uczący')
parser.add_argument('test', metavar='T', type=str, help='plik testowy')
parser.add_argument('type', metavar='t', type=str, help='typ: n (normalny), u (jednorodny), p (permutujący), up, pu', default='n')
parser.add_argument('-S', '--sigma', metavar='S', type=int, help='odchylenie standardowe wartości - absolutne', default=1)

args = parser.parse_args()

def Gen(type):
	return DataSetGenerator if type == 'n' else UnifiedForeignObjectsSetGenerator if type == 'u' else PermutedForeignObjectsSetGenerator

if len(args.type) == 1:
	args.type = args.type + args.type


set_generator = Gen(args.type[0])(args.klasy, args.cechy, args.wiersze, args.sigma)
save_to_csv(set_generator.generate_learning_set(), open(args.learning, "w"))

set_generator2 = Gen(args.type[1])(args.klasy, args.cechy, args.wiersze, args.sigma)
set_generator2.class_representative = set_generator.class_representative
set_generator = set_generator2
save_to_csv(set_generator.generate_test_set(), open(args.test, "w"))
