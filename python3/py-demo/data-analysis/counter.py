# -*- coding: utf-8 -*-

import json
from pandas import DataFrame, Series
import numpy as np
import matplotlib.pyplot as plt

path = r'C:\usr\work\pydata\pydata-book\ch02\usagov_bitly_data2012-03-16-1331923249.txt'
records = [json.loads(line) for line in open(path)]

frame = DataFrame(records)

# tz_counts = frame['tz'].value_counts()
# print tz_counts[:10]

clean_tz = frame['tz'].fillna('Missing')
clean_tz[clean_tz == ''] = 'Unknown'
tz_counts = clean_tz.value_counts()

# 绘制时区统计直方图
# tz_counts[:10].plot(kind='barh', rot=0)

results = Series([x.split()[0] for x in frame.a.dropna()])

print results.value_counts()[:8]


plt.show()

