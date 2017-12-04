import datetime
import torch
import torch.nn as nn
from torch.autograd import Variable
import torch.optim as optim
from state import State
from player import Player
from net_player import NetPlayer
from monte_carlo_tree import MonteCarloTree, NetEvaluator
from tester import Tester

class Trainer:

    def __init__(self):

        self.evaluator = NetEvaluator()
        self.net = self.evaluator.net
        self.tree = MonteCarloTree(State(), NetEvaluator())
        self.alpha = 0.01
        self.optimizer = optim.SGD(self.net.parameters(), lr=self.alpha)
        self.criterion = nn.MSELoss()

    def train(self, k, n):
        for i in range(k):
            print(i)
            self.train_on_game(n)
    def reset_tree(self):
        self.tree = MonteCarloTree(State(), self.evaluator) 
                
    def train_on_game(self, n):
        print('playin game')
        self.reset_tree()
        self.tree.play_training_game(n)
        print('training on game')
        game_path = self.tree.game_path
        winner = self.tree.state.score()[0]
        for node in game_path:
            if node.edges[0].a is None: continue
            input_v = node.state.convert_to_net_input()
            target = self.node_to_target(node, winner)
            self.optimizer.zero_grad()
            output = self.net(input_v)
            loss = self.criterion(output, target)
            loss.backward()
            self.optimizer.step()

    def node_to_target(self, node, winner):
        target = [0]*65
        for edge in node.edges:
            x,y = edge.a
            target[x + y*8] = edge.Q
        target[64] = winner
        return Variable(torch.FloatTensor(target))


version = 2.0
tester = Tester()
trainer = Trainer()
#trainer.net.read_weights_from_file('./weights/weight_1.2_2017-12-04T13:00:44.134928')
trainer.train(100, 10)
print(trainer.net.layer_1.weight.data)
print(trainer.net.layer_2.weight.data)
print(trainer.net.layer_3.weight.data)

tester.test_vs_random(trainer.net, 500)

ts = datetime.datetime.now().timestamp()
readable = datetime.datetime.fromtimestamp(ts).isoformat()
path = "./weights/weight_{}_{}".format(version, readable)
trainer.net.write_weights_to_file(path)

