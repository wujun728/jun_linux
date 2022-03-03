## 准备工作


```
# 安装 Web 框架 
pip install Django
# 创建一个项目
python  django-admin.py startproject itstyle
# 切换目录
cd itstyle
 # 创建  App
python manage.py startapp novel
```

一般一个项目有多个app, 当然通用的app也可以在多个项目中使用，然后启动服务：

```
# 默认端口是8000
python manage.py runserver
```

如果提示端口被占用，可以用其它端口：

```
python manage.py runserver 8001
python manage.py runserver 8002
```

## 项目结构

win下使用命令 tree /F > 项目结构图.txt ，如下：


```
│  manage.py
│  
├─novel
│  │  settings.py # 基础配置
│  │  urls.py     # URL映射
│  │  wsgi.py
│  │  __init__.py
│  │  
│          
├─templates # 相关页面
│      novel.html # 章节
│      novel_list.html # 小说首页
│      
├─utils
│  │  dbMysqlConfig.cnf # 数据库配置参数
│  │  encoder.py # 编码类
│  │  mysql_DBUtils.py # 数据库连接池
│          
└─view
    │  index.py   # 后台业务        

```

## 要点备注


### RESTful 风格

控制器

```
from django.conf.urls import url
from django.urls import path
from view import index

urlpatterns = [
    # 首页
    path('', index.main),  # new
    # 章节页面 正则匹配 
    path('chapter/<int:novel_id>/', index.chapter),    # new
]
```
代码实现

```
# 此处 novel_id 对应 urls.py 中的 <int:novel_id>
# 你可以访问：http://localhost:8000/chapter/1/
def chapter(request, novel_id):
    sql = "SELECT title,content FROM novel where id = %(id)s;"
    param = {"id": novel_id}
    result = mysql.getOne(sql, param)
    # 中文编码问题，由于查询出来的额中文是字节码，这里需要转换一下
    result['title'] = result['title'].decode('utf-8')
    result['content'] = result['content'].decode('utf-8')
    context = {'novel': result}
    return render(request, 'novel.html', context)
```

### 列表展示


基于后端返回的数据，在前台进行展示，这里你可以把它想象成Java中的Struts2标签或者JSTL标签，当然也有点Vue的意思：

```
{% for novel in novel_list %}
    <a href="/chapter/{{novel.id}} "><li>{{ novel.title }}</li></a>

{% endfor %}
```