from pyswarm import pso


class Optimizer:
    swarm_iterations_number = 20
    swarm_size = 40

    @property
    def states_count(self):
        return len(self.classes)

    def __init__(self, automata, data_set, symbols, classes):
        self.automata = automata
        self.data_set = data_set
        self.symbols = symbols
        self.classes = classes

    def optimize(self):
        xopt, fopt = pso(
            func=self._classifier_error, lb=self.automata.vector_lb, ub=self.automata.vector_ub,
            maxiter=self.swarm_iterations_number,
            kwargs={'learning_data_set': self.data_set},
            swarmsize=self.swarm_size,
            debug=True)
        print('xopt (optymalny znaleziony wektor) = \n', xopt)
        print('fopt (najmniejsza znaleziona wartość dla wektora) = ', fopt)
        self.automata.vector = xopt

    def _classifier_error(self, automata_vector, learning_data_set):
        self.automata.vector = automata_vector
        mismatch_count = self.automata.calculate_error(learning_data_set)
        return mismatch_count
