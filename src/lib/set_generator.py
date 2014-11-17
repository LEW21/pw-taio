import csv
import random
import sys


class DataSetGenerator:
    test_set_size_factor = 1/3
    attribute_range = (0, 20)

    def __init__(self, classes_count, attributes_count, rows_per_class, sigma_absolute=0.2):
        self.classes_count = classes_count
        self.classes = [i for i in range(0, classes_count)]
        self.attributes_count = attributes_count
        self.rows_per_class = rows_per_class
        self.sigma_absolute = sigma_absolute
        self.class_representative = self._generate_representatives(classes_count, attributes_count)

    def _generate_representatives(self, classes_count, attributes_count):
        min_attribute = self.attribute_range[0]
        max_attribute = self.attribute_range[1]
        class_representative = {}
        for i in range(0, classes_count):
            class_representative[i] = [random.randrange(min_attribute, max_attribute)
                                       for _ in range(0, attributes_count)]
        return class_representative

    def generate_learning_set(self):
        return self.generate_set(self.rows_per_class)

    def generate_test_set(self):
        test_set_size = int(self.rows_per_class * self.test_set_size_factor)
        return self.generate_set(test_set_size)

    def generate_set(self, rows_per_class):
        data_set = []
        for class_number in range(0, self.classes_count):
            representative = self.class_representative[class_number]
            for i in range(0, rows_per_class):
                element_attributes = [random.normalvariate(attribute, self.sigma_absolute)
                                      for attribute in representative]
                data_set.append([class_number, element_attributes])
        return data_set

    def save_to_csv(self, data_set, out=sys.stdout):
        w = csv.writer(out, lineterminator='\n')
        for element in data_set:
            class_number = element[0]
            attributes = element[1]
            w.writerow([class_number] + attributes)
