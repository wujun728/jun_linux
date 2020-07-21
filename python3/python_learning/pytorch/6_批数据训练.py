import torch

# 这个data是用于小批量数据训练的模块
import torch.utils.data as Data

torch.manual_seed(1)    # reproducible

# 定义5个大小的批处理模块
BATCH_SIZE = 5

# 定义1 - 10的10个数据点
x = torch.linspace(1, 10, 10)
y = torch.linspace(10, 1, 10)

# 用torch定义一个数据集  第一个参数表示训练集， 第二个表示 目标集（用于进行均方差）
# 下面步骤是转换成 torch 能识别的 Dataset
torch_dataset = Data.TensorDataset(x, y)

# DataLoader是使得我们的数据变成小批的
loader = Data.DataLoader(
    # 定义数据集
    dataset=torch_dataset,
    # 定义批处理模块大小
    batch_size=BATCH_SIZE,
    # shuffle表示，在下面进行数据训练的时候，是否需要打乱数据
    shuffle=True,
    # 表示使用两个线程进行提取
    num_workers=2,
);

def show_step():
    # 定义循环，让数据整训练三次
    for epoch in range(3):
        # 每一步 loader 释放一小批数据用来学习
        # enumerate:表示对loader增加索引
        for step, (batch_x, batch_y) in enumerate(loader):
            # 下面是开始训练的过程
            # 打出来一些数据
            print('批数: ', epoch, '| 步数: ', step, '| batch x: ',
                  batch_x.numpy(), '| batch y: ', batch_y.numpy())

if __name__ == '__main__':
    show_step()
