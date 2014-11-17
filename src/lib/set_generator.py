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

    def save_to_csv(self, out):
        w = csv.writer(out, lineterminator='\n')
        for i in range(0, self.rows_per_class):
            class_number = random.randrange(0, self.classes_count)
            element_class_identifier = [str(class_number)]
            element_attributes = [str(int(random.normalvariate(x, self.sigma_absolute)))
                                  for x in self.class_representative[class_number]]
            w.writerow(element_class_identifier + element_attributes)

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
                element_attributes = [int(random.normalvariate(attribute, self.sigma_absolute))
                                      for attribute in representative]
                data_set.append([class_number, element_attributes])
        return data_set
