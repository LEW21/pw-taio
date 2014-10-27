import csv


class Norm(object):
    __symbole = 0
    symboleTab = []
    zbior = []
    __cechy = 0

    def __init__(self, symbole, zbior):
        self.__symbole = symbole
        self.zbior = zbior
        self.__cechy = len(zbior[0][1])
        self.symboleTab = [chr(int(ord("a") + i)) for i in range(0, self.__symbole)]
        self.__normalizuj()

    def czytajZCSV(self, input):
        r = csv.reader(input)
        self.zbior = []
        for row in r:
            self.zbior.append([int(row[0]), [int(v) for v in row[1:]]])
        self.__normalizuj()

    def zapiszJakoCSV(self, out):
        w = csv.writer(out, lineterminator='\n')
        for d in self.zbior:
            w.writerow([d[0]] + d[1])

    def __normalizuj(self):
        minmax_cech = [(min(row[1][i] for row in self.zbior), max(row[1][i] for row in self.zbior) + 1) for i in range(0, self.__cechy)]
        # Normalizacja
        self.zbior = [[row[0], [(v - minv)/(maxv - minv) for (minv, maxv), v in zip(minmax_cech, row[1])]] for row in self.zbior]
        # Zamiana na symbole
        self.zbior = [[row[0], [self.symboleTab[int(v * self.__symbole)] for v in row[1]]] for row in self.zbior]
