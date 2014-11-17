import csv
import sys


class Normalizer:
    def __init__(self, symbols_count, data_set):
        self.data_set = data_set
        self.symbols = [chr(int(ord("a") + i)) for i in range(0, symbols_count)]
        self._symbols_count = symbols_count
        self._attributes_count = len(data_set[0][1])
        self._normalize()

    def load_from_csv(self, csv_file):
        reader = csv.reader(csv_file)
        self.data_set = []
        for row in reader:
            class_number = int(row[0])
            attributes = [int(attribute) for attribute in row[1:]]
            self.data_set.append([class_number, attributes])
        self._normalize()

    def save_to_csv(self, out=sys.stdout):
        writer = csv.writer(out, lineterminator='\n')
        for element in self.data_set:
            class_number = element[0]
            attributes = element[1]
            writer.writerow([class_number] + attributes)

    def _normalize(self):
        attributes_range = [(min(row[1][i] for row in self.data_set), max(row[1][i] for row in self.data_set) + 1) for i in range(0, self._attributes_count)]
        # Normalizacja
        self.data_set = [[row[0], [(v - minv)/(maxv - minv) for (minv, maxv), v in zip(attributes_range, row[1])]] for row in self.data_set]
        # Zamiana na symbole
        self.data_set = [[row[0], [self.symbols[int(v * self._symbols_count)] for v in row[1]]] for row in self.data_set]
