# Centos7 安装 jdk8 / java8 以及配置环境变量


 
1、安装方法
windows 下载，复制到 linux，解压，配置环境变量
linux 使用 wget 下载，解压，配置环境变量
linux 使用 yum 直接安装，环境变量自动配置好
2、查看是否已安装
看到下面结果，说明已经安装配置 jdk

[root@root-100 ~]# java -version
java version "1.8.0_191"
Java(TM) SE Runtime Environment (build 1.8.0_191-b12)
Java HotSpot(TM) 64-Bit Server VM (build 25.191-b12, mixed mode)
1
2
3
4
3、卸载
查看系统是否自带 jdk
rpm -qa |grep java
rpm -qa |grep jdk
rpm -qa |grep gcj
1
2
3
如果有输出信息，批量卸载系统自带
rpm -qa | grep java | xargs rpm -e --nodeps
1
如果使用 yum 安装的 jdk，请使用下面命令卸载
yum -y remove java-1.8.0-openjdk-headless-1.8.0.65-3.b17.el7.x86_64
1
4、下载
windows 下载地址https://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html
根据自己的系统下载对应的 jdk，文件结尾要是 tar.gz

把下载的 jdk 复制到 Centos7 指定目录下（/root/shared）
也可以在 Centos7 直接使用命令 wget 下载
 # 直接使用此方法下载会有问题，请使用下面命令下载
 wget -P /root/shared http://download.oracle.com/otn-pub/java/jdk/8u191-b12/2787e4a523244c269598db4e85c51e0c/jdk-8u191-linux-x64.tar.gz
 # 如果没有 wget 命令，可以是用下面命令安装 wget
 yum -y install wget
 # 下载，解决上面下载文件不全问题
 cd /root/shared
 wget --no-cookies --no-check-certificate --header "Cookie: gpw_e24=http%3A%2F%2Fwww.oracle.com%2F; oraclelicense=accept-securebackup-cookie" "http://download.oracle.com/otn-pub/java/jdk/8u191-b12/2787e4a523244c269598db4e85c51e0c/jdk-8u191-linux-x64.tar.gz"
1
2
3
4
5
6
7
或使用 yum 直接安装，则不需要下面的 配置和生效 ，直接验证即可
检查 yum 中有没有 java1.8 包
yum list java-1.8*
1
开始安装
yum install java-1.8.0-openjdk* -y
1
5、配置
解压

# 解压到 /usr/java
tar -zxvf /root/shared/jdk-8u191-linux-x64.tar.gz
1
2
配置 profile

 # 编辑profile，
 vi /etc/profile
 # 在上面增加下面内容
 JAVA_HOME=/usr/java/jdk1.8.0_191
 JRE_HOME=$JAVA_HOME/jre
 PATH=$PATH:$JAVA_HOME/bin:$JRE_HOME/bin
 CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar:$JRE_HOME/lib
 export JAVA_HOME JRE_HOME PATH CLASSPATH
1
2
3
4
5
6
7
8
变量	含义
JAVA_HOME	指明JDK安装路径，就是刚才安装时所选择的路径，此路径下包括lib，bin，jre等文件夹（tomcat，Eclipse的运行都需要依靠此变量）。
CLASSPATH	为java加载类(class or lib)路径，只有类在classpath中，java命令才能识别，设：.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar:$JRE_HOME/lib。CLASSPATH 变量值中的.表示当前目录
PATH	使得系统可以在任何路径下识别java命令，设为：$JAVA_HOME/bin:$JRE_HOME/bin。
特别注意	环境变量值的结尾没有任何符号，不同值之间用:隔开（windows中用;）
6、生效
source /etc/profile
1
7、验证
 [root@root-100 ~]# java -version
 java version "1.8.0_191"
 Java(TM) SE Runtime Environment (build 1.8.0_191-b12)
 Java HotSpot(TM) 64-Bit Server VM (build 25.191-b12, mixed mode)
————————————————
版权声明：本文为CSDN博主「沧海一粟X」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/axing2015/article/details/83614800