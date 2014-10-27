from pyswarm import pso


class Optimizer:
    swarmIterationsNumber = 50

    @property
    def states_count(self):
        return len(self.classes)

    def __init__(self, automata, data_set, symbols, classes):
        self.automata = automata
        self.data_set = data_set
        self.symbols = symbols
        self.classes = classes

    def optimize(self):
        automata_vector = self.automata.getVector()
        lower_bound = [0] * len(automata_vector)
        upper_bound = [1] * len(automata_vector)
        xopt, fopt = pso(
            func=self._classifier_error, lb=lower_bound, ub=upper_bound,
            maxiter=self.swarmIterationsNumber,
            kwargs={'learning_data_set': self.data_set},
            debug=False)
        print('xopt (optymalny znaleziony wektor) = \n', xopt)
        print('fopt (najmniejsza znaleziona wartość dla wektora) = ', fopt)
        self._classifier_error(xopt, self.data_set)

    def _classifier_error(self, automata_vector, learning_data_set):
        self.automata.setVector(v=automata_vector)

        for symbol in self.symbols:
            for column_number in range(0, self.states_count):
                column = self.automata.getMatrixColumn(symbol, column_number)
                selected_row = self._select_row_from_column(column)
                self.automata.reassignMatrixColumn(symbol, column_number, selected_row)

        mismatch_count = self.automata.calculateError(learning_data_set)
        return mismatch_count

    def _select_row_from_column(self, column):
        max_index, max_value = max(enumerate(column), key=lambda p: p[1])
        return max_index
