import random
from state import State
from player import Player

class NetPlayer(Player):

    def play_move(self, state):
        return random.choice(state.legal_moves())


def main():
    n_player = NetPlayer()
    state = State()
    state.pretty_print()
    for _ in range(8):
        state = n_player.play_move(state)
        state.pretty_print()


if  __name__ =='__main__':main()