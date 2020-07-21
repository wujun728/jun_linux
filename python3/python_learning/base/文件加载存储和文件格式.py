import pandas as pd
import numpy as np

# 读取csv文件，分隔符为 /n ,并且只读取5行
csv = pd.read_csv("../data/visit.csv",sep="\t", header=None, names=['uid','user_id','ip','behavior','module_uid','other_data','status','create_time','update_time']);

# 计数
# print(csv.groupby('ip')['ip'].count())

dateDf = pd.DataFrame();

dateDf['data'] = pd.to_datetime(csv['create_time']).dt.weekday;
print(dateDf);


# print(csv.items);
#for ii in  csv.values:
#    print(ii);

# csv2 = pd.read_csv("../data/blog.csv", sep="/n/t", chunksize=10)
# print(csv.info())

# def add(s):
#     s+"!"
#     return s
#
# fun = lambda xx: xx['uid'];
# print(csv['uid'].apply(fun))

