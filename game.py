import torch
from state import State
from player import Player
from net import Net
from random_player import RandomPlayer
from human_player import HumanPlayer
from mct_player import MCTPlayer 
from net_player import NetPlayer
from policy_net import PolicyNet

class Game:

    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.state = State()

    def play(self, log=False):
        self.player1.reset()
        if log: self.state.pretty_print()
        while not self.state.is_over():
            self.state.pretty_print()
            if self.state.to_move == 1:
                self.state = self.player1.play_move(self.state)
            else:
                self.state = self.player2.play_move(self.state)
            if log: self.state.pretty_print()
        if log: self.state.print_score(with_winner=True)


def main():
    net = PolicyNet()

    net.read_weights_from_file('./weights/policy_2.0_2017-12-04T21:08:08.381535')
    player2 = RandomPlayer()
    player1 = MCTPlayer()
    game = Game(player1, player2)
    print()
    game.play(log=True)


if  __name__ =='__main__':main()
