import csv
import sys

def save_to_csv(data_set, out=sys.stdout):
    writer = csv.writer(out, lineterminator='\n')
    for element in data_set:
        class_number = element[0]
        attributes = element[1]
        writer.writerow([class_number] + attributes)

def load_from_csv(csv_file, attr_type):
    reader = csv.reader(csv_file)
    data_set = []
    for row in reader:
        class_number = int(row[0])
        attributes = [attr_type(attribute) for attribute in row[1:]]
        data_set.append([class_number, attributes])
    return data_set

def load_from_csv_file(file):
	return load_from_csv(open(file, "r"))

def load_from_xslx_file(file):
	...

def load_file(file):
	if file.endswith(".xlsx"):
		return load_from_xlsx_file(file)
	elif file.endswith(".csv"):
		return load_from_csv_file(file)
