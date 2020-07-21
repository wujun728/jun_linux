# 常用模块说明

os 操作系统模块，文件路径操作等

sys 程序系统本身模块，获取参数，导入的模块，输入输出等

time timestamp时间戳，struct_time时间元组，format time 格式化时间模块 

datetime模块 datatime模块重新封装了time模块，提供更多接口

hashlib加密 hashlib主要提供字符加密功能，将md5和sha模块整合到了一起，支持md5,sha1, sha224, sha256, sha384, sha512等算法

logging模块简介 logging模块是Python内置的标准模块，可以设置级别

subprocess模块 subprocess是Python 2.4中新增的一个模块，它允许你生成新的进程

# 总结
那么我们到底该用哪个模块、哪个函数来执行命令与系统及系统进行交互呢？下面我们来做个总结：

首先应该知道的是，Python2.4版本引入了subprocess模块用来替换os.system()、os.popen()、os.spawn*()等函数以及commands模块；也就是说如果你使用的是Python 2.4及以上的版本就应该使用subprocess模块了。
如果你的应用使用的Python 2.4以上，但是是Python 3.5以下的版本，Python官方给出的建议是使用subprocess.call()函数。Python 2.5中新增了一个subprocess.check_call()函数，Python 2.7中新增了一个subprocess.check_output()函数，这两个函数也可以按照需求进行使用。
如果你的应用使用的是Python 3.5及以上的版本（目前应该还很少），Python官方给出的建议是尽量使用subprocess.run()函数。
当subprocess.call()、subprocess.check_call()、subprocess.check_output()和subprocess.run()这些高级函数无法满足需求时，我们可以使用subprocess.Popen类来实现我们需要的复杂功能。
json ,pickle模块
JSON(JavaScript Object Notation, JS 对象标记) 是一种轻量级的数据交换格式。JSON的数据格式其实就是python里面的字典格式，里面可以包含方括号括起来的数组，也就是python里面的列表。

在python中，有专门处理json格式的模块—— json 和 picle模块

  Json   模块提供了四个方法： dumps、dump、loads、load

pickle 模块也提供了四个功能：dumps、dump、loads、load

# 参考地址
常用模块和使用案例
https://www.cnblogs.com/wf-linux/archive/2018/08/01/9400354.html

