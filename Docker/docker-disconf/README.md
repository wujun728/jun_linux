#Docker-Disconf
Docker-Disconf是本人学习Docker后，尝试使用Docker解决Disconf打包和运行问题的作品。
Disconf是分布式配置管理平台(Distributed Configuration Management Platform)的简称，使用该平台提供的Web界面，可以统一管理多个应用，多个环境的所有配置。Disconf是一个GitHub上的开源项目，在[https://github.com/knightliao/disconf](https://github.com/knightliao/disconf)可以找到相关的源码和文档。Disconf-web是Disconf的服务器端，提供了用于管理分布式配置的Web界面。
## 准备
Docker-Disconf所使用的Dockerfile和配置样例可以从[https://git.oschina.net/gongxusheng/docker-disconf.git](https://git.oschina.net/gongxusheng/docker-disconf.git)下载。以下说明文档中的操作假设用户已经成功安装了[Docker](https://docs.docker.com/engine/installation/linux/centos/)和[Docker-compose](https://docs.docker.com/compose/install/)，并且已经把DockerDisconf目录下的文件夹上传到了/home/ubuntu目录。如果解压在了其它的目录。需要调整部分配置文件和命令。
## 使用Docker打包Disconf
在disconf-build目录中执行以下命令构建Docker镜像，该镜像的用于Disconf-web的打包
```
docker build -t yourimgs/disconf-build .
```
在disconf-build目录执行以下的命令，打包Disconf-war
```
docker run -v ${PWD}/working:/home/work/dsp/disconf-rd/working \
    -v ${PWD}/config:/home/work/dsp/disconf-rd/online-resources \
    --name disconf-build yourimgs/disconf-build
```
如果修改了properties文件，可以通过再次启动disconf-build容器来打包
```
docker start disconf-build
```
## 使用Docker Compose部署运行Disconf
如下图所示，Disconf的部署使用到了Nginx, Tomcat, MySQL, Redis和ZooKeeper：

![Disconf部署架构](http://git.oschina.net/uploads/images/2016/0127/125722_8de982ee_411046.png "Disconf部署架构")
在disconf-compose目录中执行
```
docker-compose up
```
所有容器启动正常以后，就可以通过[http://yourhost:8081](http://)访问Disconf-web服务了。
###Disconf客户端的配置
首先应配置disconf.properties指向[http://yourhost:8081](http://)。Disconf的客户端需要访问zookeeper，会使用/DockerDisconf/disconf-build/config/zoo.properties中的配置。为了统一配置，Docker-Disconf的配置使用了disconf-zoo:2181，因此在客户端所在的主机上需要配置hosts文件，将主机名disconf-zoo映射到Docker所在的服务器ip。
## (非Docker Compose方式)部署运行Disconf
【说明】本章是早期版本，操作步骤较多。推荐使用前面章节介绍的Docker Compose部署运行。

1) 启动一个Redis服务，执行
```
docker run --name disconf-redis -d redis:3.0
```
2) 启动MySQL服务，在disconf-mysql目录执行
```
docker run --name disconf-mysql -e MYSQL_ROOT_PASSWORD=passw0rd -v ${PWD}/files/sql:/docker-entrypoint-initdb.d \
    -v ${PWD}/data:/var/lib/mysql -d mysql:5.7
```
3) 创建一个ZooKeeper服务，在disconf-zoo目录下执行
```
docker build -t yourimgs/disconf-zoo .
docker run --name disconf-zoo -p 2181:2181 -d yourimgs/disconf-zoo
```
4) 创建应用服务器镜像，在disconf-app目录下执行
```
docker build -t yourimgs/disconf-app .
docker run -d --link disconf-mysql:disconf-mysql --link disconf-redis:disconf-redis --link disconf-zoo:disconf-zoo \
    -v /home/ubuntu/disconf-build/working/war:/home/work/dsp/disconf-rd/war --name disconf-app yourimgs/disconf-app
```
5) 在disconf-nginx目录下执行
```
docker run --name disconf-nginx -v ${PWD}/nginx.conf:/etc/nginx/nginx.conf:ro \
    -v /home/ubuntu/disconf-build/working/war/html:/home/work/dsp/disconf-rd/war/html:ro \
    -v ${PWD}/logs:/home/work/var/logs/disconf -d -p 8081:8081 --link disconf-app:disconf-app nginx:1.9
```
所有容器启动正常以后，就可以通过[http://yourhost:8081](http://)访问Disconf-web服务了。Disconf的客户端需要访问zookeeper，所以在配置Disconf的客户端时请配置hosts文件，将主机名disconf-zoo映射到Docker所在的服务器上。