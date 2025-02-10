## linux下yum安装JDK8


Linux安装软件方式有很多种，常见的有两种：rpm安装、yum安装。然而人生苦短，我选择yum安装

1、先查看centos中自带的jdk并卸载

如果从未安装过JDK环境，这一步可忽略

[root@root ~]# rpm -qa | grep jdk    //查看
[root@root ~]  rpm -e | grep java     //删除

# 卸载 -e --nodeps 强制删除
[root@kuangshen ~]# rpm -e --nodeps jdk1.8.0_121-1.8.0_121-fcs.x86_64

2、yum 命令查找jdk所有版本

两种方法：

//第一种：
[root@root ~]# yum -y list java*
//第二种：
[root@root ~]# yum search jdk

3、安装jdk

这里以 java-1.8.0-openjdk.x86_64 版本为例

[root@root ~]# yum install java-1.8.0-openjdk.x86_64
一直y确定

检验安装
[root@root ~]# java -version

4、设置jdk环境变量

[root@root alternatives]# vi /etc/profile
1
在文件最后加入如下配置：

#set java environment
JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.352.b08-2.el7_9.x86_64/jre
PATH=$PATH:$JAVA_HOME/bin
CLASSPATH=.:$JAVA_HOME/lib
export JAVA_HOME CLASSPATH PATH


5、使profile文件立马生效

[root@root alternatives]#. /etc/profile   

OK，end…

