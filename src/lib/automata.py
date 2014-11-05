__author__ = 'skoczekam'
import random


class Automata(object):
    matrix = {}
    state = []
    __symbols = []
    __noOfClasses = []
    __classes = []

    def __init__(self, symbols, classes):
        """
        Initialize DFA automata's matrix, so there is one "1" for each column, for each symbol.

        :param symbols: consumable symbols
        :type symbols: list[str]
        :param classes: number of generated classes (automata's states)
        :type classes: list[int]
        """
        self.__symbols = symbols
        self.__classes = classes
        self.__noOfClasses = len(classes)
        for s in symbols:
            self.matrix[s] = [[0 for j in range(0, self.__noOfClasses)] for i in range(0, self.__noOfClasses)]
        r = [[random.randint(0, self.__noOfClasses - 1) for i in range(0, self.__noOfClasses)] for s in symbols]
        for k, s in enumerate(symbols):
            for j in range(0, self.__noOfClasses):
                self.matrix[s][r[k][j]][j] = 1

    def __initState(self):
        """Initialize beginning state."""
        self.state = [0 for i in range(0, self.__noOfClasses)]
        self.state[0] = 1

    def advance(self, char):
        """Advance automata by one char.

        :param char: consumable character from input
        :type char: str
        """
        outState = [0 for i in range(0, self.__noOfClasses)]
        for i in range(0, self.__noOfClasses):
            for j, st in enumerate(self.state):
                if self.matrix[char][i][j] > st > outState[i]:
                    outState[i] = st
                elif st >= self.matrix[char][i][j] > outState[i]:
                    outState[i] = self.matrix[char][i][j]
        self.state = outState

    def consume(self, word):
        """Consume the given word.

        :param word: given word
        :type word: list[str]
        """
        self.__initState()
        for char in word:
            self.advance(char)

    def getVector(self):
        """Get the automata's matrix as a vector.

        :returns: vector of the matrix
        :rtype: list[int]
        """
        v = []
        for s in self.__symbols:
            for i in range(0, self.__noOfClasses):
                for j in range(0, self.__noOfClasses):
                    v.append(self.matrix[s][i][j])
        return v

    def setVector(self, v):
        """Set the automata's matrix as a vector.

        :type v: list[int]
        """
        noOfClasses2 = self.__noOfClasses ** 2
        for k, val in enumerate(v):
            ind = int(k / noOfClasses2)
            symb = self.__symbols[ind]
            inCur = k - ind * noOfClasses2
            i = int(inCur / self.__noOfClasses)
            j = int(inCur % self.__noOfClasses)
            self.matrix[symb][i][j] = val

    def calculateError(self, set):
        """Calculate how many times the automata gets to the wrong state.

        :param set: records of classes and their properties
        :type set: list
        :rtype: int
        """
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

    def getMatrixColumn(self, symbol, columnNumber):
        column = []
        for row in self.matrix[symbol]:
            column.append(row[columnNumber])
        return column

    def reassignMatrixColumn(self, symbol, columnNumber, selectedRowNumber):
        for rowIndex, row in enumerate(self.matrix[symbol]):
            if rowIndex == selectedRowNumber:
                value = 1
            else:
                value = 0
            row[columnNumber] = value
