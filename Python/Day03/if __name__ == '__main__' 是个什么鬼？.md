有句话经典的概括了这段代码的意义：

“Make a script both importable and executable”

意思就是说让你写的脚本模块既可以导入到别的模块中用，另外该模块自己也可执行。

咋一看，其实我也不理解到底是个什么球意思，这里我们写两个Demo

test01.py：

```
#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 导入模块
import test02


def show():
    print('test01')


if __name__ == '__main__':
    show()

```

test02.py：

```
#!/usr/bin/python
# -*- coding: UTF-8 -*-


def show():
    print('test02')


if __name__ == '__main__':
    show()

```

这里我们运行test01.py，会输出test01。

如果我们吧test02.py修改为：

```
#!/usr/bin/python
# -*- coding: UTF-8 -*-


def show():
    print('test02')



show()

```

再次执行test01.py，它会输出test01 和 test02。


看到这里小伙伴应该明白了吧，在多模块编程的时候，一定要加入if __name__ == '__main__': 这样一个判断，否则引入模块的方法也会被执行。