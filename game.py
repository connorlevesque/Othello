import torch
from state import State
from player import Player
from random_player import RandomPlayer
from human_player import HumanPlayer
from mct_player import MCTPlayer 

class Game:

    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.state = State()
        self.last_state = None
        self.consecutive_passes = 0

    def play(self, log=False):
        if log: self.state.pretty_print()
        while not self.state.is_over():
            self.last_state = self.state
            if self.state.to_move == 1:
                self.state = self.player1.play_move(self.state)
            else:
                self.state = self.player2.play_move(self.state)
            if log: self.state.pretty_print()
        if log: self.state.print_score(with_winner=True)


def main():
    player1 = RandomPlayer()
    player2 = MCTPlayer()
    game = Game(player1, player2)
    print()
    game.play(log=True)


if  __name__ =='__main__':main()
