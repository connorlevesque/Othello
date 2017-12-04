import torch
from torch.autograd import Variable
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

class Net(nn.Module):

    def __init__(self):
        super(Net, self).__init__()
        self.layer_1 = nn.Linear(128, 84, True)
        self.layer_2 = nn.Linear(84, 84, True)
        self.layer_3 = nn.Linear(84, 65, True)

    def forward(self, x):
        x = F.relu(self.layer_1(x))
        x = F.relu(self.layer_2(x))
        x = F.relu(self.layer_3(x))
        return x


net = Net()
input_v = Variable(torch.randn(128))
target = Variable(torch.arange(0.0, 65.0))  # a dummy target, for example
criterion = nn.MSELoss()
optimizer = optim.SGD(net.parameters(), lr=0.01)

for _ in range(1000):
    optimizer.zero_grad()
    output = net(input_v)
    loss = criterion(output, target)
    loss.backward()
    optimizer.step()

print(output)