#TODO: FINISH THIS

class MonteCarloTreeEdge:
    # might not need parent
    U_CONSTANT = 1
    def __init__(self, parent_node, child_node, action, probability):
        self.N = 0
        self.W = 0
        self.Q = 0
        self.P = probability
        self.a = action
    def backprop_thru(self, dw):
        self.N += 1
        self.W += dw
        self.Q = self.update_Q()
    def update_Q(self):
        self.Q = float(self.W)/float(self.N)
    def calculate_U(self):
        return U_CONSTANT * self.P/(1 + self.N)

class MonteCarloTreeNode:
    def __init__(self, state, evaluator):
        self.state = state
        self.edges = []
        self.evaluator = evaluator
    def is_leaf(self):
        return not len(self.edges)
    def expand(self):
        for move in state.legalMoves()[1]:
