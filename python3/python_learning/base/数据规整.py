import pandas as pd
import numpy as np

# 层次化索引
data = pd.Series(np.random.randn(9), index=[['a', 'a', 'a', 'b', 'b', 'c', 'c', 'd', 'd'], [1, 2, 3, 1, 3, 1, 2, 2, 3]])

# 看到的结果是经过美化的带有MultiIndex索引的Series的格式。索引之间的间隔表示直接使用上面的标签
print(data.index);

# 对于一个层次化索引的对象，可以使用所谓的部分索引，使用它选取数据子集
print(data['a'])
print(data['b': 'c'])
print(data.loc[['b', 'c']])


