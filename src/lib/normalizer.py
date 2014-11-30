
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
