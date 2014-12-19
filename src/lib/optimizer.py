from pyswarm import pso


class Optimizer:
    @property
    def states_count(self):
        return len(self.classes)

    def __init__(self, automata, data_set, symbols, classes):
        self.automata = automata
        self.data_set = data_set
        self.symbols = symbols
        self.classes = classes

    def optimize(self, control):
        xopt, fopt = pso(
            func=self._classifier_error, lb=self.automata.vector_lb, ub=self.automata.vector_ub,
            maxiter=control["maxit"],
            swarmsize=control["s"],
            debug=True)
        print('xopt (optymalny znaleziony wektor) = \n', xopt)
        print('fopt (najmniejsza znaleziona wartość dla wektora) = ', fopt)
        self.automata.vector = xopt

    def _classifier_error(self, automata_vector):
        self.automata.vector = automata_vector
        mismatch_count = self.automata.calculate_error(self.data_set)
        return mismatch_count
