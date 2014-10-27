__author__ = 'skoczekam'
import random


class Automata(object):
    """Private automata's members"""
    matrix = {}
    state = []
    __symbols = []
    __noOfClasses = []
    __classes = []

    """
    Initialize DFA automata's matrix, so there is one "1" for each column, for each symbol
    :param char[] symbols consumable symbols
    :param string[] classes number of generated classes (automata's states)
    """
    def __init__(self, symbols, classes):
        self.__symbols = symbols
        self.__classes = classes
        self.__noOfClasses = len(classes)
        for s in symbols:
            self.matrix[s] = [[0 for j in range(0, self.__noOfClasses)] for i in range(0, self.__noOfClasses)]
        r = [[random.randint(0, self.__noOfClasses - 1) for i in range(0, self.__noOfClasses)] for s in symbols]
        for k, s in enumerate(symbols):
            for j in range(0, self.__noOfClasses):
                self.matrix[s][r[k][j]][j] = 1

    """
    Initializes beginning state
    """
    def __initState(self):
        self.state = [0 for i in range(0, self.__noOfClasses)]
        self.state[0] = 1

    """
    Advance automata by one char
    :param int char consumable character from input
    """
    def advance(self, char):
        outState = [0 for i in range(0, self.__noOfClasses)]
        for i in range(0, self.__noOfClasses):
            for j, st in enumerate(self.state):
                if st < self.matrix[char][i][j] and st > outState[i]:
                    outState[i] = st
                elif st >= self.matrix[char][i][j] and self.matrix[char][i][j] > outState[i]:
                    outState[i] = self.matrix[char][i][j]
        self.state = outState

    """
    Consume the given word
    :param string string given word
    """
    def consume(self, string):
        self.__initState()
        for char in string:
            self.advance(char)

    """
    Get the automata's matrix as a vector
    :returns int[] vector of the matrix
    """
    def getVector(self):
        v = []
        for s in self.__symbols:
            for i in range(0, self.__noOfClasses):
                for j in range(0, self.__noOfClasses):
                    v.append(self.matrix[s][i][j])
        return v

    """
    Set the automata's matrix as a vector
    :returns int[] vector of the matrix
    """
    def setVector(self, v):
        noOfClasses2 = self.__noOfClasses ** 2
        for k, val in enumerate(v):
            ind = int(k / noOfClasses2)
            symb = self.__symbols[ind]
            inCur = k - ind * noOfClasses2
            i = int(inCur / self.__noOfClasses)
            j = int(inCur % self.__noOfClasses)
            self.matrix[symb][i][j] = val

    """
    Calculates how many times the automata gets to the wrong state
    :param set set records of classes and their properties
    """
    def calculateError(self, set):
        missCount = 0
        for row in set:
            self.__initState()
            self.consume(row[1])
            for k, i in enumerate(self.state):
                if i == 1:
                    if row[0] != self.__classes[k]:
                        missCount += 1
                        break
        return missCount
