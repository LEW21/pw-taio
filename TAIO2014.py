#!/usr/bin/env python
import argparse
import sys
import random

from src.lib import automata, set_generator, normalizer
from src.lib.optimizer import Optimizer
from src.lib.io import load_file, save_classes_file

parser = argparse.ArgumentParser(description='Generate random data.')

parser.add_argument('--etap', metavar='e', type=str, required=True)
parser.add_argument('--wejscieTyp', metavar='w', type=str)
parser.add_argument('--sciezkaTrain', metavar='str', type=str)
parser.add_argument('--sciezkaTest', metavar='ste', type=str)
parser.add_argument('--sciezkaObceTrain', metavar='str', type=str)
parser.add_argument('--sciezkaObceTest', metavar='ste', type=str)
parser.add_argument('--sciezkaOutputKlas', metavar='out', type=str)
parser.add_argument('--sciezkaOutputErr', metavar='outerr', type=str)
parser.add_argument('--iloscKlas', metavar='ilk', type=int)
parser.add_argument('--iloscCech', metavar='ich', type=int)
parser.add_argument('--iloscPowtorzenWKlasie', metavar='ilewkl', type=int)
parser.add_argument('--minLos', metavar='minlos', type=float, default=0)
parser.add_argument('--maxLos', metavar='maxlos', type=float, default=100)
parser.add_argument('--zaburzenie', metavar='zab', type=float, default=1)
parser.add_argument('--procRozmTest', metavar='procte', type=int, default=20)
parser.add_argument('--procRozmObce', metavar='obce', type=int, default=20)
parser.add_argument('--dyskretyzacja', metavar='dysk', type=int, required=True)
parser.add_argument('--ograniczNietermin', metavar='ogranicz', type=int, default=20)
parser.add_argument('--rownolegle', metavar='row', type=str) # not supported ever

# Not supported unless tagged as supported:
parser.add_argument('--PSOtrace', type=int, default=0)
parser.add_argument('--PSOfnscale', type=str)
parser.add_argument('--PSOmaxit', type=int, default=20) # Supported!
parser.add_argument('--PSOmaxf', type=str)
parser.add_argument('--PSOabstol', type=str)
parser.add_argument('--PSOreltol', type=str)
parser.add_argument('--PSOREPORT', type=str)
parser.add_argument('--PSOs', type=int, default=50) # Supported!
parser.add_argument('--PSOk', type=str)
parser.add_argument('--PSOp', type=str)
parser.add_argument('--PSOw', type=str)
parser.add_argument('--PSOc.p', type=str)
parser.add_argument('--PSOc.g', type=str)
parser.add_argument('--PSOd', type=str)
parser.add_argument('--PSOv.max', type=str)
parser.add_argument('--PSOrand.order', type=str)
parser.add_argument('--PSOmax.restart', type=str)
parser.add_argument('--PSOmaxit.stagnate', type=str)

args = parser.parse_args([('-' + x if x[0] == '-' else x) for x in sys.argv[1:]])

automationTypes = {
	"a1": "automat deterministyczny bez elementów obcych",
	"a2": "automat deterministyczny z elementami obcymi",
	"a3": "automat niedeterministyczny bez elementów obcych",
	"a4": "automat niedeterministyczny z elementami obcymi",
	"a5": "automat rozmyty bez elementów obcych",
	"a6": "automat rozmyty z elementami obcymi",
}

try:
	print(automationTypes[args.etap])
except:
	sys.exit("Nieprawidłowy etap.")

hasForeign = args.etap in ["a2", "a4", "a6"]
isFuzzy = args.etap in ["a5", "a6"]
isNondeterministic = args.etap in ["a3", "a4"]

inputType = 'czyt' if args.sciezkaTrain else 'gen'
if args.wejscieTyp and args.wejscieTyp != inputType:
	sys.exit("Typ wejścia niezgodny z pozostałymi parametrami.")

dataTrain = None
dataTest = None
foreignTrain = None
foreignTest = None

if inputType == 'czyt':
	dataTrain = load_file(args.sciezkaTrain)
	dataTest = load_file(args.sciezkaTest) if args.sciezkaTest else None
	foreignTrain = load_file(args.sciezkaObceTrain) if args.sciezkaObceTrain else None
	foreignTest = load_file(args.sciezkaObceTest) if args.sciezkaObceTrain else None
else:
	if not args.iloscKlas or not args.iloscCech or not args.iloscPowtorzenWKlasie:
		sys.exit("Brak liczby klas, cech lub powtórzeń.")
	representatives = set_generator.generate_representatives(args.iloscKlas, args.iloscCech, (args.minLos, args.maxLos))
	dataTrain = set_generator.generate_dataset(args.iloscPowtorzenWKlasie, representatives, (args.minLos, args.maxLos), args.zaburzenie)

if not dataTest:
	random.shuffle(dataTrain)
	testPercent = args.procRozmTest / 100
	testAmount = int(len(dataTrain) * testPercent)
	dataTest = dataTrain[:testAmount]
	dataTrain = dataTrain[testAmount:]

if hasForeign:
	if not foreignTrain:
		trainAmount = int(args.procRozmObce * len(dataTrain))
		testAmount = int(args.procRozmObce * len(dataTest))
		representatives = set_generator.generate_representatives(args.iloscKlas, args.iloscCech, (args.minLos, args.maxLos))
		foreignTrain = set_generator.generate_foreign_unified(trainAmount, representatives, (args.minLos, args.maxLos), args.zaburzenie)
		foreignTest = set_generator.generate_foreign_unified(testAmount, representatives, (args.minLos, args.maxLos), args.zaburzenie)

	if not foreignTest: # foreignTrain was specified - so we split it like dataTrain.
		random.shuffle(foreignTrain)
		testPercent = args.procRozmTest / 100
		testAmount = int(len(foreignTrain) * testPercent)
		foreignTest = foreignTrain[testAmount:]
		foreignTrain = foreignTrain[:testAmount]

# OK, dataset reading/generation finished.

num_classes = args.iloscKlas if args.iloscKlas else max(dataTrain, key=lambda x: x[0])[0]

if hasForeign:
	num_classes += 1
	foreign_class_number = num_classes
	dataTrain += [(foreign_class_number, attrs) for attrs in foreignTrain]
	dataTest += [(foreign_class_number, attrs) for attrs in foreignTest]
	random.shuffle(dataTrain)
	random.shuffle(dataTest)

pso_control = {key[3:]: value for key, value in vars(args).items() if key[:3] == "PSO"}

symbols = normalizer.symbols(args.dyskretyzacja)
classes = [i for i in range(0, num_classes)]
automation = automata.Automata(symbols, classes)

automation.type = automata.Nondeterministic if isNondeterministic else automata.Deterministic
automation.nondet_limit = args.ograniczNietermin/100

if isFuzzy:
    normalize_func = normalizer.normalize_fuzzy
else:
	normalize_func = normalizer.normalize

learning_set = normalize_func(dataTrain, symbols)

errors_count = automation.calculate_error(learning_set)
errors_percentage = 100 * errors_count / len(learning_set)
print('Liczba błędnych przyporządkowań: {} ({} %)'.format(errors_count, errors_percentage))

print('Optymalizowanie automatu za pomocą PSO...')
optimizer = Optimizer(automation, learning_set, symbols, classes)
optimizer.optimize(pso_control)

errors_count = automation.calculate_error(learning_set)
errors_percentage = 100 * errors_count / len(learning_set)
print('Zbiór uczący (rozmiar = {})'.format(len(learning_set)))
print('Funkcja błędu: {} ({} %)'.format(errors_count, errors_percentage))
errors_count = automation.calculate_error(learning_set, binary=True)
errors_percentage = 100 * errors_count / len(learning_set)
print('Liczba błędnych przyporządkowań: {} ({} %)'.format(errors_count, errors_percentage))

test_set = normalize_func(dataTest, symbols)
errors_count = automation.calculate_error(test_set)
errors_percentage = 100 * errors_count / len(test_set)
print('Zbiór testowy (rozmiar = {})'.format(len(test_set)))
print('Funkcja błędu: {} ({} %)'.format(errors_count, errors_percentage))
errors_count = automation.calculate_error(test_set, binary=True)
errors_percentage = 100 * errors_count / len(test_set)
print('Liczba błędnych przyporządkowań: {} ({} %)'.format(errors_count, errors_percentage))

if args.sciezkaOutputKlas:
	classes = automation.consume_dataset(test_set, choose_best=True)
	save_classes_file(classes, args.sciezkaOutputKlas)

if args.sciezkaOutputErr:
	classes = [str(errors_percentage)+"%"]
	save_classes_file(classes, args.sciezkaOutputErr)
