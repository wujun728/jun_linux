docker安装hadoop伪集群（虚拟机，阿里云适用）


注意：是阿里云的机器，系统是centOS 8 ，已经提前安装docker。
一、首先安装hadoop镜像
 1、 在docker中查找hadoop 镜像

docker search hadoop


2、 选择star数量最多的镜像拉取就可以

docker run --name hadoop1 -d -h master docker.io/sequenceiq/hadoop-docker
3、查看镜像

docker images
4、创建master节点

docker run --name hadoop1 -d -h master docker.io/sequenceiq/hadoop-docker
 参数解释：
--name ：设置容器的名称 -d：在后台运行 -h：为容器设置主机名

5、以此方法创建slave1和slave2节点

#slave1节点
docker run --name hadoop2 -d -h slave1 docker.io/sequenceiq/hadoop-docker
#slave2节点
docker run --name hadoop3 -d -h slave2 docker.io/sequenceiq/hadoop-docker
6、查看容器

docker ps -s


 7、进入容器查看jdk

1、docker exec -it hadoop1 bash

2、java -version


8、配置ssh生成秘钥，所有的节点都要配置。进入容器后，启动ssh

/etc/init.d/sshd start
生成秘钥

ssh-keygen -t rsa

回车 、y、 回车 、回车
进入/root/.ssh/目录

cd /root/.ssh/
复制公钥到authorized_keys中

cat id_rsa.pub > authorized_keys
查看authorized_keys

cat authorized_keys
9、其他节点（hadoop2、hadoop3）都要执行一下第8个步骤

10、将三个容器中的公钥向其余节点进行复制，三个节点的公钥应该都一样，且里面都有三个。

推荐复制出来，然后凑齐一起粘贴回去。每个容器都要有三个呀，记得。



11、 查看ip地址，使用ifconfig命令查看每个容器ip地址



12、为每个容器设置地址vi /etc/hosts（ip是每个容器的ip地址 后面是容器的节点名称，把三个容器都配置上）

172.17.0.6      master

172.17.0.7      slave1

172.17.0.8      slave2

13、测试一下：(记得登录后一定要用exit退出才能回到根节点)

ssh master


 类似于这样然后再把另外两个测试一下

 ssh slave1
ssh slave2

二、配置hadoop（在master节点上）
1、进入容器查找 hadoop-env.sh存放位置

find / -name hadoop-env.sh
2、配置文件的目录一般都在/usr/local/hadoop-2.7.0/etc/hadoop下面

进入/usr/local/hadoop-2.7.0/etc/hadoop目录下

cd /usr/local/hadoop-2.7.0/etc/hadoop
3、查看 hadoop-env.sh文件(已经帮我们配置好了)

vi hadoop-env.sh
4、查找core-site.xml

find / -name core-site.xml
5、进入/usr/local/hadoop-2.7.0/etc/hadoop/目录下

cd /usr/local/hadoop-2.7.0/etc/hadoop/
6、查看并编辑core-site.xml文件

vi core-site.xml
#添加如下配置：
<property>
 	 <name>hadoop.tmp.dir</name>
  	<value>/hadoop/tmp</value>
</property>
7、查找hdfs-site.xml

find / -name hdfs-site.xml
8、进入/usr/local/hadoop-2.7.0/etc/hadoop/目录下

cd /usr/local/hadoop-2.7.0/etc/hadoop/
9、配置hdfs-site.xml

vi hdfs-site.xml
slave数量要大于等于备份的数量，否则会报错，当前是2个slave，所以满足条件。

10、查找mapred-site.xml

find / -name mapred-site.xml
进入/usr/local/hadoop-2.7.0/etc/hadoop/目录下

cd /usr/local/hadoop-2.7.0/etc/hadoop/
配置mapred-site.xml(已经帮我们配置好了)
vi mapred-site.xml
查找yarn-site.xml

find / -name yarn-site.xml
进入/usr/local/hadoop-2.7.0/etc/hadoop/目录下

cd /usr/local/hadoop-2.7.0/etc/hadoop/
配置yarn-site.xml

vi yarn-site.xml
<property>
        <name>yarn.resourcemanager.address</name>
        <value>master:8032</value>
</property>

<property>
        <name>yarn.nodemanager.aux-services</name>
        <value>mapreduce_shuffle</value>
</property>

<property>
        <name>yarn.nodemanager.aux-services.mapreduce.shuffle.class</name>
        <value>org.apache.hadoop.mapred.ShuffleHandler</value>
</property>

<property>
        <name>yarn.resourcemanager.scheduler.address</name>
        <value>master:8030</value>
</property>

<property>
        <name>yarn.resourcemanager.resource-tracker.address</name>
        <value>master:8031</value>
</property>

<property>
        <name>yarn.resourcemanager.admin.address</name>
        <value>master:8033</value>
</property>

<property>
        <name>yarn.resourcemanager.webapp.address</name>
        <value>master:8089</value>
</property>

 11、将这些参数发送到其它节点(slave1/slave2)

scp /usr/local/hadoop-2.7.0/etc/hadoop/yarn-site.xml slave1:/usr/local/hadoop-2.7.0/etc/hadoop/
scp /usr/local/hadoop-2.7.0/etc/hadoop/yarn-site.xml slave2:/usr/local/hadoop-2.7.0/etc/hadoop/
 三、运行hadoop
1、查找hadoop

find / -name hadoop
2、进入/usr/local/hadoop-2.7.0/bin/目录

cd /usr/local/hadoop-2.7.0/bin/
3、在master上格式化namenode

./hadoop namenode -format
注意注意注意：
如果在日志信息中能看到这一行,则说明 namenode格式化成功：common Storage: Storage directory /data/hadoop repo/dfs/name has been successfully formatted，大家可以把日志信息粘贴出来，Ctrl+F查找一下关键字，看是否有这句话，如果有，代表格式化namenode成功。


5、在master上启动集群

1、cd /usr/local/hadoop-2.7.0/sbin/

2、./start-all.sh

如果报错告诉端口被占用，那么就先停止,然后再启动：
./stop-all.sh
./start-all.sh

5.jps查看进程，查看到，说明已启动
————————————————
版权声明：本文为CSDN博主「codesChao」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/qq_46063016/article/details/123639616