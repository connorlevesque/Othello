#!/usr/bin/env python3
import datetime
import torch
import torch.nn as nn
from torch.autograd import Variable
import torch.optim as optim
from state import State, move_dict
from player import Player
from monte_carlo_tree import MonteCarloTree, TwoNetEvaluator
from tester import Tester

class DualTrainerBatch:

    def __init__(self):
        self.evaluator = TwoNetEvaluator()
        self.policy_net = self.evaluator.policy_net
        self.eval_net = self.evaluator.eval_net
        self.tree = MonteCarloTree(State(), self.evaluator)
        self.policy_optimizer = optim.SGD(self.policy_net.parameters(), lr=0.01)
        self.eval_optimizer = optim.SGD(self.eval_net.parameters(), lr=0.01)
        self.criterion = nn.MSELoss()
        


    def make_batch_of_n_games_k_iterations(self, n, k, log=False):
        self.reset_tree()
        batch = []
        for i in range(n):
            if log:
                print("Playing game {}".format(i))
            self.tree.reset_root()
            self.tree.play_training_game(k)
            game_path = self.tree.game_path
            winner_int = self.tree.state.score()[0]
            winner_float = [0.5,1.0,0.0][winner_int]
            target_eval = Variable(torch.FloatTensor([winner_float]))
            game = (target_eval, game_path)
            batch.append(game)
        return batch
    
    def train_on_batch(self, batch):
        print("------Begin Training------")
        for i in range(len(batch)):
            print("Training on game {}".format(i))
            game = batch[i]
            path = game[1]
            target_eval = game[0]
            for node in path:

                if node.edges[0].a is None: continue
                input_v = node.state.convert_to_net_input()
                # train policy_net
                target_policy = self.node_to_target(node)
                self.policy_optimizer.zero_grad()
                policy_output = self.policy_net(input_v)
                policy_loss = self.criterion(policy_output, target_policy)
                policy_loss.backward()
                self.policy_optimizer.step()
                # train eval_net
                self.eval_optimizer.zero_grad()
                eval_output = self.eval_net(input_v)
                eval_loss = self.criterion(eval_output, target_eval)
                eval_loss.backward()
                self.eval_optimizer.step()

    def reset_tree(self):
        self.tree = MonteCarloTree(State(), self.evaluator) 

    def node_to_target(self, node):
        target = [0]*64
        for edge in node.edges:
            x,y = edge.a
            target[x + y*8] = edge.Q
        return Variable(torch.FloatTensor(target))


def main():
    version = 1000
    load = False
    trainer = DualTrainerBatch()
    
    ts = datetime.datetime.now().timestamp()
    readable = datetime.datetime.fromtimestamp(ts).isoformat()
    policy_path = "./weights/policy_{}_{}".format(version, readable)
    eval_path = "./weights/eval_{}_{}".format(version, readable)

    
    log_filename = "./logs/{}_{}.log".format(version, readable)
    
    with open(log_filename, 'w+') as f:
        f.write("hello\n")
        f.close()
    
    tester = Tester(log=log_filename)
    if load:
        trainer.policy_net.read_weights_from_file('./weights/policy_10.0_2017-12-06T00:04:33.437222')
        trainer.eval_net.read_weights_from_file('./weights/eval_10.0_2017-12-06T00:04:33.437222')

    for i in range(10):
        log_file=open(log_filename, 'a')
        log_file.write("+++Batch {}+++\n".format(i+1))
        log_file.close()
        print("++++++++running batch {} +++++++++++".format(i))
        batch = trainer.make_batch_of_n_games_k_iterations(100, 50, log=True)
        trainer.train_on_batch(batch)
        print('testing:')
        tester.test_vs_random(trainer.policy_net, 500)

        print(100.0 * move_dict.keys_added / float(move_dict.keys_accessed), '% new keys')
        #move_dict.save()
        log_file=open(log_filename, 'a')
        #log_file.write("{}% new keys\n".format(100.0 * move_dict.keys_added / float(move_dict.keys_accessed)))
        log_file.close()

    trainer.policy_net.write_weights_to_file(policy_path)
    trainer.eval_net.write_weights_to_file(eval_path)
    print('written to', policy_path)
    print('written to', eval_path)
    with open(log_filename, 'a') as f:
        f.write("written to: {}\nwritten to: {}\n".format(policy_path, eval_path))
        f.close()
    #print(100.0 * move_dict.keys_added / float(move_dict.keys_accessed), '% new keys')
    #move_dict.save()

    #log_file.write("{}% new keys".format(100.0 * move_dict.keys_added / float(move_dict.keys_accessed)))
    #move_dict.save()
    log_file.close()

if  __name__ =='__main__':main()
