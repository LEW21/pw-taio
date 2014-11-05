import csv
import random
import sys


class DataSetGenerator(object):
    classes_count = 0
    classes = []
    __attributes_count = 0
    __rows_count = 0
    __sigma_absolute = 0
    __sigma_relative = 0
    __attribute_ranges = 0
    D = {}
    test_set_size_factor = 1/3

    def __init__(self, classes_count, attributes_count, rows_count, sigma_absolute=10, sigma_relative=0.1):
        self.classes_count = classes_count
        self.classes = [i for i in range(0, classes_count)]
        self.__attributes_count = attributes_count
        self.__rows_count = rows_count
        self.__sigma_absolute = sigma_absolute
        self.__sigma_relative = sigma_relative
        self.__attribute_ranges = [self.__generate_range() for j in range(0, attributes_count)]
        for i in range(0, classes_count):
            self.D[i] = [random.randrange(min, max) for min, max in self.__attribute_ranges]

    def __generate_range(self):
        # Dlaczego sigma jako minimum? Bo chcę, żeby ujemnych wartości było relatywnie mało - nie są specjalnie oczekiwanym wynikiem normalnych pomiarów.
        range = sorted([random.randrange(self.__sigma_absolute, 1000), random.randrange(self.__sigma_absolute, 1000)])
        if range[0] != range[1]:
            return range
        return self.__generate_range()

    def print_absolute_sigmas(self):
        for i, (vmin, vmax) in enumerate(self.__attribute_ranges):
            print("Sigma absolutna cechy " + str(i) + ": " + str(round(self.__sigma_absolute + self.__sigma_relative * (vmax - vmin), 2)), file=sys.stderr)

    def print_relative_sigmas(self):
        for i, (vmin, vmax) in enumerate(self.__attribute_ranges):
            print("Sigma relatywna cechy " + str(i) + ": " + str(round(self.__sigma_absolute / (vmax - vmin) + self.__sigma_relative, 2)), file=sys.stderr)

    def save_to_csv(self, out):
        w = csv.writer(out, lineterminator='\n')
        for i in range(0, self.__rows_count):
            k = random.randrange(0, self.classes_count)
            w.writerow([str(k)] + [str(int(random.normalvariate(x, self.__sigma_absolute + self.__sigma_relative * (xmax - xmin)))) for x, (xmin, xmax) in zip(self.D[k], self.__attribute_ranges)])

    def generate_learning_set(self):
        return self.generate_set(self.__rows_count)

    def generate_test_set(self):
        test_set_size = int(self.__rows_count * self.test_set_size_factor)
        return self.generate_set(test_set_size)

    def generate_set(self, elements_count):
        data_set = []
        for i in range(0, elements_count):
            k = random.randrange(0, self.classes_count)
            # w.writerow([str(k)] + [str(int(random.normalvariate(x, self.__sigmaAbs + self.__sigmaRel * (xmax - xmin)))) for x, (xmin, xmax) in zip(self.D[k], self.__zakresCech)])
            data_set.append([k, [int(random.normalvariate(x, self.__sigma_absolute + self.__sigma_relative * (xmax - xmin))) for x, (xmin, xmax) in zip(self.D[k], self.__attribute_ranges)]])
        return data_set
