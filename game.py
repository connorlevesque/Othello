import torch
from state import State
from player import Player
from random_player import RandomPlayer
from human_player import HumanPlayer

class Game:

    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.state = State()
        self.last_state = None
        self.consecutive_passes = 0

    def play(self, log=False):
        if log: self.state.pretty_print()
        while self.is_over():
            self.last_state = self.state
            if self.state.to_move == 1:
                self.state = self.player1.play_move(self.state)
            else:
                self.state = self.player2.play_move(self.state)
            if log: self.state.pretty_print()
        if log: self.state.print_score(with_winner=True)

    def is_over(self):
        return self.state.is_full() or self.has_moves_left()

    def has_moves_left(self):
        if self.last_state is None: return True
        if torch.equal(self.state.board, self.last_state.board):
            self.consecutive_passes += 1
        else:
            self.consecutive_passes = 0
        return self.consecutive_passes < 2


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