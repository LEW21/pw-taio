import csv
import random
import sys


class Gen(object):
    klasy = 0
    klasyTab = []
    __cechy = 0
    __wiersze = 0
    __sigmaAbs = 0
    __sigmaRel = 0
    __zakresCech = 0
    D = {}
    wspolczynnikRozmiaruZbioruTestowego = 1/3

    def __init__(self, klasy, cechy, wiersze, sigmaAbs=10, sigmaRel=0.1):
        self.klasy = klasy
        self.klasyTab = [i for i in range(0, klasy)]
        self.__cechy = cechy
        self.__wiersze = wiersze
        self.__sigmaAbs = sigmaAbs
        self.__sigmaRel = sigmaRel
        self.__zakresCech = [self.__randZakres() for j in range(0, cechy)]
        for i in range(0, klasy):
            self.D[i] = [random.randrange(min, max) for min, max in self.__zakresCech]

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
            k = random.randrange(0, self.klasy)
            w.writerow([str(k)] + [str(int(random.normalvariate(x, self.__sigmaAbs + self.__sigmaRel * (xmax - xmin)))) for x, (xmin, xmax) in zip(self.D[k], self.__zakresCech)])

    def generujZbiorUczacy(self):
        return self.generujZbior(self.__wiersze)

    def generujZbiorTestowy(self):
        rozmiarZbioruTestowego = int(self.__wiersze * self.wspolczynnikRozmiaruZbioruTestowego)
        return self.generujZbior(rozmiarZbioruTestowego)

    def generujZbior(self, liczbaElementow):
        zbior = []
        for i in range(0, liczbaElementow):
            k = random.randrange(0, self.klasy)
            # w.writerow([str(k)] + [str(int(random.normalvariate(x, self.__sigmaAbs + self.__sigmaRel * (xmax - xmin)))) for x, (xmin, xmax) in zip(self.D[k], self.__zakresCech)])
            zbior.append([k, [int(random.normalvariate(x, self.__sigmaAbs + self.__sigmaRel * (xmax - xmin))) for x, (xmin, xmax) in zip(self.D[k], self.__zakresCech)]])
        return zbior
