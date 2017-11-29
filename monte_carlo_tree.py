#TODO: FINISH THIS
import random
from state import State

class FakeRandomNet:

    def get_move_probability(self, state, move):
        return random.uniform(0, 1)
    def evaluate_state(self, state):
        return random.uniform(0, 1)

class MonteCarloTreeEdge:
    # might not need parent
    U_CONSTANT = 1
    def __init__(self, parent_node, child_node, action, probability):
        self.N = 0
        self.W = 0
        self.Q = 0
        self.P = probability
        self.a = action
        self.parent_node = parent_node
        self.child_node = child_node
    def backprop_thru(self, dw):
        self.N += 1
        self.W += dw
        self.update_Q()
    def update_Q(self):
        self.Q = float(self.W)/float(self.N)
    def calculate_U(self):
        return U_CONSTANT * self.P/(1 + self.N)
    def __str__(self):
        return 'N: {}, W: {}, Q: {}, P: {}, a: {}'.format(self.N, self.W, self.Q, self.P, self.a)

class MonteCarloTreeNode:
    def __init__(self, state, evaluator):
        self.state = state
        self.v = evaluator.evaluate_state(state)
        self.edges = []
        self.evaluator = evaluator
    def is_leaf(self):
        return not len(self.edges)
    def expand(self):
        for pair in self.state.legal_moves():
            new_state = pair[1]
            move = pair[0]
            # evaluate move using evaluator, store probability in new edge
            new_edge = MonteCarloTreeEdge(self, MonteCarloTreeNode(new_state, self.evaluator), move, self.evaluator.get_move_probability(self.state, move))
            self.edges.append(new_edge)
        self.backprop_to_root()
# m = MonteCarloTreeEdge(0, 0, (2,4), .3592888009)
# print(m)
# for i in range(3):
#     m.backprop_thru(1)
# m.backprop_thru(0)
# print(m)
s = State()
net = FakeRandomNet()
s.pretty_print()
n = MonteCarloTreeNode(s, net)
print(n.is_leaf())
n.expand()
print(n.is_leaf())
for edge in n.edges:
    edge.child_node.state.pretty_print()
