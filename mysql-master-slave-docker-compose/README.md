### mysql 主从复制概述  
- 1.`mysql`  主从复制是指从一个主数据库将数据复制到一个或者多个从数据库节点，数据的复制是异步的，开发者可以指定需要复制的数据库以及排除复制的数据库完成任务。   
- 2.`mysql` 的优化方向：sql语句、索引、数据表结构设计、服务器硬件、架构（主从同步、读写分离）, 本篇主要目的在于数据库架构优化.  


###  mysql 部署主从同步、实现读写分离  
> 1.本篇主要是快速部署一套主从同步的mysql服务器, 方便程序实现读写分离.    
> 2.注意事项：主从同步、读写分离一般都会部署在不同的服务器，但是如果数据库服务器配置比较高，又考虑到一个进程对服务器资源的利用率是有限的，那么结合docker容器虚拟化技术，我们就可以在一台服务器实现多台的效果，对高配服务器的资源，也做到了利用率最大化.  

### 主从同步原理示意图
- 1.主数据库开启binlog日志记录功能，这样针对 `dml(create、insert、update、delete等)` 操作类sql,mysql服务器主进程就会在主服务器指定的目录，生成二进制日志文件(binlog).  
- 2.主服务器的 `Binlog Dump线程` 负责监控`binlog` 日志变化,实时发送最新的操作内容发送给 `slave` 的 `i/o线程` ,然后继续等待主服务器 `binlog` 日志新的变化.   
- 3.从服务器的 `i/o线程` 接受到主服务器发送的 `binlog` 数据后，写入中继日志 `RelayLog` ,然后由 `sql 线程` 从 `RelayLog` 中解析出 sql命令,执行它,从而实现了主从数据一致性.  
- 4.mysql8主从复制官方参考资料：`https://dev.mysql.com/doc/refman/8.0/en/replication-threads-monitor-main.html`  
![master_status](https://www.ginskeleton.com/images/master-to-slave.png)

####  1.相关配置项介绍  
- 1.1主数据库(master)配置文件
```code  
# 该路径下的配置文件默认即可，如果需要修改，请您确保熟悉每项的含义
./conf/master/my.cnf

```

- 1.2.从数据库(slave)配置文件
```code  
# 该路径下的配置文件默认即可，如果需要修改，请您确保熟悉每项的含义
./conf/slave/my.cnf

```

####  2.构建步骤  
 - 1.下载本项目，进入 docker-compose.yml 文件同目录
```code   

# 首先给配置文件设置权限，否则后面的配置都不会生效(mysql8必须操作)
chmod  644   ./conf/master/my.cnf    ./conf/slave/my.cnf

# 执行命令快速启动主从服务容器
docker-compose  up  -d

# 查看主、从数据库容器是否启动ok
docker-compose  ps

```

#### 3.数据库配置其他命令
 - 3.1.主数据库(master)执行的命令  
 > 相关参数解释  
 > 在主服务器创建用户，从数据库就可以使用此账号连接服务器，读取binlog日志  

```code   

# mysql5.7 版本
# *.* 表示任意数据库、任意数据表  
# data_sync 表示账号  
# 192.168.6.113 表示客户端来源IP  
# v9#QKUeS*6 密码，尽量有大写、小写、字母、特殊符号  
GRANT REPLICATION SLAVE ON *.* TO 'data_sync'@'192.168.6.113' IDENTIFIED BY 'v9#QKUeS*6';

# mysql8 版本
# 主数据库(master)创建数据同步专用账号，从数据库（slave）通过这个账号就可以登陆到主数据库，获取数据。
CREATE USER data_sync IDENTIFIED BY 'v9#QKUeS*6';
GRANT SELECT, REPLICATION SLAVE, REPLICATION CLIENT ON *.* TO 'data_sync'@'%';
GRANT ALL PRIVILEGES ON *.* TO 'data_sync'@'%' ;

# 刷新权限
FLUSH PRIVILEGES;

# 获取主数据库 binlog 日志状态，主要是确定日志的文件名以及从数据库开始读取的日志位置. 
# 记录一下File 和Position, 用于在从服务器配置连接的主服务器时的部分参数
SHOW MASTER  STATUS; 

```
![master_status](https://www.ginskeleton.com/images/master_status.jpg)

- 3.2.从数据库(slave)执行的命令
```code   

# 首先停止数据同步相关的线程： slave I/O 线程和 slave SQL 线程
STOP SLAVE  ;

# 为了避免可能发生的错误，直接重置客户端
RESET  SLAVE  ;

#设置主从同步隶属关系
# mysql_master 为主数据库的容器服务名称，如果是非容器部署，就填写主服务器的ip
# MASTER_LOG_FILE=binlog_filename.000005 为主数据库binlog的文件名
# MASTER_LOG_POS=156 为binlog日志开始同步时的位置
# Binlog_Do_DB=db_ginskeleton  需要同步的数据库
# Binlog_Ignore_DB=mysql,test  指定忽略同步的数据库

SET @binlog_filename='binlog_filename.000005'  ;
SET @binlog_pos=156  ;
CHANGE MASTER TO MASTER_HOST='mysql_master',MASTER_PORT=3306,MASTER_USER='data_sync',MASTER_PASSWORD='v9#QKUeS*6',MASTER_LOG_FILE=@binlog_filename,MASTER_LOG_POS=@binlog_pos;

#启动slaver 服务
START   SLAVE  ;    //  如果报错，请依次执行：（停止）STOP SLAVE、： （重置）RESET  SLAVE ，然后   启动 （START   SLAVE ）


# 查看从数据库的状态
SHOW   SLAVE  STATUS  ;


```
![master_status](https://www.ginskeleton.com/images/slave_status.png)


#### 4.读写分离验证  
> 4.1 至此我们已经配置完成了 主从同步，那么接下来就可以把主、从数据库的ip、账号、密码、端口配置在程序,实现读写分离方案.  
> 4.2 您可以在程序操作数据库(增删改查),在主从数据库监听，看看sql命令的执行位置,就可以确定本方案是否生效.  
```code  

# 主、从数据库开启sql监听日志打印功能，以下命令需要在从数据库服务器执行，然后在主服务器执行相关sql命令，在系统层面进行独立验证
#指定sql执行监听日志文件
SET GLOBAL general_log_file='/tmp/mysql.log';

# 开启sql监听
SET GLOBAL general_log=on;

#执行以下命令观察实时打印的sql执行记录
 tail  -f -n  100  /tmp/mysql.log 

#验证后关闭sql监听即可
SET GLOBAL general_log=off;

```

#### 5.关于主从同步，读写分离可能带来的其他问题
> 1.主从同步方案，理论上两个数据库之间的数据的确存在延迟问题。   
> 2.我们使用 ab 命令模拟高并发环境测试主从同步方案延迟时，发现在高并发环境还是比较明显的,具体表现为:在主数据库刚插入的数据，根据id在从数据库查询时，并没有拿到数据,因此对于新增、查询比较紧密的子系统，建议切换到主数据库，而对于大屏展示系统等几乎都是查询类接口的子系统,建议切换到从数据库。   
> 3.实际面临的环境可能更加多样、更复杂,只有您熟悉每种方案的适用范围以及它的局限性,才能做出正确的技术选型.  
```code 
# 请自行阅读相关资料，了解主从同步存在的数据延迟问题 以及解决办法 
https://blog.csdn.net/weixin_33066433/article/details/113944731
http://blog.csdn.net/u012845423/article/details/88977955

```
