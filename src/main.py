import argparse

from lib import Automata
from lib import Gen
from lib import Norm


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

generator = Gen.Gen(args.klasy, args.cechy, args.wiersze)
if args.wypisz_sigmy_abs:
    generator.wypiszSigmyAbs()
if args.wypisz_sigmy_rel:
    generator.wypiszSigmyRel()

zbior = generator.generujZbior()
normalizator = Norm.Norm(args.symbole, zbior)
zbior = normalizator.zbior
automat = Automata.Automata(normalizator.symboleTab, generator.klasyTab)
liczbaBledow = automat.calculateError(zbior)
liczbaBledowProcentowo = 100 * liczbaBledow / len(zbior)
print('Liczba błędnych przyporządkowań: {} ({} %)'.format(liczbaBledow, liczbaBledowProcentowo))
