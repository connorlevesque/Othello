import random
from state import State
from player import Player
from monte_carlo_tree import MonteCarloTree, FakeRandomNet

class MCTPlayer(Player):

    def __init__(self):
        self.tree = MonteCarloTree(Rollouter())
        iterations = 50

    def play_move(self, state):
        return self.tree.search_and_then_also_move(iterations)


def main():
    m_player = MCTPlayer()
    state = State()
    state.pretty_print()
    for _ in range(8):
        state = m_player.play_move(state)
        state.pretty_print()


if  __name__ =='__main__':main()