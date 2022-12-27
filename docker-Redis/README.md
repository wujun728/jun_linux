#docker-redis

1. 指定使用 centos6

2. 更新 yum 源安装依赖 tar

3. 下载 redis-2.8.9.tar.gz

4. 编译 redis 指定端口 6379

5. 启动 redis

#测试方法  1
D:\redis>redis-cli.exe -h 54.223.168.107 -p 42711
redis 54.223.168.107:42711> set foo oschina
OK
redis 54.223.168.107:42711> get foo
"oschina"

#测试方法 2
D:\redis>redis-cli.exe -h redis-juapk.alaudacn.me -p 42711
redis redis-juapk.alaudacn.me:4set foo oschina
OK
redis redis-juapk.alaudacn.me:4get foo
"oschina"


关注我
====================
![程序员日记](http://git.oschina.net/uploads/images/2016/0121/093728_1bc1658f_12260.png "程序员日记")


