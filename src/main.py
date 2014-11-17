import argparse

from lib.automata import Automata
from lib.optimizer import Optimizer
from lib.set_generator import DataSetGenerator
from lib.normalizer import Normalizer


parser = argparse.ArgumentParser(description='Generate random data.')

parser.add_argument('klasy', metavar='K', type=int, help='liczba klas')
parser.add_argument('cechy', metavar='C', type=int, help='liczba cech')
parser.add_argument('wiersze', metavar='N', type=int, help='liczba wierszy dla każdej klasy')
parser.add_argument('symbole', metavar='S', type=int, help='liczba symboli')

args = parser.parse_args()

set_generator = DataSetGenerator(args.klasy, args.cechy, args.wiersze)

learning_set = set_generator.generate_learning_set()
normalizer = Normalizer(args.symbole, learning_set)
learning_set = normalizer.data_set
symbols = normalizer.symbols
classes = set_generator.classes
automata = Automata(symbols, classes)

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

test_set = set_generator.generate_test_set()
normalizer = Normalizer(args.symbole, test_set)
test_set = normalizer.data_set
errors_count = automata.calculate_error(test_set)
errors_percentage = 100 * errors_count / len(test_set)
print('Zbiór testowy (rozmiar = {})'.format(len(test_set)))
print('Liczba błędnych przyporządkowań: {} ({} %)'.format(errors_count, errors_percentage))
