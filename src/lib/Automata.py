__author__ = 'skoczekam'
import random

class Automata(object):
    """Private automata's members"""
    __matrix = {}
    __state = []
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
            self.__matrix[s] = [[0 for j in range(0, self.__noOfClasses)] for i in range(0, self.__noOfClasses)]
        r = [[random.randint(0, self.__noOfClasses - 1) for i in range(0, self.__noOfClasses)] for s in symbols]
        for k, s in enumerate(symbols):
            for j in range(0, self.__noOfClasses):
                self.__matrix[s][r[k][j]][j] = 1

    """
    Initializes beginning state
    """
    def __initState(self):
        self.__state = [0 for i in range(0, self.__noOfClasses)]
        self.__state[0] = 1;

    """
    Get the matrix of the initialized automata
    :returns int{}[][] automata's matrix
    """
    def getMatrix(self):
        return self.__matrix

    """
    Set the matrix of the initialized automata
    :param int{}[][] automata's matrix
    """
    def setMatrix(self, matrix):
        self.__matrix = matrix

    """
    Get the state of the automata
    :returns int[] automata's state
    """
    def getState(self):
        return self.__state

    """
    Set the state of the automata
    :param int[] state the desired state
    """
    def setState(self, state):
        self.__state = state

    """
    Advance automata by one char
    :param int char consumable character from input
    """
    def advance(self, char):
        outState = [0 for i in range(0, self.__noOfClasses)]
        for i in range(0, self.__noOfClasses):
            for j, st in enumerate(self.__state):
                if st < self.__matrix[char][i][j] and st > outState[i]:
                    outState[i] = st
                elif st >= self.__matrix[char][i][j] and self.__matrix[char][i][j] > outState[i]:
                    outState[i] = self.__matrix[char][i][j]
        self.__state = outState

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
        v = [];
        for s in self.__symbols:
            for i in range(0, self.__noOfClasses):
                for j in range(0, self.__noOfClasses):
                    v.append(self.__matrix[s][i][j])
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
            self.__matrix[symb][i][j] = val

    """
    Calculates how many times the automata gets to the wrong state
    :param set set records of classes and their properties
    """
    def calculateError(self, set):
        cnt = 0
        for row in set:
            self.__initState()
            self.consume(row[1])
            for k, i in enumerate(self.__state):
                if i == 1:
                    if row[0] != self.__classes[k]:
                        cnt += 1
                        break
        return cnt