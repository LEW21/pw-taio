__author__ = 'skoczekam'
import random
import numpy
import math

def normalize(v, default):
    s = sum(v)
    if s == 0:
        return default
    else:
        return v / s

Deterministic = 1
Nondeterministic = 2

class Automata:
    type = Deterministic

    matrix = {}
    __symbols = []
    __classes = []
    nondet_limit = 0.2

    def __init__(self, symbols, classes):
        """Initialize DFA automata's matrix, so there is one "1" for each column, for each symbol.

        :param symbols: consumable symbols
        :type symbols: list[str]
        :param classes: number of generated classes (automata's states)
        :type classes: list[int]
        """
        self.__symbols = symbols
        self.__classes = classes

        self.vector = [random.randint(0, len(classes) - 1) for i in range(0, len(classes) * len(symbols))]

        self.__initial_state = numpy.array([1.0] + [0.0] * (len(classes)-1))
        self.__empty_state = numpy.array([0.0] * len(classes))

    def consume(self, word):
        """Consume the given word.

        :param word: given word
        :type word: list[str]
        :returns: final state vector
        :rtype: list[int]
        """
        state = self.__initial_state
        for char in word:
            #state = self.advance_slow(state, char)
            if type(char) == list:
                new_state = self.__empty_state.copy()
                for sym, prob in zip(self.__symbols, char):
                    new_state += numpy.multiply(prob, numpy.dot(self.matrix[sym], state))
                state = normalize(new_state, self.__initial_state)
            else:
                state = numpy.dot(self.matrix[char], state)
            if self.type == Nondeterministic:
                state_num = random.choice([x[0] for x in enumerate(state) if x[1]])
                state = self.__empty_state.copy()
                state[state_num] = 1

        return state

    def consume_slow(self, word):
        """Consume the given word.

        :param word: given word
        :type word: list[str]
        :returns: final state vector
        :rtype: list[int]
        """
        state = self.__initial_state
        for char in word:
            #state = self.advance_slow(state, char)
            if type(char) == list:
                # new_state = self.__empty_state.copy()
                new_state = []
                for sym, prob in zip(self.__symbols, char):
                    # new_state = self.__empty_state.copy()
                    new_state.append(self.min_a_vec(prob, self.advance_slow(state, sym)))
                state = self.max_vec_list(new_state);
                # state = normalize(new_state, self.__initial_state)
            else:
                state = numpy.dot(self.matrix[char], state)
            if self.type == Nondeterministic:
                state_num = random.choice([x[0] for x in enumerate(state) if x[1]])
                state = self.__empty_state.copy()
                state[state_num] = 1

        return state

    def advance_slow(self, state, char):
        return [self.max_f([self.min_f(self.matrix[char][i][j], st) for j, st in enumerate(state)]) for i in range(0, len(self.__classes))]

    def min_f(self, a, b):
        if(a >= 2):
            a = 1.99
        if(a <= 0):
            a = 0.01
        if(b >= 2):
            b = 1.99
        if(b <= 0):
            b = 0.01
        return 1 - math.tanh(math.atanh(1 - a) + math.atanh(1 - b));

    def max_f(self, vec):
        sum = 0
        for v in vec:
            if(v >= 1):
                v = 0.99
            if(v <= -1):
                v = -0.99
            sum += math.atanh(v)
        return math.tanh(sum);

    def min_a_vec(self, a, vec):
        return [self.min_f(a, vec[i]) for i in range(0, len(vec))]

    def max_vec_list(self, list):
        cnt = len(list[0])
        cntVec = len(list)
        outVec = [0 for i in range(0, cnt)]
        for i in range(0, cnt):
            for j in range(0, cntVec):
                if(list[j][i] >= 1):
                    list[j][i] = 0.99
                if(list[j][i] <= -1):
                    list[j][i] = -0.99
                outVec[i] += math.atanh(list[j][i])
            outVec[i] = math.tanh(outVec[i])
        return outVec

    @property
    def vector_lb(self):
        return [0] * (len(self.__symbols) * len(self.__classes) * len(self.__classes))

    @property
    def vector_ub(self):
        return [1] * (len(self.__symbols) * len(self.__classes) * len(self.__classes))

    @property
    def vector(self):
        """Get the automata's matrix as a vector.

        :returns: vector of the matrix
        :rtype: list[int]
        """
        v = []

        for s in self.__symbols:
            for j in range(0, len(self.__classes)):
                for i in range(0, len(self.__classes)):
                    v.append(self.matrix[s][i][j])

        return v

    @vector.setter
    def vector(self, v):
        """Set the automata's matrix as a vector.

        :type v: list[int]
        """
        is_compact_vector = len(v) == len(self.__symbols) * len(self.__classes)

        it = iter(v)
        for s in self.__symbols:
            self.matrix[s] = [[0] * len(self.__classes) for i in range(0, len(self.__classes))]
            for j in range(0, len(self.__classes)):
                if is_compact_vector:
                    self.matrix[s][next(it)][j] = 1
                elif self.type == Deterministic:
                    column = [next(it) for i in range(0, len(self.__classes))]
                    val = max(range(0, len(self.__classes)), key=lambda p: column[p])
                    self.matrix[s][val][j] = 1
                elif self.type == Nondeterministic:
                    column = [next(it) for i in range(0, len(self.__classes))]
                    vals = sorted(range(0, len(self.__classes)), key=lambda p: column[p], reverse=True)
                    prev_val = 0
                    for val in vals[:int(self.nondet_limit*len(vals))]:
                        self.matrix[s][val][j] = 1
                        prev_val = val

    def consume_dataset(self, data_set, choose_best=False):
        """Consume the whole data set, and return 

        :param data_set: records of classes and their properties
        :type data_set: list
        :rtype: int[] if choose_best else int[][]
        """
        matrix_bak = self.matrix
        self.matrix = {s: numpy.array(self.matrix[s]) for s in self.__symbols}
        for row in data_set:
            state = self.consume_slow(row[1])
            if choose_best:
                yield max(zip(self.__classes, state), key=lambda x: x[1])[0]
            else:
                yield state
        self.matrix = matrix_bak

    def calculate_error(self, data_set, binary=False):
        """Calculate how many times the automata gets to the wrong state.

        :param data_set: records of classes and their properties
        :type data_set: list
        :rtype: int
        """
        miss_count = 0
        matrix_bak = self.matrix
        self.matrix = {s: numpy.array(self.matrix[s]) for s in self.__symbols}
        for row in data_set:
            state = self.consume_slow(row[1])
            if not binary:
                for class_, probability in zip(self.__classes, state):
                    if row[0] != class_:
                        miss_count += probability**2
            else:
                if row[0] != max(zip(self.__classes, state), key=lambda x: x[1])[0]:
                    miss_count += 1
        self.matrix = matrix_bak
        return miss_count
