import torch
from torch.autograd import Variable
import torch.utils.data as Data
import torch.nn.functional as F
import matplotlib.pyplot as plt

# torch.manual_seed(1)    # reproducible

# 定义超参数
# 在机器学习的上下文中，超参数是在开始学习过程之前设置值的参数，而不是通过训练得到的参数数据。
# 通常情况下，需要对超参数进行优化，给学习机选择一组最优超参数，以提高学习的性能和效果。
LR = 0.01
BATCH_SIZE = 32
EPOCH = 12

# 制作测试数据
x = torch.unsqueeze(torch.linspace(-1, 1, 1000), dim=1)
y = x.pow(2) + 0.1*torch.normal(torch.zeros(*x.size()))

# 显示
# plt.scatter(x.numpy(), y.numpy())
# plt.show()

# 把numpy创建的数据集放到tensor里面
torch_dataset = Data.TensorDataset(x, y)

# 使用DataLoader进行数据加载，批训练大小为32
loader = Data.DataLoader(dataset=torch_dataset, batch_size=BATCH_SIZE, shuffle=True, num_workers=2,)


# default network
class Net(torch.nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.hidden = torch.nn.Linear(1, 20)   # 定义20个隐藏层的神经元
        self.re = torch.nn.Linear(20, 40)
        self.predict = torch.nn.Linear(40, 1)   # 定义输出层

    def forward(self, x):
        x = F.relu(self.hidden(x))# 激励函数(隐藏层的线性值)
        x = self.re(x)
        x = F.relu(x)
        x = self.predict(x)             # 输出值, 但是这个不是预测值, 预测值还需要再另外计算
        return x

if __name__ == '__main__':
    # 建立四个不同的神经网络，用于优化
    net_SGD         = Net()
    net_Momentum    = Net()
    net_RMSprop     = Net()
    net_Adam        = Net()
    # 把创建的神经网络放到List中
    nets = [net_SGD, net_Momentum, net_RMSprop, net_Adam]

    # 不同的优化器
    opt_SGD         = torch.optim.SGD(net_SGD.parameters(), lr=LR)
    opt_Momentum    = torch.optim.SGD(net_Momentum.parameters(), lr=LR, momentum=0.8)
    opt_RMSprop     = torch.optim.RMSprop(net_RMSprop.parameters(), lr=LR, alpha=0.9)
    opt_Adam        = torch.optim.Adam(net_Adam.parameters(), lr=LR, betas=(0.9, 0.99))

    # 把创建的优化器放到list中
    optimizers = [opt_SGD, opt_Momentum, opt_RMSprop, opt_Adam]

    # 定义回归的误差计算公式  损失函数
    loss_func = torch.nn.MSELoss()

    # 这个用于记录误差变化曲线
    losses_his = [[], [], [], []]

    # 开始训练 训练12个EPOCH
    for epoch in range(EPOCH):

        print('Epoch: ', epoch)

        for step, (b_x, b_y) in enumerate(loader):          # for each training step

            # 将数据使用Variable进行包装
            b_x = Variable(b_x)
            b_y = Variable(b_y)

            # nets, optimizers, losses_his 是list的形式，我们需要一个一个的提取出来
            for net, opt, l_his in zip(nets, optimizers, losses_his):
                output = net(b_x)              # get output for every net
                loss = loss_func(output, b_y)  # compute loss for every net
                opt.zero_grad()                # clear gradients for next train
                loss.backward()                # backpropagation, compute gradients
                opt.step()                     # apply gradients
                l_his.append(loss.data.numpy())     # loss recoder

    labels = ['SGD', 'Momentum', 'RMSprop', 'Adam']
    for i, l_his in enumerate(losses_his):
        plt.plot(l_his, label=labels[i])
    plt.legend(loc='best')
    plt.xlabel('Steps')
    plt.ylabel('Loss')
    plt.ylim((0, 0.2))
    plt.show()