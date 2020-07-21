import torch
import torch.nn as nn
import numpy as np
import matplotlib.pyplot as plt

# torch.manual_seed(1)    # reproducible
# np.random.seed(1)

# Hyper Parameters
BATCH_SIZE = 64
LR_G = 0.0001           # learning rate for generator
LR_D = 0.0001           # learning rate for discriminator
N_IDEAS = 5             # think of this as number of ideas for generating an art work (Generator)
ART_COMPONENTS = 15     # it could be total point G can draw in the canvas   有十五个点
PAINT_POINTS = np.vstack([np.linspace(-1, 1, ART_COMPONENTS) for _ in range(BATCH_SIZE)])

# show our beautiful painting range
# plt.plot(PAINT_POINTS[0], 2 * np.power(PAINT_POINTS[0], 2) + 1, c='#74BCFF', lw=3, label='upper bound')
# plt.plot(PAINT_POINTS[0], 1 * np.power(PAINT_POINTS[0], 2) + 0, c='#FF9359', lw=3, label='lower bound')
# plt.legend(loc='upper right')
# plt.show()

# 生成一批著名画家的数据
def artist_works():     # painting from the famous artist (real target)
    a = np.random.uniform(1, 2, size=BATCH_SIZE)[:, np.newaxis]
    # 通过15个点，产生一个一元二次函数
    paintings = a * np.power(PAINT_POINTS, 2) + (a-1)
    # 转换成torch形式
    paintings = torch.from_numpy(paintings).float()
    return paintings

# 新手画家
G = nn.Sequential(                      # Generator
    nn.Linear(N_IDEAS, 128),            # 新手画家，随机传入N_IDEAS 个想法
    nn.ReLU(),
    nn.Linear(128, ART_COMPONENTS),     # making a painting from these random ideas
)

# 新手鉴赏家
D = nn.Sequential(                      # Discriminator
    nn.Linear(ART_COMPONENTS, 128),     # 接收这幅画中的15个点， ART_COMPONENTS
    nn.ReLU(),
    nn.Linear(128, 1),                  # 判别，最后得出好画还是不好的画
    nn.Sigmoid(),                       # sigmoid函数也叫 Logistic 函数，用于隐层神经元输出，取值范围为(0,1)，它可以将一个实数映射到(0,1)的区间，可以用来做二分类。
)

# 使用Adam优化器，来进行优化学习
opt_D = torch.optim.Adam(D.parameters(), lr=LR_D)
opt_G = torch.optim.Adam(G.parameters(), lr=LR_G)

plt.ion()   # something about continuous plotting

# 学习10000步
for step in range(10000):
    # 著名画家绘制的画
    artist_paintings = artist_works()           # real painting from artist
    # 新手画家的想法产生
    G_ideas = torch.randn(BATCH_SIZE, N_IDEAS)  # random ideas
    # 新手画家开始生成画
    G_paintings = G(G_ideas)                    # fake painting from G (random ideas)

    # 这匹画中有多少是著名画家画的
    prob_artist0 = D(artist_paintings)          # D try to increase this prob
    # 这匹画里面，有多少是新手画家画的
    prob_artist1 = D(G_paintings)               # D try to reduce this prob

    D_loss = - torch.mean(torch.log(prob_artist0) + torch.log(1. - prob_artist1))
    # 增加著名画家的概率
    G_loss = torch.mean(torch.log(1. - prob_artist1))

    opt_D.zero_grad()
    D_loss.backward(retain_graph=True)      # reusing computational graph
    opt_D.step()

    opt_G.zero_grad()
    G_loss.backward()
    opt_G.step()

    if step % 50 == 0:  # plotting
        plt.cla()
        plt.plot(PAINT_POINTS[0], G_paintings.data.numpy()[0], c='#4AD631', lw=3, label='Generated painting',)
        plt.plot(PAINT_POINTS[0], 2 * np.power(PAINT_POINTS[0], 2) + 1, c='#74BCFF', lw=3, label='upper bound')
        plt.plot(PAINT_POINTS[0], 1 * np.power(PAINT_POINTS[0], 2) + 0, c='#FF9359', lw=3, label='lower bound')
        plt.text(-.5, 2.3, 'D accuracy=%.2f (0.5 for D to converge)' % prob_artist0.data.numpy().mean(), fontdict={'size': 13})
        plt.text(-.5, 2, 'D score= %.2f (-1.38 for G to converge)' % -D_loss.data.numpy(), fontdict={'size': 13})
        plt.ylim((0, 3));plt.legend(loc='upper right', fontsize=10);plt.draw();plt.pause(0.01)

plt.ioff()
plt.show()