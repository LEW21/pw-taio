import csv
import sys
import argparse

from lib.io import save_to_csv, load_from_csv
from lib import normalizer

parser = argparse.ArgumentParser(description='Normalize and transform to symbols.')

parser.add_argument('symbole', metavar='S', type=int, help='liczba symboli')

args = parser.parse_args()

data = load_from_csv(sys.stdin, int)

data = normalizer.normalize(data, normalizer.symbols(args.symbole))

save_to_csv(data)
