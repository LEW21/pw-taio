import argparse
import sys

from lib.automata import Automata
from lib.optimizer import Optimizer
from lib.set_generator import DataSetGenerator
from lib import normalizer
from lib.io import load_from_csv

parser = argparse.ArgumentParser(description='Generate random data.')

parser.add_argument('-k', '--klasy', metavar='K', type=int, help='liczba klas')
parser.add_argument('-c', '--cechy', metavar='C', type=int, help='liczba cech')
parser.add_argument('-n', '--wiersze', metavar='N', type=int, help='liczba wierszy dla każdej klasy')
parser.add_argument('-s', '--symbole', metavar='s', type=int, help='liczba symboli')
parser.add_argument('-S', '--sigma', metavar='S', type=int, help='odchylenie standardowe wartości', default=2)
parser.add_argument('-l', '--learning', metavar='l', type=str, help='plik uczący')
parser.add_argument('-t', '--test', metavar='t', type=str, help='plik testowy')

args = parser.parse_args()

if not (args.klasy and args.cechy and args.wiersze) and not (args.learning and args.test):
    sys.exit("Podaj (-k, -c i -n) lub (-l i -t).")

if not args.symbole:
    sys.exit("Podaj -s.")

if args.wiersze:
    set_generator = DataSetGenerator(args.klasy, args.cechy, args.wiersze)
    learning_set = set_generator.generate_learning_set()
    test_set = set_generator.generate_test_set()
else:
    learning_set = load_from_csv(open(args.learning, "r"), float)
    test_set = load_from_csv(open(args.test, "r"), float)
    args.klasy = max(learning_set, key=lambda x: x[0])[0]

symbols = normalizer.symbols(args.symbole)
classes = [i for i in range(0, args.klasy)]
automata = Automata(symbols, classes)

learning_set = normalizer.normalize(learning_set, symbols)

errors_count = automata.calculate_error(learning_set)
errors_percentage = 100 * errors_count / len(learning_set)
print('Liczba błędnych przyporządkowań: {} ({} %)'.format(errors_count, errors_percentage))

print('Optymalizowanie automatu za pomocą PSO...')
optimizer = Optimizer(automata, learning_set, symbols, classes)
optimizer.optimize()

errors_count = automata.calculate_error(learning_set)
errors_percentage = 100 * errors_count / len(learning_set)
print('Zbiór uczący (rozmiar = {})'.format(len(learning_set)))
print('Liczba błędnych przyporządkowań: {} ({} %)'.format(errors_count, errors_percentage))

test_set = normalizer.normalize(test_set, symbols)
errors_count = automata.calculate_error(test_set)
errors_percentage = 100 * errors_count / len(test_set)
print('Zbiór testowy (rozmiar = {})'.format(len(test_set)))
print('Liczba błędnych przyporządkowań: {} ({} %)'.format(errors_count, errors_percentage))
