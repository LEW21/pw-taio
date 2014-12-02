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
Fuzzy = 3

class Automata:
    type = Deterministic

    matrix = {}
    __symbols = []
    __classes = []

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

        self.__initial_state = numpy.array([1] + [0] * (len(classes)-1))
        self.__empty_state = numpy.array([0] * len(classes))

    def consume(self, word):
        """Consume the given word.

        :param word: given word
        :type word: list[str]
        :returns: final state vector
        :rtype: list[int]
        """
        state = self.__initial_state
        for char in word:
            state = numpy.dot(self.matrix[char], state)
            if self.type == Nondeterministic:
                state_num = random.choice([x[0] for x in enumerate(state) if x[1]])
                state = self.__empty_state.copy()
                state[state_num] = 1
            elif self.type == Fuzzy:
                state = normalize(state, self.__initial_state)

        return state

    """Min function for 2 ints

    :param a: given float
    :type a: float
    :param b: given float
    :type b: float
    :returns: min
    :rtype: float
    """
    def min_f(self, a, b):
        return 1 - math.tanh(math.atanh(1 - a) + math.atanh(1 - b));

    """Max function for vector

    :param vec: given vector of floats
    :type vec: list[float]
    :returns: max
    :rtype: float
    """
    def max_f(self, vec):
        sum = 0
        for v in vec:
            sum += math.atanh(v)
        return math.tanh(sum);

    """Min function for float and vector

    :param a: given float
    :type a: float
    :param vec: given vector of floats
    :type vec: list[float]
    :returns: min
    :rtype: float
    """
    def min_vec(self, a, vec):
        outV = [0 for i in range(0, len(vec))]
        for key, num in enumerate(vec):
            outV[key] = self.min_f(a, num)
        return outV

    """max function for vectors

    :param a: given float
    :type a: float
    :param vecTab: given array of vectors
    :type vecTab: list[list[float]]
    :returns: max
    :rtype: list[float]
    """
    def max_vecs(self, vecTab):
        cnt = len(vecTab[0])
        outV = [0 for i in range(0, cnt)]
        for i in range(0, cnt):
            sum = 0
            for v in vecTab:
                sum += math.atanh(v[i])
                outV[i] = sum
            outV[i] = math.tanh(outV[i])
        return outV

    """Given the vector of floats (symbol in previous stages) for each calculate
    the out state using above min and max functions. Having vector from each calculation
    perform on each min with the symbol used in calculation of the particular state vector
    and then max on the result vectors

    :param vec: input vector
    :type vec: list[float]
    """
    # def advanceVec(self, vec):
        # for val in vec:
        #     ...


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
                    # Add at least one, and stop if (n+1)th is >2 times smaller than the n-th one.
                    for val in vals:
                        if 2*column[val] < column[prev_val]:
                            break
                        self.matrix[s][val][j] = 1
                        prev_val = val
                else: # Fuzzy
                    for i in range(0, len(self.__classes)):
                        self.matrix[s][i][j] = next(it)

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
            state = self.consume(row[1])
            if not binary:
                for class_, probability in zip(self.__classes, state):
                    if row[0] != class_:
                        miss_count += probability**2
            else:
                if row[0] != max(zip(self.__classes, state), key=lambda x: x[1])[0]:
                    miss_count += 1
        self.matrix = matrix_bak
        return miss_count
