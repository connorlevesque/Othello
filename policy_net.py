import torch
from torch.autograd import Variable
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

class PolicyNet(nn.Module):

    def __init__(self):
        super(PolicyNet, self).__init__()
        self.layer_1 = nn.Linear(128, 84, True)
        self.layer_2 = nn.Linear(84, 84, True)
        self.layer_3 = nn.Linear(84, 84, True)
        # self.layer_4 = nn.Linear(84, 84, True)
        self.layer_5 = nn.Linear(84, 64, True)

    def write_weights_to_file(self, file):
        torch.save(self.state_dict(), file)

    def read_weights_from_file(self, file):
        self.load_state_dict(torch.load(file))

    def forward(self, x):
        x = F.relu(self.layer_1(x))
        x = F.relu(self.layer_2(x))
        x = F.relu(self.layer_3(x))
        # x = F.relu(self.layer_4(x))
        x = F.relu(self.layer_5(x))
        return x
