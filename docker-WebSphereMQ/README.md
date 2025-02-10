#docker-wmq

前几天已经把WebSphere MQ 7.5安装在CentOS 7上了，今天经理又要求在另外一个云的另一台服务器上准备一个新环境，看起来安装MQ的需求还是很旺盛的。因此笔者决定制作一个Docker镜像，以加速MQ的准备
##MQ软件的安装
1. 在一台Linux服务器上安装Docker
2. 上传WS_MQ_LINUX_ON_X86_64_7.5.0.2_IMG.tar.gz；解压
3. 在解压安装文件的目录中执行以下命令，进入Docker容器
```
docker run -it -v $PWD:/tmp/software centos:7.1.1503 /bin/bash
```
4. 在/tmp/software目录下安装mq
执行 ```./mqlicense.sh -accept -text_only```，接受许可证
执行 ```rpm -ivh MQSeriesRuntime-*.rpm MQSeriesServer-*.rpm```
5. 执行exit，退出Docker容器
6. 执行以下命令，把安装了MQ的Docker容器提交为一个Image
```
docker commit wmq_container xsh/wmq75:0.1
```

##制作可以提供服务的MQ image
1. 请在以下地址下载相关的配置脚本
[http://git.oschina.net/gongxusheng/docker-wmq](http://git.oschina.net/gongxusheng/docker-wmq)
其中MQ队列管理器的配置和启动脚本在start_queue_manager.sh中，可以根据你的规划做相应的修改
如果端口不是默认的1414，请同时在Dockerfile中修改EXPOSE
2. 在Dockerfile目录中执行，创建image
```
docker build --tag xsh/wmq75:0.2 .
```
3. image创建成功以后，即可使用以下的命令启动服务
```
docker run -d -p 1414:1414 --name wmq xsh/wmq75:0.2
```

4. 如果要自定义队列管理器，可以仿照start_queue_manager.sh写一个自己的配置文件(如some_queue_manager.sh)，启动时加载即可
```
docker run -d -p <yourport>:<yourport> -v $PWD/some_queue_manager.sh:/start_queue_manager.sh --name wmq xsh/wmq75:0.2
```

##使用MQ Explorer测试队列
1. 使用MQ的Windows介质安装MQ Explorer，并启动
2. 左侧菜单中在Queue Managers右键，选择Add Remote Queue Manager...
3. Queue Manger Name中填写远程对列管理器的名称，默认为TESTQM。在后续的配置页面中输入队列管理器所在服务器的ip，用户名为mqm(无密码)
如果连接成功，恭喜，安装配置已经成功。


##关于人工而非Dockerfile安装MQ软件
由于Dockerfile安装时无法有效的删除安装介质，会导致做出的image过大，所以笔者使用了人工安装的方法。有兴趣的读者可以试试Dockerfile2，做出的image要927MB，比前文所述方法做出的Image要大约500MB
##关于操作系统参数的优化
MQ安装步骤中有一步要求su mqm -c "/opt/mqm/bin/mqconfig"，检查MQ的执行环境符合最小要求，不符合最小要求则可能无法启动队列管理器。结合Docker Engine的特点，可以在运行Docker Engine的服务器做相应的配置，Docker容器启动时即会带入相关的参数。

_说明_：经过测试，修改运行Docker Engine服务器系统参数的方法在Ubuntu Server 14.04.4 LTS 64bit + Docker 1.10.有效果；在Cent 6.5 + Docker 1.7.1没有效果。如果哪位读者知道在Docker 1.7.1上的设置方法，请给我留言

1. 执行```docker exec -it wmq /bin/bash```，进入Docker容器

2. 执行 ```su mqm -c "/opt/mqm/bin/mqconfig```", 查看哪些参数需要设置

3. 按照mqconfig的提示信息设置操作系统参数，如笔者的环境提示以下的Fail
```
System V Semaphores
  semmsl     (sem:1)  250 semaphores                     IBM>=500          FAIL
  semmns     (sem:2)  1 of 32000 semaphores      (0%)    IBM>=256000       FAIL
  semopm     (sem:3)  32 operations                      IBM>=250          FAIL
  semmni     (sem:4)  1 of 128 sets              (0%)    IBM>=1024         FAIL
System Settings
  file-max            1568 of 185426 files       (0%)    IBM>=524288       FAIL
  tcp_keepalive_time  7200 seconds                       IBM<=300          FAIL
Current User Limits (mqm)
  nofile       (-Hn)  4096 files                         IBM>=10240        FAIL
  nofile       (-Sn)  1024 files                         IBM>=10240        FAIL
```
则在(运行Docker Engine的服务器 )/etc/sysctl.conf中设置：
```
kernel.sem = 500 256000 250 1024
fs.file-max = 524288
net.ipv4.tcp_keepalive_time = 300
```
在(运行Docker Engine的服务器 )/etc/security/limits.conf中设置：
```
mqm    soft    nofile    10240
mqm    hard    nofile    10240
```

4. (在运行Docker Engine的服务器 ) 执行 sysctl -p 后启动一个新的容器，再次执行 su mqm -c "/opt/mqm/bin/mqconfig" 检查，全部通过即设置成功


##参考文章
1. Running MQSC commands from batch files from Administering IBM WebSphere MQ Version 7 Release 5
2. https://docs.docker.com/engine/admin/using_supervisord/
3. http://blog.csdn.net/gongxsh00/article/details/51182057


