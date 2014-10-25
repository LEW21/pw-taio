import csv
import argparse
import random

class Norm(object):
    __symbole = 0
    __symboleTab = []
    __zbior = []
    __cechy = 0

    def __init__(self, symbole, zbior):
        self.__symbole = symbole
        self.__zbior = zbior
        self.__cechy = len(zbior[0][1])
        self.__symboleTab = [chr(int(ord("a") + i)) for i in range(0, self.__symbole)]
        self.__normalizuj()

    def czytajZCSV(self, input):
        r = csv.reader(input)
        self.__zbior = []
        for row in r:
            self.__zbior.append([int(row[0]), [int(v) for v in row[1:]]])
        self.__normalizuj()

    def zapiszJakoCSV(self, out):
        w = csv.writer(out, lineterminator='\n')
        for d in self.__zbior:
	        w.writerow([d[0]] + d[1])

    def __normalizuj(self):
        minmax_cech = [(min(row[1][i] for row in self.__zbior), max(row[1][i] for row in self.__zbior) + 1) for i in range(0, self.__cechy)]
        # Normalizacja
        self.__zbior = [[row[0], [(v - minv)/(maxv - minv) for (minv, maxv), v in zip(minmax_cech, row[1])]] for row in self.__zbior]
        # Zamiana na symbole
        self.__zbior = [[row[0], [self.__symboleTab[int(v * self.__symbole)] for v in row[1]]] for row in self.__zbior]

    def getZbior(self):
        return self.__zbior

    def getSymboleTab(self):
        return self.__symboleTab