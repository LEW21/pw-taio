import argparse

from lib import automata
from lib import optimizer
from lib import gen
from lib import norm


parser = argparse.ArgumentParser(description='Generate random data.')

parser.add_argument('klasy', metavar='K', type=int, help='liczba klas')
parser.add_argument('cechy', metavar='C', type=int, help='liczba cech')
parser.add_argument('wiersze', metavar='N', type=int, help='liczba wierszy')
parser.add_argument('symbole', metavar='S', type=int, help='liczba symboli')
parser.add_argument('-S', '--sigma-abs', metavar='S', type=int, help='odchylenie standardowe wartości - absolutne', default=10)
parser.add_argument('-s', '--sigma-rel', metavar='s', type=float, help='odchylenie standardowe wartości - relatywne do wielkości zakresu', default=0.1)
parser.add_argument('-V', '--wypisz-sigmy-abs', action='store_true', help='wypisz wyliczone sigmy absolutne')
parser.add_argument('-v', '--wypisz-sigmy-rel', action='store_true', help='wypisz wyliczone sigmy relatywne')

args = parser.parse_args()

generator = gen.Gen(args.klasy, args.cechy, args.wiersze)
if args.wypisz_sigmy_abs:
    generator.wypiszSigmyAbs()
if args.wypisz_sigmy_rel:
    generator.wypiszSigmyRel()

zbiorUczacy = generator.generujZbiorUczacy()
normalizator = norm.Norm(args.symbole, zbiorUczacy)
zbiorUczacy = normalizator.zbior
symbole = normalizator.symboleTab
klasy = generator.klasyTab
automat = automata.Automata(symbole, klasy)

liczbaBledow = automat.calculateError(zbiorUczacy)
liczbaBledowProcentowo = 100 * liczbaBledow / len(zbiorUczacy)
print('Liczba błędnych przyporządkowań: {} ({} %)'.format(liczbaBledow, liczbaBledowProcentowo))

print('Optymalizowanie automatu za pomocą PSO...')
optymalizator = optimizer.Optimizer(automat, zbiorUczacy, symbole, klasy)
optymalizator.optimize()

liczbaBledow = automat.calculateError(zbiorUczacy)
liczbaBledowProcentowo = 100 * liczbaBledow / len(zbiorUczacy)
print('Zbiór uczący (rozmiar = {})'.format(len(zbiorUczacy)))
print('Liczba błędnych przyporządkowań: {} ({} %)'.format(liczbaBledow, liczbaBledowProcentowo))

zbiorTestowy = generator.generujZbiorTestowy()
normalizator = norm.Norm(args.symbole, zbiorTestowy)
zbiorTestowy = normalizator.zbior
liczbaBledow = automat.calculateError(zbiorTestowy)
liczbaBledowProcentowo = 100 * liczbaBledow / len(zbiorTestowy)
print('Zbiór testowy (rozmiar = {})'.format(len(zbiorTestowy)))
print('Liczba błędnych przyporządkowań: {} ({} %)'.format(liczbaBledow, liczbaBledowProcentowo))
