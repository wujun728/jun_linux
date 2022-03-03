# [使用Docker安装Jenkins](https://www.cnblogs.com/stulzq/p/8627360.html)

> 博主不再推荐以Docker的方式安装Jenkins，请查看最新版 https://www.cnblogs.com/stulzq/p/9291237.html

# Jenkins

Jenkins是一个开源软件项目，是基于Java开发的一种持续集成工具，用于监控持续重复的工作，旨在提供一个开放易用的软件平台，使软件的持续集成变成可能。

# 环境准备

腾讯云

硬件配置：2核4G 1M带宽。50G硬盘。

系统配置：CentOS 7.2

# Docker安装

请移步查看：[CentOS 7 安装 Docker](http://www.cnblogs.com/stulzq/p/7743073.html)

# 安装Jenkins

首先不直接从Docker Store上直接Pull Jenkins 的 Image 文件，因为待会需要进行dotnet core 的 Docker自动部署，需要对宿主机上的Docker进行直接操作，那么需要挂载 Docker 给 Jenkins Image，所以现在需要自己动手编写 Dockerfile 构建自定义的Jenkins。

1.新建Dockerfile

```shell
touch Dockerfile
vim Dockerfile
```

2.加入以下内容：

```shell
FROM jenkins

USER root
#清除了基础镜像设置的源，切换成腾讯云的jessie源
#使用非腾讯云环境的需要将 tencentyun 改为 aliyun
RUN echo '' > /etc/apt/sources.list.d/jessie-backports.list \
  && echo "deb http://mirrors.tencentyun.com/debian jessie main contrib non-free" > /etc/apt/sources.list \
  && echo "deb http://mirrors.tencentyun.com/debian jessie-updates main contrib non-free" >> /etc/apt/sources.list \
  && echo "deb http://mirrors.tencentyun.com/debian-security jessie/updates main contrib non-free" >> /etc/apt/sources.list
#更新源并安装缺少的包
RUN apt-get update && apt-get install -y libltdl7 && apt-get update

ARG dockerGid=999

RUN echo "docker:x:${dockerGid}:jenkins" >> /etc/group 

# 安装 docker-compose 因为等下构建环境的需要
RUN curl -L https://github.com/docker/compose/releases/download/1.16.1/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose

RUN chmod +x /usr/local/bin/docker-compose
```

3.构建image

```shell
docker build . -t auto-jenkins
```

![img](https://images2018.cnblogs.com/blog/668104/201803/668104-20180322222116474-1640057742.png)

> 等待时间可能有点长，请耐心等待。

出现以上 Successfully 内容代表安装Jenkins成功

4.在启动Jenkins时，需要先创建一个Jenkins的配置目录，并且挂载到docker 里的Jenkins目录下

```shell
mkdir -p /var/jenkins_home
```

5.修改目录权限（很重要！）

```shell
chown -R 1000 /var/jenkins_home
```

6.运行 Jenkins

```shell
docker run --name jenkins -p 8080:8080 -p 50000:50000 \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v $(which docker):/bin/docker \
    -v /var/jenkins_home:/var/jenkins_home \
    -d auto-jenkins
```

出现一串很长的字符串以后，我们的jenkins已经成功启动：

![img](https://images2018.cnblogs.com/blog/668104/201803/668104-20180322222533517-840973024.png)

通过命令`docker ps`查看运行的镜像：

![img](https://images2018.cnblogs.com/blog/668104/201803/668104-20180322222602116-233245974.png)

# 配置Jenkins

访问`http://<你的ip>:8080`访问Jenkins。如果无法访问请检查系统防火墙、云的安全组设置。

![img](https://images2018.cnblogs.com/blog/668104/201803/668104-20180322223342353-910104143.png)

可以看到需要我们输入密码。

首选进入容器：

```shell
docker exec -it jenkins /bin/bash
```

然后查看密码：

```shell
cat /var/jenkins_home/secrets/initialAdminPassword
```

![img](https://images2018.cnblogs.com/blog/668104/201803/668104-20180322223542177-40967692.png)

复制输出的内容，粘贴到Administrator password，输入 exit 退出容器，此时进行下一步你会看到此界面，点击 Install suggested plugins

![img](https://images2018.cnblogs.com/blog/668104/201803/668104-20180322223626654-1063652757.png)

等待安装完毕：

![img](https://images2018.cnblogs.com/blog/668104/201803/668104-20180322223725671-1549853481.png)

> 如果有插件安装失败，不用紧张，安装结束之后会有"Retry”重试选项，点击重试即可。

漫长的等待之后到了下一步：

![img](https://images2018.cnblogs.com/blog/668104/201803/668104-20180322225250069-660652719.png)

根据表单填写信息之后就结束了！

进入主界面后如果看到右上角有错误的提示信息，那么请把你的Jenkins升级到最新版本，然后更新一下插件。

如果更新之后出现协议警告：

![img](https://images2018.cnblogs.com/blog/668104/201803/668104-20180322230742481-949979217.png)

我们可以直接点击警告中的Protocol Configuration，或者点击系统管理—>全局安全配置—>Agents—>Agent protocols

![img](https://images2018.cnblogs.com/blog/668104/201803/668104-20180322231118355-911681095.png)

将那两项取消勾选即可。

## 配置加速器

【系统管理】-> 【插件管理】-> 【高级】-> 【升级站点】

更换地址：http://mirror.xmission.com/jenkins/updates/current/update-center.json

![img](https://images2018.cnblogs.com/blog/668104/201805/668104-20180505102755229-1403253159.png)

至此Jenkins的配置就结束了！