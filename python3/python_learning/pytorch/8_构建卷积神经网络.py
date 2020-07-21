import os
# third-party library
import torch
import torch.nn as nn
import torch.utils.data as Data
# torchvision包含一些数据库
import torchvision
import matplotlib.pyplot as plt

# torch.manual_seed(1)    # reproducible

# 定义超参数
EPOCH = 1               # train the training data n times, to save time, we just train 1 epoch
BATCH_SIZE = 50
LR = 0.001              # learning rate
DOWNLOAD_MNIST = False # 是否下载好


# Mnist digits dataset
if not(os.path.exists('./mnist/')) or not os.listdir('./mnist/'):
    # not mnist dir or mnist is empyt dir
    DOWNLOAD_MNIST = True

# 下载数据
train_data = torchvision.datasets.MNIST(
    root='./mnist/',
    train=True,                                     # 这是训练数据
    transform=torchvision.transforms.ToTensor(),    # 把原始的数据（numpy array），改变成tensor的格式。把0-255的值，压缩到0-1，因为这个是只有一层，不是GRB的格式
    download=DOWNLOAD_MNIST,                        # 是否下载好了 minist数据
)

# 把示例图进行显示
print(train_data.train_data.size())                 # (60000, 28, 28)
print(train_data.train_labels.size())               # (60000)
plt.imshow(train_data.train_data[0].numpy(), cmap='gray') # 展示第一张图片
plt.title('%i' % train_data.train_labels[0]) # 展示结果标签
plt.show()

# 使用DataLoader进行小批量数据训练，图像批处理形状是 (50, 1, 28, 28)
train_loader = Data.DataLoader(dataset=train_data, batch_size=BATCH_SIZE, shuffle=True)

# pick 2000 samples to speed up testing
test_data = torchvision.datasets.MNIST(root='./mnist/', train=False)

# 将test_data 压缩到 0-1之间
test_x = torch.unsqueeze(test_data.test_data, dim=1).type(torch.FloatTensor)[:2000]/255.   # shape from (2000, 28, 28) to (2000, 1, 28, 28), value in range(0,1)
# 取2000个数据
test_y = test_data.test_labels[:2000]

# 开始建立神经网络
class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()

        # 快速创建一个卷积神经网络
        self.conv1 = nn.Sequential(         # input shape (1, 28, 28)
            # 一个卷积神经网络通常包含三个部分： Conv2d：卷积层   ReLU：神经网络   MaxPool2d：池化层

            # 卷积层，相当于信息过滤器，是一个三维的过滤器（有长宽高三个属性）
            nn.Conv2d(
                in_channels=1,              # 输入层的高度（因为是灰度图片，只有一层，如果是RGB图片，有三层）
                out_channels=16,            # 输出层的高度，相当于有16个特征，用于下一层处理（16个滤波器同时扫描，会得出16个特征，高度为16）
                kernel_size=5,              # filter的大小是 5*5的像素点
                stride=1,                   # filter movement/step，跳跃的filter,每隔多少步跳一步
                padding=2,                  # 在周围围上一圈为0的数据。为了让过滤器能够完全扫描，需要在外面包裹一圈

            ),                              # output shape (16, 28, 28)

            nn.ReLU(),                      # activation   （16，28,28）

            # output (16,14,14)
            nn.MaxPool2d(kernel_size=2),    # 选取这个区域中，最大的值（从两个中选取1个，所以减少了一半） choose max value in 2x2 area, output shape (16, 14, 14)
        )

        # 第二层卷积
        self.conv2 = nn.Sequential(         # input shape (16, 14, 14)
            nn.Conv2d(16, 32, 5, 1, 2),     # output shape (32, 14, 14) 输入16层 然后输出 32层
            nn.ReLU(),                      # activation (32,14,14)
            nn.MaxPool2d(2),                # output shape (32, 7, 7)
        )
        # 输出层   10个分类的东西, 展平数据
        self.out = nn.Linear(32 * 7 * 7, 10)   # fully connected layer, output 10 classes

    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)   # （batch_size, 32, 7, 7）

        # 进行扩展，展平的操作  -1:表示维度变成一起
        x = x.view(x.size(0), -1)           # flatten the output of conv2 to (batch_size, 32 * 7 * 7)

        output = self.out(x)

        return output, x    # return x for visualization


cnn = CNN()
print(cnn)  # net architecture

# 使用 Adam优化器
optimizer = torch.optim.Adam(cnn.parameters(), lr=LR)   # optimize all cnn parameters
loss_func = nn.CrossEntropyLoss()                       # the target label is not one-hotted

# following function (plot_with_labels) is for visualization, can be ignored if not interested
from matplotlib import cm
try: from sklearn.manifold import TSNE; HAS_SK = True
except: HAS_SK = False; print('Please install sklearn for layer visualization')
def plot_with_labels(lowDWeights, labels):
    plt.cla()
    X, Y = lowDWeights[:, 0], lowDWeights[:, 1]
    for x, y, s in zip(X, Y, labels):
        c = cm.rainbow(int(255 * s / 9)); plt.text(x, y, s, backgroundcolor=c, fontsize=9)
    plt.xlim(X.min(), X.max()); plt.ylim(Y.min(), Y.max()); plt.title('Visualize last layer'); plt.show(); plt.pause(0.01)

plt.ion()
# training and testing
for epoch in range(EPOCH):
    for step, (b_x, b_y) in enumerate(train_loader):   # gives batch data, normalize x when iterate train_loader

        output = cnn(b_x)[0]               # cnn output
        loss = loss_func(output, b_y)   # cross entropy loss
        optimizer.zero_grad()           # clear gradients for this training step
        loss.backward()                 # backpropagation, compute gradients
        optimizer.step()                # apply gradients

        if step % 50 == 0:
            test_output, last_layer = cnn(test_x)
            pred_y = torch.max(test_output, 1)[1].data.numpy()
            accuracy = float((pred_y == test_y.data.numpy()).astype(int).sum()) / float(test_y.size(0))
            print('Epoch: ', epoch, '| train loss: %.4f' % loss.data.numpy(), '| test accuracy: %.2f' % accuracy)
            if HAS_SK:
                # Visualization of trained flatten layer (T-SNE)
                tsne = TSNE(perplexity=30, n_components=2, init='pca', n_iter=5000)
                plot_only = 500
                low_dim_embs = tsne.fit_transform(last_layer.data.numpy()[:plot_only, :])
                labels = test_y.numpy()[:plot_only]
                plot_with_labels(low_dim_embs, labels)
plt.ioff()

# print 10 predictions from test data
test_output, _ = cnn(test_x[:10])
pred_y = torch.max(test_output, 1)[1].data.numpy()
print(pred_y, 'prediction number')
print(test_y[:10].numpy(), 'real number')
