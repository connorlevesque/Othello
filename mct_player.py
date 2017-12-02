import random
from state import State
from player import Player
from monte_carlo_tree import MonteCarloTree, Rollouter

class MCTPlayer(Player):

    def __init__(self):
        self.tree = MonteCarloTree(State(), Rollouter())
        self.iterations = 3

    def play_move(self, state):
        self.tree.update_working_root_to(state)
        return self.tree.search_and_then_also_move(self.iterations)

    

def main():
    m_player = MCTPlayer()
    state = State()
    state.pretty_print()
    for _ in range(8):
        state = m_player.play_move(state)
        state.pretty_print()


if  __name__ =='__main__':main()
