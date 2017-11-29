import sys
from state import State
from player import Player

class HumanPlayer(Player):

    def play_move(self, state):
        while True:
            x,y = self.read_move() 
            try:
                move_state = state.try_move(x,y)
            except ValueError:
                print('Please enter a valid move of the form: x y')
                continue
            return move_state

    def read_move(self):
        line = input('\nEnter move: ');
        return list(map(int, line.split(' ')))


def main():
    h_player = HumanPlayer()
    state = State()
    state.pretty_print()
    for _ in range(8):
        state = h_player.play_move(state)
        state.pretty_print()


if  __name__ =='__main__':main()
