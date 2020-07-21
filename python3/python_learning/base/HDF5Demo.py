import pandas as pd
import numpy as np

frame = pd.DataFrame({'a': np.random.randn(100)});

store = pd.HDFStore('mydata.h5');

store['obj1'] = frame;

store['obj1_col'] = frame['a']

# HDF5文件中的对象可以通过与字典一样的API进行获取：
print(store['obj1']);

# HDFStore支持两种存储模式，'fixed'和'table'。后者通常会更慢，但是支持使用特殊语法进行查询操作：

store.put('obj2', frame, format='table')

storeList = store.select('obj2', where=['index >=10 and index <=15 '])

print(storeList);

# pandas.read_hdf函数可以快捷使用这些工具：
frame.to_hdf('mydata.h5', 'obj3', format ='table')

h5List = pd.read_hdf('mydata.h5', 'obj3', where=['index < 5'])
