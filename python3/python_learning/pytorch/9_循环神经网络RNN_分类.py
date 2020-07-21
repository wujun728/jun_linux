import torch
from torch import nn
import torchvision.datasets as dsets
import torchvision.transforms as transforms
import matplotlib.pyplot as plt


# torch.manual_seed(1)    # reproducible

# 超参数
EPOCH = 1               # 训练数据n次，为了节省时间，我们只训练1个epoch
BATCH_SIZE = 64         # 批训练的数量

# RNN 有 TIME_STEP  和  INPUT_SIZE
TIME_STEP = 28          # rnn time step / image height (多少个时间点的数据，一行数据包含28个像素点)
INPUT_SIZE = 28         # rnn input size / image width
LR = 0.01               # 学习率

DOWNLOAD_MNIST = False   # 如果下载好了数据就改成False


# Mnist digital dataset
train_data = dsets.MNIST(
    root='./mnist/',
    train=True,                         # this is training data
    transform=transforms.ToTensor(),    # Converts a PIL.Image or numpy.ndarray to
                                        # torch.FloatTensor of shape (C x H x W) and normalize in the range [0.0, 1.0]
    download=DOWNLOAD_MNIST,            # download it if you don't have it
)

# plot one example
print(train_data.train_data.size())     # (60000, 28, 28)
print(train_data.train_labels.size())   # (60000)
plt.imshow(train_data.train_data[0].numpy(), cmap='gray')
plt.title('%i' % train_data.train_labels[0])
plt.show()

# Data Loader for easy mini-batch return in training
train_loader = torch.utils.data.DataLoader(dataset=train_data, batch_size=BATCH_SIZE, shuffle=True)

# convert test data into Variable, pick 2000 samples to speed up testing
test_data = dsets.MNIST(root='./mnist/', train=False, transform=transforms.ToTensor())
test_x = test_data.test_data.type(torch.FloatTensor)[:2000]/255.   # shape (2000, 28, 28) value in range(0,1)
print(test_x)
test_y = test_data.test_labels.numpy()[:2000]    # covert to numpy array


class RNN(nn.Module):
    def __init__(self):
        super(RNN, self).__init__()

        # 使用LSTM的RNN形式，使用更高级LSTM，能加速收敛
        self.rnn = nn.LSTM(         # if use nn.RNN(), it hardly learns
            input_size=INPUT_SIZE,
            hidden_size=64,         # 隐藏层大小
            num_layers=1,           # 类似于细胞层数，值越大，效果越好，处理越慢

            # 输入数据的维度 (batch, time_step, input_size) ， 一般是 batch放在第一个，就需要设置True
            batch_first=True,       # input & output will has batch size as 1s dimension. e.g. (batch, time_step, input_size)
        )

        # 对数据进行处理
        self.out = nn.Linear(64, 10)

    # 定义前置传播
    def forward(self, x):
        # x shape (batch, time_step, input_size)
        # r_out shape (batch, time_step, output_size)
        # h_n shape (n_layers, batch, hidden_size)
        # h_c shape (n_layers, batch, hidden_size)

        # 定义RNN output    在这一步，每次都会加上上一步的理解    (h_n, h_c)：一个是支线，一个是主线  None：表示第一个hidden_state有没有值
        #  x (batch, time_step, input_size):    有28个time_step 和 28个input_size，根据time_step和input_size计算得出每一步的理解
        # r_out 有28个输出，所有有28个
        r_out, (h_n, h_c) = self.rnn(x, None)

        # r_out[]中有全部的每一层的理解，这里是选取最后的一个output
        out = self.out(r_out[:, -1, :])  # (batch, time_step, input)
        return out


rnn = RNN()
print(rnn)

optimizer = torch.optim.Adam(rnn.parameters(), lr=LR)   # 使用Adam优化器，加载全部参数
loss_func = nn.CrossEntropyLoss()                       # 使用CrossEntropyLoss()来计算误差

# training and testing
for epoch in range(EPOCH):
    for step, (b_x, b_y) in enumerate(train_loader):        # gives batch data

        # 取出最后一个 output，因为要读完了，在取最后一个做决定
        b_x = b_x.view(-1, 28, 28)              # reshape x to (batch, time_step, input_size)

        output = rnn(b_x)                               # rnn output
        loss = loss_func(output, b_y)                   # cross entropy loss
        optimizer.zero_grad()                           # clear gradients for this training step
        loss.backward()                                 # backpropagation, compute gradients
        optimizer.step()                                # apply gradients

        # 每50步查看一下误差
        if step % 50 == 0:
            test_output = rnn(test_x)                   # (samples, time_step, input_size)
            pred_y = torch.max(test_output, 1)[1].data.numpy()
            accuracy = float((pred_y == test_y).astype(int).sum()) / float(test_y.size)
            print('Epoch: ', epoch, '| train loss: %.4f' % loss.data.numpy(), '| test accuracy: %.2f' % accuracy)

# print 10 predictions from test data
test_output = rnn(test_x[:10].view(-1, 28, 28))
pred_y = torch.max(test_output, 1)[1].data.numpy()
print(pred_y, 'prediction number')
print(test_y[:10], 'real number')