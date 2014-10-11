import csv
import sys
import argparse
import random

parser = argparse.ArgumentParser(description='Generate random data.')

parser.add_argument('klasy', metavar='K', type=int, help='liczba klas')
parser.add_argument('cechy', metavar='C', type=int, help='liczba cech')
parser.add_argument('wiersze', metavar='N', type=int, help='liczba wierszy')
parser.add_argument('-S', '--sigma-abs', metavar='S', type=int, help='odchylenie standardowe wartości - absolutne', default=10)
parser.add_argument('-s', '--sigma-rel', metavar='s', type=float, help='odchylenie standardowe wartości - relatywne do wielkości zakresu', default=0.1)
parser.add_argument('-V', '--wypisz-sigmy-abs', action='store_true', help='wypisz wyliczone sigmy absolutne')
parser.add_argument('-v', '--wypisz-sigmy-rel', action='store_true', help='wypisz wyliczone sigmy relatywne')

args = parser.parse_args()

def rand_zakres():
	# Dlaczego sigma jako minimum? Bo chcę, żeby ujemnych wartości było relatywnie mało - nie są specjalnie oczekiwanym wynikiem normalnych pomiarów.
	zakres = sorted([random.randrange(args.sigma_abs, 1000), random.randrange(args.sigma_abs, 1000)])
	if zakres[0] != zakres[1]:
		return zakres
	return rand_zakres()

zakres_cech = [rand_zakres() for j in range(0, args.cechy)]

if args.wypisz_sigmy_abs:
	for i, (vmin, vmax) in enumerate(zakres_cech):
		print("Sigma absolutna cechy " + str(i) + ": " + str(round(args.sigma_abs + args.sigma_rel * (vmax - vmin), 2)), file=sys.stderr)

if args.wypisz_sigmy_rel:
	for i, (vmin, vmax) in enumerate(zakres_cech):
		print("Sigma relatywna cechy " + str(i) + ": " + str(round(args.sigma_abs / (vmax - vmin) + args.sigma_rel, 2)), file=sys.stderr)

D = {}
for i in range(0, args.klasy):
	D[i] = [random.randrange(min, max) for min, max in zakres_cech]

w = csv.writer(sys.stdout)
for i in range(0, args.wiersze):
	k = random.randrange(0, args.klasy)
	w.writerow([str(k)] + [str(int(random.normalvariate(x, args.sigma_abs + args.sigma_rel * (xmax - xmin)))) for x, (xmin, xmax) in zip(D[k], zakres_cech)])
