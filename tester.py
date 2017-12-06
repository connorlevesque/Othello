from game import Game
from net_player import NetPlayer
from random_player import RandomPlayer
from mct_player import MCTPlayer

class Tester:
    def __init__(self, log=None):
        if log:
            self.log_file = log
        else:
            self.log_file = None

    def test_vs_random(self, net, num_games):
        player1 = NetPlayer(net)
        player2 = RandomPlayer()
        draws_wins1_wins2 = [0]*3
        for i in range(num_games):
            #print('test', i)
            game = Game(player1, player2)
            game.play()
            windex = game.state.score()[0]
            #print(i, windex)
            draws_wins1_wins2[windex] += 1
        win_percent = 100 * (draws_wins1_wins2[1] / float(num_games))
        print('draws_wins1_wins2 =', draws_wins1_wins2)
        print('p1 win% = ', win_percent, '%', sep='')
        if self.log_file:
            with f as open(self.log_file, 'w'):
                f.write("draws_wins1_wins2 = {}\np1 win% = {}%".format(draws_wins1_wins2, win_percent))
                f.close()

# t = Tester()
# t.test_vs_random(None, 10)
