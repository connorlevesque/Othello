import random
import dhconnelly_othello as dhc
from state import State
from player import Player


class MiniMaxPlayer(Player):

    # def __init__(self, depth, evaluate):
    #     self.strategy = dhc.minimax_searcher(depth, evaluate)

    # def play_move(self, state):
    #     player = 
    #     board = our_state_to_dhc_board(state)
    #     depth = 
    #     evaluate = 
    #     dhc.minimax(player, board, depth)
    #     return random.choice(state.legal_moves())


    # def our_state_to_dhc_board(state):


    # def dhc_move_to_our_state(dhc_move):



def main():
    mm_player = RandomPlayer()
    state = State()
    state.pretty_print()
    for _ in range(8):
        state = mm_player.play_move(state)
        state.pretty_print()


if  __name__ =='__main__':main()