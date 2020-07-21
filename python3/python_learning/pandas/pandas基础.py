import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 从ndarray创建一个系列
# 如果数据是ndarray，则传递的索引必须具有相同的长度。 如果没有传递索引值，那么默认的索引将是范围(n)，其中n是数组长度，即[0,1,2,3…. range(len(array))-1] - 1]。
ndarray = np.array(["a", "b", "c", "d"]);
s1 = pd.Series(ndarray);
print(s1);

# 从字典创建一个序列
# 字典(dict)可以作为输入传递，如果没有指定索引，则按排序顺序取得字典键以构造索引。 如果传递了索引，索引中与标签对应的数据中的值将被拉出。
data = {'name': '张三', 'age': '18', 'habbit': '吃饭'}
s2 = pd.Series(data);
print(s2);

# 使用标量创建一个序列

s3 = pd.Series(5, [0,1,2,3,4,5]);
print(s3);

