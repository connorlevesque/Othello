#TODO: FINISH THIS
import random
import torch
from state import State


class Rollouter:
    def get_move_probability(self, state, move):
        return random.uniform(-1, 1)
    def evaluate_state(self, state):
        to_move = state.to_move
        while not state.is_over():
            state = random.choice(state.legal_moves())
        #game is over
        winner = state.score()[0]
        if winner == to_move:
            return 1
        elif winner == 0:
            return 0
        else:
            return -1


class FakeRandomNet:
    def get_move_probability(self, state, move):
        return random.uniform(-1, 1)
    def evaluate_state(self, state):
        return random.uniform(-1, 1)

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
        self.who_moved = parent_node.state.to_move
        self.U_constant = 1
        self.parent_node = parent_node
        self.child_node = child_node

    # dw is the change in our W that we carry with us when backproping
    # i.e. it's the evaluation of the leaf node we expanded
    def backprop_thru(self, dw, evaluated_player):
        self.N += 1
        if evaluated_player == self.who_moved:
            self.W += dw
        else:
            self.W -= dw
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
        if state.is_over():
            # self.v = state.score()[0]
            self.v = 1
        self.v = evaluator.evaluate_state(state)
        #self.is_root = is_root
        self.parent_edge = parent_edge
        self.edges = []
        self.evaluator = evaluator
    
    def is_leaf(self):
        return (not len(self.edges)) or self.is_game_over()

    def is_game_over(self):
        return self.state.is_over()
        # self.state.is_game_over


    def choose_next_node(self):
        #return self.edges[0].child_node
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
        self.working_root = self.root
    
    def perform_search(self):
        cur_node = self.working_root
        #print(cur_node)
        #print("\n\nSEARCHING")
    
        while not cur_node.is_leaf():
            #if cur_node.is_game_over():
             #   break
            # cur_node.state.pretty_print()
            cur_node = cur_node.choose_next_node()
        
        # cur_node is leaf
        hit_end = False
        if not cur_node.is_game_over():
            cur_node.expand()
        else:
            hit_end = True
        #print("expanding:")
        #cur_node.state.pretty_print()
        # begin backprop

        cur_edge = cur_node.parent_edge
        dw = cur_node.v
        to_move = cur_node.state.to_move
        while cur_edge: # while cur_node isn't root
            if hit_end:
                #print(cur_edge)
                pass
                #cur_edge.child_node.state.pretty_print()
            cur_edge.backprop_thru(dw, to_move)
            cur_node = cur_edge.parent_node
            cur_edge = cur_node.parent_edge
    
    def perform_n_searches(self, n):
        for i in range(n):
            self.perform_search()
    
    def choose_move(self):
        return max(self.working_root.edges, key=lambda e: e.N).child_node
    
    def search_and_then_also_move(self, n):
        self.perform_n_searches(n)
        self.update_working_root(self.choose_move())
        return self.choose_move().state

    def update_working_root(self, node):
        self.working_root = node

    def update_working_root_to(self, state):
        next_move = State()
        for edge in self.working_root.edges:
            node = edge.child_node
            if torch.equal(state.board, node.state.board):
                self.update_working_root(node)
                return
"""
s = State()
net = FakeRandomNet()
tree = MonteCarloTree(s, net)

while not s.is_over():
    s.pretty_print()
    s = tree.search_and_then_also_move(5)
s.pretty_print()
"""

"""
when you arrive at a state that is the end of the game, backprop the value as a hard win or loss value. do not expand. that is all. have a great day :)


"""


