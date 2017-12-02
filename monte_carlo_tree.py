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

# action is the move associated with this edge
    # probability is the probability of that move
    def __init__(self, parent_node, child_node, action, probability):
        self.N = 0
        self.W = 0
        self.Q = 0
        self.P = probability
        self.a = action
        self.U_constant = 1
        self.parent_node = parent_node
        self.child_node = child_node

    # dw is the change in our W that we carry with us when backproping
    # i.e. it's the evaluation of the leaf node we expanded
    def backprop_thru(self, dw):
        self.N += 1
        self.W += dw
        self.update_Q()
    def update_Q(self):
        self.Q = float(self.W)/float(self.N)
    def calculate_U(self):
        return self.U_constant * self.P/(1 + self.N)
    def __str__(self):
        return 'N: {}, W: {}, Q: {}, P: {}, a: {}, U: {}'.format(self.N, self.W, self.Q, self.P, self.a, self.calculate_U())

class MonteCarloTreeNode:
    
    # evaluator will be the neural net
    def __init__(self, state, evaluator, parent_edge):
        self.state = state
        self.v = evaluator.evaluate_state(state)
        self.parent_edge = parent_edge
        self.edges = []
        self.evaluator = evaluator
    
    def is_leaf(self):
        return not len(self.edges)

    def is_game_over(self):
        pass
        # self.state.is_game_over


    def choose_next_node(self):
        return max(self.edges, key=lambda e: e.calculate_U()).child_node
        # return random.choice(self.edges).child_node

    def expand(self):
        """
        legals = []
        c = False
        while not c:
            try:
                legals = self.state.legal_moves()
                c = True
            except IndexError:
                c = False
        """
        legals = self.state.legal_moves()
        for new_state in legals:
            # evaluate move using evaluator, store probability in new edge
            new_node = MonteCarloTreeNode(new_state, self.evaluator, None)
            new_edge = MonteCarloTreeEdge(self, new_node, new_node.state.last_move, self.evaluator.get_move_probability(self.state, new_node.state.last_move))
            new_node.parent_edge = new_edge
            self.edges.append(new_edge)

class MonteCarloTree:
    
    def __init__(self, state, evaluator):
        self.state = state
        self.evaluator = evaluator
        self.root = MonteCarloTreeNode(state, evaluator, None)
        self.player_id = self.root.state.to_move 
    def perform_search(self):
        cur_node = self.root
        #print(cur_node)
        print("\n\nSEARCHING")
    
        while not cur_node.is_leaf():
            cur_node.state.pretty_print()
            cur_node = cur_node.choose_next_node()
    
    # cur_node is leaf
        #if cur_node.is_game_over():
        cur_node.expand()
        print("expanding:")
        cur_node.state.pretty_print()
        # begin backprop
        cur_edge = cur_node.parent_edge
        dw = cur_node.v
        while cur_edge: # while cur_node isn't root
            #print(cur_edge)
            cur_edge.backprop_thru(dw)
            cur_node = cur_edge.parent_node
            cur_edge = cur_node.parent_edge


s = State()
net = FakeRandomNet()
tree = MonteCarloTree(s, net)
for i in range(10000):
    for edge in tree.root.edges:
        print(edge)
    tree.perform_search()
for edge in tree.root.edges:
    print(edge)


"""
when you arrive at a state that is the end of the game, backprop the value as a hard win or loss value. do not expand. that is all. have a great day :)


"""
