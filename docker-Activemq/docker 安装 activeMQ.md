在安装完[Docker](https://so.csdn.net/so/search?q=Docker&spm=1001.2101.3001.7020)的机器上，安装activeMQ。

在docker hub上搜了一下[activeMQ](https://so.csdn.net/so/search?q=activeMQ&spm=1001.2101.3001.7020)的镜像，然后选择了，下载量最多的和start最多的,但是上次更新已经是三年前了。

![在这里插入图片描述](https://img-blog.csdnimg.cn/2020052211354697.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2xpbm1lbmdtZW5nXzEzMTQ=,size_16,color_FFFFFF,t_70)
拉取镜像：docker pull webcenter/activemq

 ![在这里插入图片描述](https://img-blog.csdnimg.cn/20200522112351462.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2xpbm1lbmdtZW5nXzEzMTQ=,size_16,color_FFFFFF,t_70)

 

查看镜像：docker images

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200522112600940.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2xpbm1lbmdtZW5nXzEzMTQ=,size_16,color_FFFFFF,t_70)
Docker运行ActiveMQ镜像
首先创建[挂载](https://so.csdn.net/so/search?q=挂载&spm=1001.2101.3001.7020)目录：

 [mkdir](https://so.csdn.net/so/search?q=mkdir&spm=1001.2101.3001.7020) /usr/soft/activemq

mkdir /usr/soft/activemq/log

 
运行activeMQ镜像：

   docker run --name='activemq' \
   -itd \
    -p 8161:8161 \
    -p 61616:61616 \
    -e ACTIVEMQ_ADMIN_LOGIN=admin \
    -e ACTIVEMQ_ADMIN_PASSWORD=123456 \
    --restart=always \
    -v /usr/soft/activemq:/data/activemq \
    -v /usr/soft/activemq/log:/var/log/activemq \
    webcenter/activemq:latest
 
61616是 activemq 的容器使用端口
8161是 web 页面管理端口
/usr/soft/activemq 是将activeMQ运行文件挂载到该目录
/usr/soft/activemq/log是将activeMQ运行日志挂载到该目录
-e ACTIVEMQ_ADMIN_LOGIN=admin 指定登录名
-e ACTIVEMQ_ADMIN_PASSWORD=123456 登录密码
查看activeMQ：
浏览器访问IP:8161，即可看到欢迎页，点击登录，输入账号密码，可进入activeMQ后台。