# Linux下的环境部署和项目发布



#### 1.查看系统版本

```
sudo uname --m
```

> i686 //表示是32位
> x86_64 // 表示是64位

#### 2.下载对应版本软件，jdk和Tomcat(切记注意版本)

jdk:
下载地址：http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html
Tomcat:
下载地址：http://tomcat.apache.org/download-70.cgi

#### 3.使用XftpPortable传输软件上Liunx系统上

> 养成好习惯新建文件夹进行上传

#### 4.安装jdk

###### (1)jdk安装

```
rpm包:
 # rpm -ivh jdk-7u55-linux-x64.rpm
```

  tar.gz包:解压缩

```
    # mkdir /usr/java



    # cd /usr/java



    # tar -zxvf /software/jdk-7u55-linux-x64.tar.gz
```

###### (2)配置环境变量

```
    # vi /etc/profile



    export JAVA_HOME=/usr/java/default



    export JAVA_BIN=$JAVA_HOME/bin



    export PATH=$PATH:$JAVA_HOME/bin



    export CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar



    export PATH=$JAVA_HOME/bin:$JRE_HOME/bin:$PATH
######(3)使配置生效(重启服务器），或者使用下面指令
    # source /etc/profile
```

###### (4) 测试jdk.

```
    # java -version
```

#### 5.安装Tomcat(压缩包要先解压缩，后安装)

```
    # mkdir /usr/local/tomcat



    # cd /usr/local/tomcat



    # tar -zxvf /software/apache-tomcat-7.0.54.tar.gz
```

*记得要打开一下防火墙*

```
    # /sbin/iptables -I INPUT -p tcp --dport 8080 -j ACCEPT



    # service iptables save



    # service iptables restart
或直接修改文件/etc/sysconfig/iptables.
    # vi /etc/sysconfig/iptables



    -A INPUT -p tcp -m tcp --dport 8080 -j ACCEPT



    # service iptables restart
```

#### 6.部署项目

将打好的war包上传至webApp下

###### 看是否已经有tomcat在运行了

```
　　ps -ef |grep tomcat
```

###### 如果在运行先kill进程id(如进程为6632)

```
kill -9 6632
```

###### 切换到对应Tomcat目录下

```
cd /java/tomcat
```

###### 执行启动tomcat

```
bin/startup.sh
```

###### 停止tomcat

```
bin/shutdown.sh
```

###### 看tomcat的控制台输出

```
　　tail -f logs/catalina.out
```