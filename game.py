from state import State
from player import Player
from random_player import RandomPlayer
from human_player import HumanPlayer

class Game:

    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.state = State()

    def play(self, log=False):
        if log: self.state.pretty_print()
        while self.state.has_moves_left():
            if self.state.to_move == 1:
                self.state = self.player1.play_move(self.state)
            else:
                self.state = self.player2.play_move(self.state)
            if log: self.state.pretty_print()
        if log: self.state.print_score(with_winner=True)


def main():
    h_player = HumanPlayer()
    r_player = RandomPlayer()
    game = Game(r_player, h_player)
    game.state.set(3,3,1)
    game.state.set(4,5,1)
    game.state.set(5,4,1)
    game.state.set(5,5,1)
    print()
    game.play(log=True)


if  __name__ =='__main__':main()