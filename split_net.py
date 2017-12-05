import torch
from torch.autograd import Variable
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

class SplitNet(nn.Module):

    def __init__(self):
        super(SplitNet, self).__init__()
        self.tail = Tail()
        self.policy_head = PolicyHead()
        self.eval_head = EvalHead()

    def write_weights_to_file(self, file):
        self.tail.write_weights_to_file(file + '_tail')
        self.policy_head.write_weights_to_file(file + '_phead')
        self.eval_head.write_weights_to_file(file + '_ehead')

    def read_weights_from_file(self, t_file, ph_file, eh_file):
        self.tail.read_weights_from_file(t_file)
        self.policy_head.read_weights_from_file(ph_file)
        self.eval_head.read_weights_from_file(eh_file)

    def forward(self, x):
        x = self.tail(x)
        policy = self.policy_head(x)
        evaluation = self.eval_head(x)
        # return torch.add_(policy, evaluation.data[0])
        return policy, evaluation


class Tail(nn.Module):

    def __init__(self):
        super(Tail, self).__init__()
        self.layer_1 = nn.Linear(128, 128, True)
        self.layer_2 = nn.Linear(128, 128, True)
        self.layer_3 = nn.Linear(128, 128, True)

    def write_weights_to_file(self, file):
        torch.save(self.state_dict(), file)

    def read_weights_from_file(self, file):
        self.load_state_dict(torch.load(file))

    def forward(self, x):
        x = F.relu(self.layer_1(x))
        x = F.relu(self.layer_2(x))
        x = F.relu(self.layer_3(x))
        return x

class PolicyHead(nn.Module):

    def __init__(self):
        super(PolicyHead, self).__init__()
        self.layer_1 = nn.Linear(128, 84, True)
        self.layer_2 = nn.Linear(84, 84, True)
        self.layer_3 = nn.Linear(84, 84, True)
        self.layer_4 = nn.Linear(84, 64, True)

    def write_weights_to_file(self, file):
        torch.save(self.state_dict(), file)

    def read_weights_from_file(self, file):
        self.load_state_dict(torch.load(file))

    def forward(self, x):
        x = F.relu(self.layer_1(x))
        x = F.relu(self.layer_2(x))
        x = F.relu(self.layer_3(x))
        x = F.relu(self.layer_4(x))
        return x

class EvalHead(nn.Module):

    def __init__(self):
        super(EvalHead, self).__init__()
        self.layer_1 = nn.Linear(128, 84, True)
        self.layer_2 = nn.Linear(84, 64, True)
        self.layer_3 = nn.Linear(64, 42, True)
        self.layer_4 = nn.Linear(42, 28, True)
        self.layer_5 = nn.Linear(28, 1, True)

    def write_weights_to_file(self, file):
        torch.save(self.state_dict(), file)

    def read_weights_from_file(self, file):
        self.load_state_dict(torch.load(file))

    def forward(self, x):
        x = F.relu(self.layer_1(x))
        x = F.relu(self.layer_2(x))
        x = F.relu(self.layer_3(x))
        x = F.relu(self.layer_4(x))
        x = F.relu(self.layer_5(x))
        return x

# net = SplitNet()
# # print(list(net.parameters()))
# input_v = Variable(torch.randn(128))
# target_pol = Variable(torch.arange(0.0, 64.0))  # a dummy target, for example
# target_eval = Variable(torch.FloatTensor([64.0]))
# criterion = nn.MSELoss()
# optimizer = optim.SGD(net.parameters(), lr=0.01)

# for _ in range(10000):
#     optimizer.zero_grad()
#     out_pol, out_eval = net(input_v)
#     loss_pol = criterion(out_pol, target_pol)
#     loss_eval = criterion(out_eval, target_eval)
#     # torch.autograd.backward([loss_pol, loss_eval])
#     loss_pol.backward(retain_graph=True)
#     optimizer.step()
#     loss_eval.backward()
#     optimizer.step()

# print(out_pol)
# print(out_eval)
