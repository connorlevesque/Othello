import random
from state import State
from player import Player

class RandomPlayer(Player):

    def play_move(self, state):
        return random.choice(state.legal_moves())


def main():
    r_player = RandomPlayer()
    state = State()
    state.pretty_print()
    for _ in range(8):
        state = r_player.play_move(state)
        state.pretty_print()


if  __name__ =='__main__':main()
