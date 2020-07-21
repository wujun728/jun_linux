例子如下：

```
import json
import numpy as np


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, bytes):
            return str(obj, encoding='utf-8');
        return json.JSONEncoder.default(self, obj)


dict = {'id': 1, 'title': b'\xe7\xac\xac\xe4\xb8\x80\xe7\xab\xa0 \xe7\xa7\xa6\xe7\xbe\xbd'}
dup = json.dumps(dict, cls=MyEncoder, ensure_ascii=False, indent=4)
print(dup)
```

###  indent

根据数据格式缩进显示，读起来更加清晰，indent的数值，代表缩进的位数。

### ensure_ascii

如果无任何配置，或者说使用默认配置， 输出的会是中文的ASCII字符吗，而不是真正的中文。 这是因为json.dumps 序列化时对中文默认使用的ascii编码。

```
{
    "id": 1,
    "title": "\u7b2c\u4e00\u7ae0 \u79e6\u7fbd"
}
```

### cls

dict类型的数据(存在中文)，在python2中是可以转化的，但是在python3中存在序列化问题：


```
TypeError: Object of type bytes is not JSON serializable

```


