---
layout: post
title: HBase shell 命令介绍
category: hbase
tags: [hbase]
---

HBase shell是HBase的一套命令行工具，类似传统数据中的sql概念，可以使用shell命令来查询HBase中数据的详细情况。安装完HBase之后，如果配置了HBase的环境变量，只要在shell中执行```hbase shell```就可以进入命令行界面，HBase的搭建可以参考我的上一篇文章：[hbase分布式集群搭建
](http://www.ityouknow.com/hbase/2017/07/25/hbase-cluster-setup.html)

## HBase介绍

### HBase简介

HBase的名字的来源于Hadoop database，即hadoop数据库，不同于一般的关系数据库，它是一个适合于非结构化数据存储的数据库，而且它是基于列的而不是基于行的模式。

HBase是一个分布式的、面向列的开源数据库,源于google的一篇论文[《bigtable：一个结构化数据的分布式存储系统》](https://static.googleusercontent.com/media/research.google.com/zh-CN//archive/bigtable-osdi06.pdf)。HBase是Google Bigtable的开源实现，它利用Hadoop HDFS作为其文件存储系统，利用Hadoop MapReduce来处理HBase中的海量数据，利用Zookeeper作为协同服务。

hbase提供了一个shell的终端给用户交互。使用命令hbase shell进入命令界面。通过执行 help可以看到命令的帮助信息。

### HBase的表结构

HBase以表的形式存储数据。表有行和列组成。列划分为若干个列族/列簇(column family)。

 
![](http://www.itmind.net/assets/images/2017/bigdata/hbase-table.png)

如上图所示，```key1```,```key2```,```key3```是三条记录的唯一的```row key```值，```column-family1```,```column-family2```,```column-family3```是三个列族，每个列族下又包括几列。比如```column-family1```这个列族下包括两列，名字是```column1```和```column2```，```t1:abc```,```t2:gdxdf```是由```row key1```和```column-family1-column1```唯一确定的一个单元```cell```。这个```cell```中有两个数据，abc和gdxdf。两个值的时间戳不一样，分别是t1,t2, hbase会返回最新时间的值给请求者。

这些名词的具体含义如下：

1、Row Key

与nosql数据库们一样,row key是用来检索记录的主键。访问hbase table中的行，只有三种方式：

- 通过单个row key访问   
- 通过row key的range  
- 全表扫描

Row key行键 (Row key)可以是任意字符串(最大长度是 64KB，实际应用中长度一般为 10-100bytes)，在hbase内部，row key保存为字节数组。

存储时，数据按照Row key的字典序(byte order)排序存储。设计key时，要充分排序存储这个特性，将经常一起读取的行存储放到一起。(位置相关性)

注意：

字典序对int排序的结果是1,10,100,11,12,13,14,15,16,17,18,19,2,20,21,…,9,91,92,93,94,95,96,97,98,99。要保持整形的自然序，行键必须用0作左填充。

行的一次读写是原子操作 (不论一次读写多少列)。这个设计决策能够使用户很容易的理解程序在对同一个行进行并发更新操作时的行为。

2、列族 column family

hbase表中的每个列，都归属与某个列族。列族是表的chema的一部分(而列不是)，必须在使用表之前定义。列名都以列族作为前缀。例如```courses:history```，```courses:math```都属于```courses```这个列族。

访问控制、磁盘和内存的使用统计都是在列族层面进行的。实际应用中，列族上的控制权限能帮助我们管理不同类型的应用：我们允许一些应用可以添加新的基本数据、一些应用可以读取基本数据并创建继承的列族、一些应用则只允许浏览数据（甚至可能因为隐私的原因不能浏览所有数据）。

3、单元 Cell

HBase中通过row和columns确定的为一个存贮单元称为cell。由```{row key, column( =<family> + <label>)```, version} 唯一确定的单元。cell中的数据是没有类型的，全部是字节码形式存贮。

4、时间戳 timestamp

每个cell都保存着同一份数据的多个版本。版本通过时间戳来索引。时间戳的类型是 64位整型。时间戳可以由hbase(在数据写入时自动 )赋值，此时时间戳是精确到毫秒的当前系统时间。时间戳也可以由客户显式赋值。如果应用程序要避免数据版本冲突，就必须自己生成具有唯一性的时间戳。每个cell中，不同版本的数据按照时间倒序排序，即最新的数据排在最前面。

为了避免数据存在过多版本造成的的管理 (包括存贮和索引)负担，hbase提供了两种数据版本回收方式。一是保存数据的最后n个版本，二是保存最近一段时间内的版本（比如最近七天）。用户可以针对每个列族进行设置。


## Hbase shell

HBase Shell的一些基本操作命令，列出了几个常用的HBase Shell命令，如下：

名称	| 命令表达式	
---  |---  
查看存在哪些表 | list 	
创建表	| create '表名称', '列名称1','列名称2','列名称N'
添加记录	| put '表名称', '行名称', '列名称:', '值'
查看记录	| get '表名称', '行名称'
查看表中的记录总数	| count '表名称'
删除记录	| delete '表名' ,'行名称' , '列名称'
删除一张表	| 先要屏蔽该表，才能对该表进行删除，第一步 disable '表名称' 第二步 drop '表名称'
查看所有记录	| scan "表名称"
查看某个表某个列中所有数据	| scan "表名称" , ['列名称:']
更新记录	| 就是重写一遍进行覆

### 一般操作

1、HBase shell中的帮助命令非常强大，使用help获得全部命令的列表，使用help ‘command_name’获得某一个命令的详细信息。 例如：

``` shell 
help ‘list'
```

2、查询服务器状态

``` shell 
status
```

3、查询Hbase版本：

``` shell 
version
```

4、查看所有表

``` shell 
list
```

### 增删改

1、创建一个表

``` shell 
create 'member','member_id','address','info’  
```

2、获得表的描述

``` shell 
describe 'member'
```

3、添加一个列族

``` shell 
alter 'member', 'id'
```

4、删除一个列族

``` shell 
alter 'member', {NAME => 'member_id', METHOD => 'delete’}
```

5、删除列

1）通过```delete```命令，我们可以删除id为某个值的```‘info:age’```字段，接下来的get就无视了

``` shell 
delete 'member','debugo','info:age'
get 'member','debugo','info:age'
```

2）删除整行的值：deleteall

``` shell 
deleteall 'member','debugo'
get 'member',’debugo'
```

6、通过enable和disable来启用/禁用这个表,相应的可以通过```is_enabled```和```is_disabled```来检查表是否被禁用。

``` shell 
is_enabled 'member'
is_disabled 'member'
```

7、使用exists来检查表是否存在

``` shell 
exists 'member'
```

8、删除表需要先将表disable。

``` shell 
disable 'member'
drop 'member'
```

9、put

在HBase shell中，我们可以通过put命令来插入数据。例如我们新创建一个表，它拥有id、address和info三个列簇，并插入一些数据。列簇下的列不需要提前创建，在需要时通过:来指定即可。

``` shell 
create 'member','id','address','info'
# 数据
put 'member', 'debugo','id','11'
put 'member', 'debugo','info:age','27'
put 'member', 'debugo','info:birthday','1987-04-04'
put 'member', 'debugo','info:industry', 'it'
put 'member', 'debugo','address:city','beijing'
put 'member', 'debugo','address:country','china'
put 'member', 'Sariel', 'id', '21'
put 'member', 'Sariel','info:age', '26'
put 'member', 'Sariel','info:birthday', '1988-05-09 '
put 'member', 'Sariel','info:industry', 'it'
put 'member', 'Sariel','address:city', 'beijing'
put 'member', 'Sariel','address:country', 'china'
put 'member', 'Elvis', 'id', '22'
put 'member', 'Elvis','info:age', '26'
put 'member', 'Elvis','info:birthday', '1988-09-14 '
put 'member', 'Elvis','info:industry', 'it'
put 'member', 'Elvis','address:city', 'beijing'
put 'member', 'Elvis','address:country', 'china'
```

### 查询

1、查询表中有多少行：count

``` shell 
count 'member'
```

2、get

1)获取一个id的所有数据

``` shell 
get 'member', ‘Sariel'
```

2)获得一个id，一个列簇（一个列）中的所有数据:

``` shell 
get 'member', 'Sariel', 'info'
```

3、查询整表数据

``` shell
scan 'member'
```

4、扫描整个列簇

``` shell
scan 'member', {COLUMN=>'info'}
```

5、指定扫描其中的某个列：

``` shell
scan 'member', {COLUMNS=> 'info:birthday'}
```

6、除了列```（COLUMNS）```修饰词外，HBase还支持```Limit```（限制查询结果行数），```STARTROW ```（```ROWKEY```起始行。会先根据这个```key```定位到```region```，再向后扫描）、```STOPROW```(结束行)、```TIMERANGE```（限定时间戳范围）、```VERSIONS```（版本数）、和```FILTER```（按条件过滤行）等。比如我们从```Sariel```这个```rowkey```开始，找下一个行的最新版本

``` shell
scan 'member', { STARTROW => 'Sariel', LIMIT=>1, VERSIONS=>1}
```

7、Filter是一个非常强大的修饰词，可以设定一系列条件来进行过滤。比如我们要限制某个列的值等于26

``` shell
scan 'member', FILTER=>"ValueFilter(=,'binary:26’)"
```

值包含6这个值：

``` shell
scan 'member', FILTER=>"ValueFilter(=,'substring:6')"
```

列名中的前缀为birthday的

``` shell
scan 'member', FILTER=>"ColumnPrefixFilter('birth') “
```

FILTER中支持多个过滤条件通过括号、AND和OR的条件组合

``` shell
scan 'member', FILTER=>"ColumnPrefixFilter('birth') AND ValueFilter ValueFilter(=,'substring:1988')"
```

```PrefixFilter```是对Rowkey的前缀进行判断,这是一个非常常用的功能。

``` shell
scan 'member', FILTER=>"PrefixFilter('E')"
```

**参考：**  
[hbase shell基础和常用命令详解](http://blog.pureisle.net/archives/1887.html)   
[HBase Shell 常用操作](http://debugo.com/hbase-shell-cmds/)