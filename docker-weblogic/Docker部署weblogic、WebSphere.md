# Docker部署weblogic、WebSphere



# 在Centos6.8安装Docker 

*1.安装依赖库：yum install -y epel-release*

*2.安装Docker：yum install -y docker-io*

*3.安装后的配置文件：/etc/sysconfig/docker*

*4.启动docker后台服务service docker start*

*5.*  docker version 验证

## *centos7安装docker*

https://docs.docker.com/engine/install/centos/

https://www.docker-cn.com

# 镜像命令

docker images :列出本机上的镜像信息

docker search [镜像名]:在docker hub上搜索镜像

docker pull [镜像名]:拉下来镜像

docker rmi [镜像名]:删除镜像

docker run -it [镜像]:启动并进入容器（输入命令的命令行终端）

docker run -d [镜像]:启动后不进入容器（没有前台，起了直接关闭）

docker run -p [镜像]:指定端口映射，格式为：主机(宿主)端口:容器端口

docker ps （-l/-n）:当前正在运行的 （上个运行的/上几个运行的）

exit / ctrl+p+q ： 退出/不停止退出容器

docker start [容器名/id] ：启动容器

docker stop [容器名/id] ： 停止容器

docker kill [容器名/id] ： 强制关闭容器

docker logs --tail [容器id] ： 查看容器日志

docker top [容器id] ： 查看容器内的进程

docker attach [容器id] ： 进入容器内的命令行终端

docker run -it -p 8888:8080 tomcat:

# docker的镜像

是一种分层、轻量级高性能的文件系统，支持对文件系统的修改作为一次提交来一层层的叠加，最终形成一个整体。（联合文件系统）

镜像查询地址：https://registry.hub.docker.com 

如果镜像下载速度很慢，可以添加配置，修改文件 **/etc/docker/daemon.json** ( 如果文件不存在，你可以直接创建它 )，添加阿里云的配置：https://7p93y96e.mirror.aliyuncs.com如下

**{**

  "registry-mirrors": [

​    "https://registry.docker-cn.com"，

​    “https://7p93y96e.mirror.aliyuncs.com" 

  ]

}

# docker部署weblogic

1、拉取镜像：docker pull ismaleiva90/weblogic12:latest

2、启动镜像：docker run -d -p 7001:7001 -p 7002:7002 ismaleiva90/weblogic12

3、登陆weblogic：

http://IP:7001/console

IP为部署的服务IP，端口号为启动镜像时配置的7001（密码为weblogic welcome1）。



![img](https://upload-images.jianshu.io/upload_images/15514965-4e1f9fa044e35c79.png?imageMogr2/auto-orient/strip|imageView2/2/w/1200/format/webp)

登录页面

4、进入主页，开始部署



![img](https://upload-images.jianshu.io/upload_images/15514965-ba983b1a5f4a255d.png?imageMogr2/auto-orient/strip|imageView2/2/w/1200/format/webp)

5、上载项目war包



![img](https://upload-images.jianshu.io/upload_images/15514965-5ca3dc252b01b212.png?imageMogr2/auto-orient/strip|imageView2/2/w/1200/format/webp)

6、选择需要上载的本地war包

![img](https://upload-images.jianshu.io/upload_images/15514965-d1fc7460a2abb2dd.png?imageMogr2/auto-orient/strip|imageView2/2/w/1200/format/webp)

选择需上传的war



![img](https://upload-images.jianshu.io/upload_images/15514965-adf40542c203ddf7.png?imageMogr2/auto-orient/strip|imageView2/2/w/970/format/webp)

点击下一步



![img](https://upload-images.jianshu.io/upload_images/15514965-40ed0bd1971c05e3.png?imageMogr2/auto-orient/strip|imageView2/2/w/606/format/webp)

继续下一步



![img](https://upload-images.jianshu.io/upload_images/15514965-5850b700177bec39.png?imageMogr2/auto-orient/strip|imageView2/2/w/742/format/webp)

下一步



![img](https://upload-images.jianshu.io/upload_images/15514965-cfb49cb13e48fa4d.png?imageMogr2/auto-orient/strip|imageView2/2/w/903/format/webp)

点击完成



![img](https://upload-images.jianshu.io/upload_images/15514965-2f30da986d670d1b.png?imageMogr2/auto-orient/strip|imageView2/2/w/1200/format/webp)

点击 激活更改



![img](https://upload-images.jianshu.io/upload_images/15514965-75bb2b700ecf63b7.png?imageMogr2/auto-orient/strip|imageView2/2/w/814/format/webp)

配置系统环境



![img](https://upload-images.jianshu.io/upload_images/15514965-add64f4ad2364164.png?imageMogr2/auto-orient/strip|imageView2/2/w/1200/format/webp)

进入AdminServer



![img](https://upload-images.jianshu.io/upload_images/15514965-36cb4e9d4ca04a13.png?imageMogr2/auto-orient/strip|imageView2/2/w/1200/format/webp)

点击协议、HTTP



![img](https://upload-images.jianshu.io/upload_images/15514965-7fcafe72b5b1786f.png?imageMogr2/auto-orient/strip|imageView2/2/w/889/format/webp)

保存HTTP协议的配置



![img](https://upload-images.jianshu.io/upload_images/15514965-9e63fd8eeb9b8964.png?imageMogr2/auto-orient/strip|imageView2/2/w/1200/format/webp)

启动项目



![img](https://upload-images.jianshu.io/upload_images/15514965-0df389862d72a83b.png?imageMogr2/auto-orient/strip|imageView2/2/w/495/format/webp)

最后一步

部署后，可以根据之前的配置，访问项目：http://172.18.0.1:7001/helloworld

# docker启动websphere

1、拉取镜像：docker pull ibmcom/websphere-traditional:9.0.0.10

2、docker run -p 9043:9043 -p 9443:9443 -d ibmcom/websphere-traditional:9.0.0.10 #后台运行该镜像生成的容器

3、查询websphere的密码：

docker ps查看部署的镜像，websphere的name为gracious_einstein

根据name进入容器docker exec -it gracious_einstein bash

获取其密码，在tmp/PASSWORD，记录密码zFz4qJAe

![img](https://upload-images.jianshu.io/upload_images/15514965-0ed6eb4258e95cb9.png?imageMogr2/auto-orient/strip|imageView2/2/w/1200/format/webp)

获取密码

4、访问websphere

https://IP:9043/ibm/console/login.do?action=secure

9043为此前运行时配置的端口号

![img](https://upload-images.jianshu.io/upload_images/15514965-b485a489cab1047f.png?imageMogr2/auto-orient/strip|imageView2/2/w/1200/format/webp)

输入之前保存的密码

5、部署项目



![img](https://upload-images.jianshu.io/upload_images/15514965-47949be6c0455719.png?imageMogr2/auto-orient/strip|imageView2/2/w/1200/format/webp)

WebSphere 企业应用程序



![img](https://upload-images.jianshu.io/upload_images/15514965-62e4a2822b8ecafe.png?imageMogr2/auto-orient/strip|imageView2/2/w/1200/format/webp)

点击安装



![img](https://upload-images.jianshu.io/upload_images/15514965-345b0098b70accf8.png?imageMogr2/auto-orient/strip|imageView2/2/w/968/format/webp)

选择war包后next



![img](https://upload-images.jianshu.io/upload_images/15514965-d98c090849eda3df.png?imageMogr2/auto-orient/strip|imageView2/2/w/1200/format/webp)

下一步



![img](https://upload-images.jianshu.io/upload_images/15514965-4d6532858f73a844.png?imageMogr2/auto-orient/strip|imageView2/2/w/1200/format/webp)

下一步



![img](https://upload-images.jianshu.io/upload_images/15514965-e525f7023cd720fa.png?imageMogr2/auto-orient/strip|imageView2/2/w/1200/format/webp)

一直下一步，finish后，点击保存