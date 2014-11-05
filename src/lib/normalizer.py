import csv


class Normalizer:
    __symbols_count = 0
    symbols = []
    data_set = []
    __attributes_count = 0

    def __init__(self, symbols_count, data_set):
        self.__symbols_count = symbols_count
        self.data_set = data_set
        self.__attributes_count = len(data_set[0][1])
        self.symbols = [chr(int(ord("a") + i)) for i in range(0, self.__symbols_count)]
        self.__normalize()

    def load_from_csv(self, csv_file):
        r = csv.reader(csv_file)
        self.data_set = []
        for row in r:
            self.data_set.append([int(row[0]), [int(v) for v in row[1:]]])
        self.__normalize()

    def save_to_csv(self, out):
        w = csv.writer(out, lineterminator='\n')
        for d in self.data_set:
            w.writerow([d[0]] + d[1])

    def __normalize(self):
        attributes_range = [(min(row[1][i] for row in self.data_set), max(row[1][i] for row in self.data_set) + 1) for i in range(0, self.__attributes_count)]
        # Normalizacja
        self.data_set = [[row[0], [(v - minv)/(maxv - minv) for (minv, maxv), v in zip(attributes_range, row[1])]] for row in self.data_set]
        # Zamiana na symbole
        self.data_set = [[row[0], [self.symbols[int(v * self.__symbols_count)] for v in row[1]]] for row in self.data_set]
