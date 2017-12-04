import random
from state import State
from player import Player
from monte_carlo_tree import MonteCarloTree, NetEvaluator

class NetPlayer(Player):

    def __init__(self, net):
        self.net = net

    def play_move(self, state):
        output = self.net(state.convert_to_net_input())
        max_prob = -1
        best_state = None
        for next_state in state.legal_moves():
            #next_state.pretty_print()
            if next_state.last_move == None:
                return next_state
            x,y = next_state.last_move
            prob = output.data[x+y*8]
            if prob > max_prob:
                max_prob = prob
                best_state = next_state
        return best_state


def main():
    m_player = MCTPlayer()
    state = State()
    state.pretty_print()
    for _ in range(8):
        state = m_player.play_move(state)
        state.pretty_print()


if  __name__ =='__main__':main()
