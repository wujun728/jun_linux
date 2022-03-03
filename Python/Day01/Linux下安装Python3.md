## 前言

Linux下大部分系统默认自带python2.x的版本，最常见的是python2.6或python2.7版本，默认的python被系统很多程序所依赖，比如centos下的yum就是python2写的，所以默认版本不要轻易删除，否则会有一些问题，如果需要使用最新的Python3那么我们可以编译安装源码包到独立目录，这和系统默认环境之间是没有任何影响的，python3和python2两个环境并存即可

## 安装


```
# 下载最新版本
wget https://www.python.org/ftp/python/3.7.1/Python-3.7.1.tar.xz
```

事先安装依赖，否则后期安装会报错：

```
yum -y install zlib*  
yum install libffi-devel -y
```

下面开始正式安装：

```
# 解压
tar -xvf Python-3.7.1.tar.xz
# 切换大目录
cd Python-3.7.1
# 配置编译
./configure
# 编译安装
make && make install
```

安装成功后python2 和 python3 可以同时使用：


```
[root@AY140216131049Z mzitu]# python2 -V
Python 2.7.5
[root@AY140216131049Z mzitu]# python3 -V
Python 3.7.1
# 默认版本
[root@AY140216131049Z mzitu]# python -V
Python 2.7.5
# 临时切换版本 <whereis python>
[root@AY140216131049Z mzitu]# alias python='/usr/local/bin/python3.7'
[root@AY140216131049Z mzitu]# python -V
Python 3.7.1

```





