__author__ = 'skoczekam'
import random


class Automata:
    matrix = {}
    state = []
    __symbols = []
    __classes_count = []
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
        self.__classes_count = len(classes)
        for s in symbols:
            self.matrix[s] = [[0 for j in range(0, self.__classes_count)] for i in range(0, self.__classes_count)]
        r = [[random.randint(0, self.__classes_count - 1) for i in range(0, self.__classes_count)] for s in symbols]
        for k, s in enumerate(symbols):
            for j in range(0, self.__classes_count):
                self.matrix[s][r[k][j]][j] = 1

    def __init_state(self):
        """Initialize beginning state."""
        self.state = [0 for i in range(0, self.__classes_count)]
        self.state[0] = 1

    def advance(self, char):
        """Advance automata by one char.

        :param char: consumable character from input
        :type char: str
        """
        out_state = [0 for i in range(0, self.__classes_count)]
        for i in range(0, self.__classes_count):
            for j, st in enumerate(self.state):
                if self.matrix[char][i][j] > st > out_state[i]:
                    out_state[i] = st
                elif st >= self.matrix[char][i][j] > out_state[i]:
                    out_state[i] = self.matrix[char][i][j]
        self.state = out_state

    def consume(self, word):
        """Consume the given word.

        :param word: given word
        :type word: list[str]
        """
        self.__init_state()
        for char in word:
            self.advance(char)

    def get_vector(self):
        """Get the automata's matrix as a vector.

        :returns: vector of the matrix
        :rtype: list[int]
        """
        v = []
        for s in self.__symbols:
            for i in range(0, self.__classes_count):
                for j in range(0, self.__classes_count):
                    v.append(self.matrix[s][i][j])
        return v

    def set_vector(self, v):
        """Set the automata's matrix as a vector.

        :type v: list[int]
        """
        no_of_classes2 = self.__classes_count ** 2
        for k, val in enumerate(v):
            ind = int(k / no_of_classes2)
            symb = self.__symbols[ind]
            in_cur = k - ind * no_of_classes2
            i = int(in_cur / self.__classes_count)
            j = int(in_cur % self.__classes_count)
            self.matrix[symb][i][j] = val

    def calculate_error(self, data_set):
        """Calculate how many times the automata gets to the wrong state.

        :param data_set: records of classes and their properties
        :type data_set: list
        :rtype: int
        """
        miss_count = 0
        for row in data_set:
            self.__init_state()
            self.consume(row[1])
            for k, i in enumerate(self.state):
                if i == 1:
                    if row[0] != self.__classes[k]:
                        miss_count += 1
                        break
        return miss_count

    def get_matrix_column(self, symbol, column_number):
        column = []
        for row in self.matrix[symbol]:
            column.append(row[column_number])
        return column

    def reassign_matrix_column(self, symbol, column_number, selected_row_number):
        for rowIndex, row in enumerate(self.matrix[symbol]):
            if rowIndex == selected_row_number:
                value = 1
            else:
                value = 0
            row[column_number] = value
