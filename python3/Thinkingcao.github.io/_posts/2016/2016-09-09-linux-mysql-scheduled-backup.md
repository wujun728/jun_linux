---
layout: post
title: linux定时备份mysql并同步到其它服务器
category: mysql
tags: [mysql]
---

数据在任何一家公司里面都是最核心的资产，定期备份则是为了保证数据库出现问题的时候能够及时回滚到最近的备份点，将损失缩小到最小

这篇文章将会两部分来说明：1、mysql的定期备份；2、同步到其它服务器


## mysql 备份

### 备份还原某个数据库

备份还原

``` shell
# 导出数据库
/usr/bin/mysqldump -u root -ppwd database > database20160929.sql
# 导入数据库
mysql -u root -p database < database20160929.sql
```

备份到压缩文件从压缩文件导入

``` shell
#备份到压缩文件
/usr/bin/mysqldump -u root -ppwd database  | gzip > database20160929.sql.gz
#从压缩文件导入
gzip < database20160929.sql.gz | mysql -u root -p database
```

###  crontab定时备份

1、创建备份目录

``` shell
# root 用户,创建备份目录
mkdir -p /bak/mysqlbak
cd /bak/mysqldata
```

2、编写运行脚本

``` shell
vi  /usr/sbin/bakmysql.sh
```

脚本代码：

``` shell
#!/bin/bash
# Name:bakmysql.sh
# This is a ShellScript For Auto DB Backup and Delete old Backup
#
backupdir=/bak/mysqlbak
time=` date +%Y%m%d%H `
mysql_bin_dir/mysqldump -u root -ppwd database | gzip > $backupdir/database$time.sql.gz
#
find $backupdir -name "name_*.sql.gz" -type f -mtime +7 -exec rm {} ; > /dev/null 2>&1

#
```

脚本说明：

> ```backupdir``` mysql备份地址  
> ```root``` mysql用户名  
> ```pwd``` mysql密码  
> ```database``` 数据库名  
> ```mysql_bin_dir``` mysql的bin路径；  
> ```time=` date +%Y%m%d%H ` ```也可以写为```time="$(date +"%Y%m%d$H")" ```其中``` ` ```  符号是TAB键上面的符号，不是ENTER左边的'符号，还有date后要有一个空格。  
> ```type f```   表示查找普通类型的文件，f表示普通文件。  
> ```mtime +7```   按照文件的更改时间来查找文件，+7表示文件更改时间距现在7天以前；如果是 -mmin +5 表示文件更改时间距现在5分钟以前。  
> ```exec rm {} \```  表示执行一段shell命令，exec选项后面跟随着所要执行的命令或脚本，然后是一对儿{}，一个空格和一个\，最后是一个分号。  
> ```/dev/null 2>&1```  把标准出错重定向到标准输出，然后扔到/DEV/NULL下面去。通俗的说，就是把所有标准输出和标准出错都扔到垃圾桶里面；其中的& 表示让该命令在后台执行。   

3、为脚本添加执行权限

``` shell
# chmod +x /usr/sbin/bakmysql.sh
```

4、设置crontab定时执行

``` shell
vi /etc/crontab 
#在最后一行中加入：  
00 3 * * * root /usr/sbin/bakmysql.sh
#表示每天3点00分执行备份
```


>注：crontab配置文件格式如下：  
>分　时　日　月　周　 命令


5、重启crontab

``` shell
/etc/rc.d/init.d/crond restart  
```

这样就完了定时备份并清理前7天的备份数据



## 同步到其它服务器

这里使用Linux同步文件工具rsync+inotify来进行文件的同步

### rsync

rsync是类unix系统下的数据镜像备份工具——remote sync。一款快速增量备份工具 Remote Sync，远程同步 支持本地复制，或者与其他SSH、rsync主机同步

**用法**

``` shell
rsync src dest
```

这是最简单的用法，表示同步src,dest文件。（即，执行之后，dest的文件与src的相同，以src的为准)

常用选项
> ```-a```: 等价于-rlptgoD,归档式  
> ```-r```: 递归  
> ```-l```: 复制软件链接  
> ```-p```: 保留权限信息  
> ```-t```: 将src的修改时间，同步到dest  
> ```-g```: 同步组信息(group)  
> ```-o```: 同步拥有者信息(own)  
> ```-D```: 保持字符与块设备文件  
> ```-z```: 启用压缩传输  
> ```–delete```：如果src没有此文件，那么dest也不能有，即在dest删除src里没有的文件。（如果你使用这个选项，就必须搭配-r选项一起）  


``` shell
## 将本地/bak/mysqlbak/文件同步到 远程服务器 /bak/mysql/bak 目录下面 排除 mysqlbak/index目录 通过ssh端口
rsync -vzacu  /bak/mysqlbak/  root@192.168.53.86:/bak/mysqlbak   --exclude  "mysqlbak/index"   -e "ssh -p 22"
# 将远程目录 /bak/mysqlbak下的文件同步到本地 /bak/mysqlbak/目录下
rsync -vzrtopg --progress --delete root@192.168.53.85:/bak/mysqlbak  /bak
```

**启用rsync服务器端同步远程文件**

rsycn的服务端为服务器的文件接收端，rsycn的客户端为服务器的文件推动端。


**rsycn的服务端/文件接收端配置**

服务端需要开启rsyncd服务

添加配置文件rsyncd.conf

``` shell
vi /etc/rsyncd.conf
#以下是全局配置
log file = /var/log/rsyncd.log
pid file = /var/run/rsyncd.pid
lock file = /var/lock/rsyncd
[mysqlbak]     #模块名，在源服务器指定这个名字
   comment = sync rsync/home      #描述信息
   path = /bak/mysqlbak      #备份目录
   use chroot=no           #不使用chroot，不用root权限
   read only = no          #设置本地备份目录为读写权限
   uid=root          
   gid=root
   max connections=10       #客户端最大连接数
   auth users = root      #指定数据同步用户
   secrets file = /etc/rsyncd.pass          #指定数据同步用户信息文件
   hosts allow=192.168.53.0/85     #允许连接的客户端
   ignore errors = yes     #忽略出现I/O错误
   timeout = 600
```

创建认证文件

``` shell
  vi /etc/rsyncd.pass
  ##代码
  root:root      #格式是用户名：密码
  #属主要有权限读这个文件，否则会报没权限
  chmod 600 /etc/rsyncd.pass  
```

修改/etc/xinetd.d/rsync文件，disable 改为 no

``` shell
service rsync
{
        disable = no
        socket_type     = stream
        wait            = no
        user            = root
        server          = /usr/bin/rsync
        server_args     = --daemon
        log_on_failure  += USERID
}
```

启动服务端

``` shell
rsync --daemon --config=/etc/rsyncd.conf
```

**rsycn的客户端/文件发送端配置**

客户端配置简单 只需要配置密码既可

``` shell
  vi /etc/rsync_client.pwd
  ##代码
  root    #只需要填写rsync服务的密码
  #属主要有权限读这个文件，否则会报没权限
  chmod 600 /etc/rsync_client.pwd 
```

客户端同步测试

``` shell
/usr/bin/rsync -auvrtzopgP --progress --password-file=/etc/rsync_client.pwd /bak/mysqlbak/ root@192.168.53.86::mysqlbak
```

> **rsync只是一次性同步,如果需要实时同步就需要引入另一个工具了**

### inotify

 Inotify 是一种强大的、细粒度的、异步的文件系统事件监控机制，linux内核从2.6.13起，加入了Inotify支持，通过Inotify可以监控文件系统中添加、删除，修改、移动等各种细微事件，利用这个内核接口，第三方软件就可以监控文件系统下文件的各种变化情况，而inotify-tools就是这样的一个第三方软件。

> Inotify只需要要按照部署在同步的客户端，当监控的文件有变化触动 rsync脚本来同步 

安装

``` shell
yum install inotify-tools
```

配置监控的文件路径

``` shell
vi /etc/inotify_exclude.lst
#代码
/bak/mysqlbak #监控目录
@/bak/log #排除监控目录
```

rsync排除监控文件目录

``` shell
vi /etc/rsyncd.d/rsync_exclude.lst
#代码
src/*.html*
src/js/
src/2014/20140[1-9]/
```

客户端同步到远程的脚本rsync.sh

``` shell
#rsync auto sync script with inotify
#variables
current_date=$(date +%Y%m%d_%H%M%S)
source_path=/bak/mysqlbak/
log_file=/var/log/rsync_client.log
#rsync
rsync_server=192.168.53.86
rsync_user=root
rsync_pwd=/etc/rsync_client.pwd
rsync_module=mysqlbak
INOTIFY_EXCLUDE='(.*/*\.log|.*/*\.swp)$|^/tmp/src/mail/(2014|20.*/.*che.*)'
RSYNC_EXCLUDE='/bak/rsync_exclude.lst'
#rsync client pwd check
if [ ! -e ${rsync_pwd} ];then
    echo -e "rsync client passwod file ${rsync_pwd} does not exist!"
    exit 0
fi
#inotify_function
inotify_fun(){
    /usr/bin/inotifywait -mrq --timefmt '%Y/%m/%d-%H:%M:%S' --format '%T %w %f' \
          --exclude ${INOTIFY_EXCLUDE}  -e modify,delete,create,move,attrib ${source_path} \
          | while read file
      do
          /usr/bin/rsync -auvrtzopgP --exclude-from=${RSYNC_EXCLUDE} --progress --bwlimit=200 --password-file=${rsync_pwd} ${source_path} ${rsync_user}@${rsync_server}::${rsync_module} 
      done
}
#inotify log
inotify_fun >> ${log_file} 2>&1 &
```

给脚本执行权限，执行后就可以了

``` shell
chmod 777 rsync.sh
./rsync.sh 
```

## 参考：

[Linux下同步工具inotify+rsync使用详解](http://seanlook.com/2014/12/12/rsync_inotify_setup/)


-------------

**作者：纯洁的微笑**  
**出处：[www.ityouknow.com](http://www.ityouknow.com)**   
**版权所有，欢迎保留原文链接进行转载 :)**
