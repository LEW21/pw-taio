import random


def generate_representatives(classes_count, attributes_count, attribute_range):
    class_representatives = []
    for i in range(0, classes_count):
        attrs = [random.randrange(*attribute_range) for _ in range(0, attributes_count)]
        class_representatives.append(attrs)
    return class_representatives


def generate_dataset(rows_per_class, representatives, attribute_range, sigma):
    data_set = []
    for class_number, representative in enumerate(representatives):
        for i in range(0, rows_per_class):
            element_attributes = [round(random.normalvariate(attribute, sigma))
                                  for attribute in representative]
            data_set.append((class_number, element_attributes))
    return data_set


def generate_foreign_unified(rows, representatives, attribute_range, sigma):
    data_set = []
    for i in range(0, rows):
        attrs = [round(random.randrange(*attribute_range)) for _ in representatives[0]]
        data_set.append(attrs)
    return data_set


def generate_foreign_permuted(rows, representatives, attribute_range, sigma):
    data_set = []
    for i in range(0, rows):
        attrs = []
        for _ in representatives[0]:
            representative = random.choice(representatives)
            attr = random.choice(representative)
            attrs.append(attr)
        data_set.append(attrs)
    return data_set
