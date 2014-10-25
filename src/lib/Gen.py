import csv
import sys
import argparse
import random


class Gen(object):
    __klasy = 0
    __klasyTab = []
    __cechy = 0
    __wiersze = 0
    __sigmaAbs = 0
    __sigmaRel = 0
    __zakresCech = 0
    __D = {}

    def __init__(self, klasy, cechy, wiersze, sigmaAbs=10, sigmaRel=0.1):
        self.__klasy = klasy
        self.__klasyTab = [i for i in range(0, klasy)]
        self.__cechy = cechy
        self.__wiersze = wiersze
        self.__sigmaAbs = sigmaAbs
        self.__sigmaRel = sigmaRel
        self.__zakresCech = [self.__randZakres() for j in range(0, cechy)]
        for i in range(0, klasy):
            self.__D[i] = [random.randrange(min, max) for min, max in self.__zakresCech]

    def __randZakres(self):
        # Dlaczego sigma jako minimum? Bo chcę, żeby ujemnych wartości było relatywnie mało - nie są specjalnie oczekiwanym wynikiem normalnych pomiarów.
        zakres = sorted([random.randrange(self.__sigmaAbs, 1000), random.randrange(self.__sigmaAbs, 1000)])
        if zakres[0] != zakres[1]:
            return zakres
        return self.__randZakres()

    def wypiszSigmyAbs(self):
        for i, (vmin, vmax) in enumerate(self.__zakresCech):
            print("Sigma absolutna cechy " + str(i) + ": " + str(round(self.__sigmaAbs + self.__sigmaRel * (vmax - vmin), 2)), file=sys.stderr)

    def wypiszSigmyRel(self):
        for i, (vmin, vmax) in enumerate(self.__zakresCech):
            print("Sigma relatywna cechy " + str(i) + ": " + str(round(self.__sigmaAbs / (vmax - vmin) + self.__sigmaRel, 2)), file=sys.stderr)

    def zapiszJakoCSV(self, out):
        w = csv.writer(out, lineterminator='\n')
        for i in range(0, self.__wiersze):
            k = random.randrange(0, self.__klasy)
            w.writerow([str(k)] + [str(int(random.normalvariate(x, self.__sigmaAbs + self.__sigmaRel * (xmax - xmin)))) for x, (xmin, xmax) in zip(self.__D[k], self.__zakresCech)])

    def generujZbior(self):
        zbior = []
        for i in range(0, self.__wiersze):
            k = random.randrange(0, self.__klasy)
            # w.writerow([str(k)] + [str(int(random.normalvariate(x, self.__sigmaAbs + self.__sigmaRel * (xmax - xmin)))) for x, (xmin, xmax) in zip(self.__D[k], self.__zakresCech)])
            zbior.append([k, [int(random.normalvariate(x, self.__sigmaAbs + self.__sigmaRel * (xmax - xmin))) for x, (xmin, xmax) in zip(self.__D[k], self.__zakresCech)]])
        return zbior

    def getKlasy(self):
        return self.__klasy

    def getKlasyTab(self):
        return self.__klasyTab

    def getD(self):
        return self.__D