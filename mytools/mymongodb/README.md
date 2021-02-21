微云（可快速扩充）
====================

MongoDB3.0-介绍
---------------------

MongoDB是一个介于关系数据库和非关系数据库之间的产品，是非关系数据库当中功能最丰富，最像关系数据库的。他支持的数据结构非常松散，是类似json的bjson格式，因此可以存储比较复杂的数据类型。Mongo最大的特点是他支持的查询语言非常强大，其语法有点类似于面向对象的查询语言，几乎可以实现类似关系数据库单表查询的绝大部分功能，而且还支持对数据建立索引。

它的特点是高性能、易部署、易使用，存储数据非常方便。主要功能特性有：

* 面向集合存储，易存储对象类型的数据。
* 模式自由。
* 支持动态查询。
* 支持完全索引，包含内部对象。
* 支持查询。
* 支持复制和故障恢复。
* 使用高效的二进制数据存储，包括大型对象（如视频等）。
* 自动处理碎片，以支持云计算层次的扩展性
* 支持RUBY，PYTHON，JAVA，C++，PHP等多种语言。
* 文件存储格式为BSON（一种JSON的扩展）
* 可通过网络访问
所谓“面向集合”（Collenction-Orented），意思是数据被分组存储在数据集中，被称为一个集合（Collenction)。每个 集合在数据库中都有一个唯一的标识名，并且可以包含无限数目的文档。集合的概念类似关系型数据库（RDBMS）里的表（table），不同的是它不需要定 义任何模式（schema)。
模式自由（schema-free)，意味着对于存储在mongodb数据库中的文件，我们不需要知道它的任何结构定义。如果需要的话，你完全可以把不同结构的文件存储在同一个数据库里。
存储在集合中的文档，被存储为键-值对的形式。键用于唯一标识一个文档，为字符串类型，而值则可以是各中复杂的文件类型。我们称这种存储形式为BSON（Binary Serialized dOcument Format）。

MongoDB服务端可运行在Linux、Windows或OS X平台，支持32位和64位应用，默认端口为27017。推荐运行在64位平台，因为MongoDB

在32位模式运行时支持的最大文件尺寸为2GB。

MongoDB把数据存储在文件中（默认路径为：/data/db），为提高效率使用内存映射文件进行管理。

压力测试工具
https://github.com/brianfrankcooper/YCSB/tree/master/mongodb


### 常用场景1 实时数据采集处理（脚本采用3.0的引擎）

> 采集网络获取数据.
>
> 存放到内存或者硬盘；硬盘顺序读写，确保高效；
>
> ## 日志输出到mongodb

数据采集-运行示例
---------------------
### 构造镜像包
> 进入到当前目录
> ## fig build
### 运行
> 进入到当前目录
> ## fig up -d && fig ps
### 观察日志
> 初始化数据
>
> sh initdb.sh //****必须先完成初始化，否则mongsink 不能自动生成数据库。
> mongo 192.168.59.103:27018  rs.status() ;mongo 192.168.59.103:27019 rs.status() ; mongo 192.168.59.103:27017 sh.status()
>
> 生产数据
> telnet 192.168.59.103 44449
>
> 输入:{ "name": "cxh", "sex": "man" }
>
> fig logs flume1
>
> mongo 192.168.59.103:27017
> show collections
> db.events.find()
>
> ## END

压力测试-运行示例
---------------------
### 构造镜像包
> 进入到当前目录
> ## fig build
### 运行
> 进入到当前目录
> ## fig up -d && fig ps
### 观察日志
> 初始化数据
>
> sh initdb.sh //****必须先完成初始化，否则mongsink 不能自动生成数据库。
>
> 下载并且运行一下代码：https://github.com/supermy/gs-accessing-data-mongodb
> 监控mongodb的运行状态：mongostat -h 192.168.59.103 -p 27017
> 查看服务器状态：mongo 192.168.59.103:27017   db.serverStatus()   
> ## END


数据导入-运行示例
---------------------
>
>导入csv格式的数据  用户：--db  集合：--c  格式:--type
>
>--headerline 表示CSV格式的第一行为字段，如果不指定这个参数，则会将CSV格式第一行当数据导入到目标库。
>

* 同步数据: rsync -avz -e ssh root@192.168.*.*:/file/mymongodb/initdbi*.js .
* 初始化数据: sh initdb-*.*.sh
* shell环境: mongo 192.168.*.*:27017
* 导入数据脚本；转换数据格式为tsv；转换文档编码  -v --stopOnError
* time ls \
    | xargs iconv -f utf8 -t utf8 -c \
    | awk -F"|" 'BEGIN{OFS="\t";}{NF=NF;print $0}'  \
    | mongoimport  -h 192.168.*.*:27017 -d gndata -c tellog --type tsv -f f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13,f14,f15,f16,f17,f18,19,f20,f21,f22,f23,f24,f25,f26,f27,f28,f29,f30,f31,f32,f33,f34,f35,f36

*
time ls gndata/1.txt \
    | xargs iconv -f utf8 -t utf8 -c \
    | awk -F"|" 'BEGIN{OFS="\t";}{NF=NF;print $0}'  \
    |  mongoimport -h 192.168.59.103:27017 -d gndata -c tellog --type tsv -f f1,f2,f3,f4


,f5,f6,f7,f8,f9,f10,f11,f12,f13,f14,f15,f16,f17,f18,19,f20,f21,f22,f23,f24,f25,f26,f27,f28,f29,f30,f31,f32,f33,f34,f35,f36

##存储优化
> docker容器默认的空间是10G,docker -d --storage-opt dm.basesize=20G,修改后需要重启docker。
启动docker服务时，加上–g参数指定docker工作目录，镜像等文件会存到这。

* --storage-opt dm.metadatadev=/dev/dm-26
* --storage-opt dm.datadev=/dev/dm-27
* --storage-opt dm.fs=xfs

##性能监控
mongostat -h 192.168.6.53:27017 1
> ## 数据导入
https://github.com/supermy/mytools/tree/master/mymongodb
http://t.cn/RwfruoO