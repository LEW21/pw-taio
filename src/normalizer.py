import math


def symbols(count):
    return [chr(int(ord("a") + i)) for i in range(0, count)]

def normalize(data_set, symbols):
    attributes_count = len(data_set[0][1])
    attributes_range = [(min(row[1][i] for row in data_set), max(row[1][i] for row in data_set) + 1) for i in range(0, attributes_count)]
    # Normalizacja
    data_set = [[row[0], [(v - minv)/(maxv - minv) for (minv, maxv), v in zip(attributes_range, row[1])]] for row in data_set]
    # Zamiana na symbole
    data_set = [[row[0], [symbols[int(v * len(symbols))] for v in row[1]]] for row in data_set]
    return data_set


def normalize_fuzzy(data_set, symbols):
	attributes_count = len(data_set[0][1])
	attributes_range = [(min(row[1][i] for row in data_set), max(row[1][i] for row in data_set) + 1) for i in range(0, attributes_count)]
	# Normalizacja
	data_set = [[row[0], [(v - minv)/(maxv - minv) for (minv, maxv), v in zip(attributes_range, row[1])]] for row in data_set]
	# Zamiana na symbole
	result = []
	for row in data_set:
		attributes = []
		for v in row[1]:
			symbol_certainty = []
			symbols_count = len(symbols)
			for index, symbol in enumerate(symbols):
				symbol_center = (1.0 / symbols_count) * (index + 0.5)
				value = math.exp(-(1.5*symbols_count*(v - symbol_center)) ** 2)
				symbol_certainty.append(value)
			attributes.append(symbol_certainty)
		result.append([row[0], attributes])
	return result
