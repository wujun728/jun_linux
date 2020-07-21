import requests
import pandas as pd

url = 'https://api.github.com/repos/pandas-dev/pandas/issues'

# 我们可以发一个HTTP GET请求，使用requests扩展库：
resp = requests.get(url);

# 响应对象的json方法会返回一个包含被解析过的JSON字典，加载到一个Python对象中：
data = resp.json();

title = data[0]['title']

print(title)

# data中的每个元素都是一个包含所有GitHub主题页数据（不包含评论）的字典。我们可以直接传递数据到DataFrame，并提取感兴趣的字段：

issues = pd.DataFrame(data, columns=['number', 'title', 'labels', 'state'])
print(issues);