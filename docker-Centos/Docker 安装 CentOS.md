# Docker 安装 CentOS

CentOS（Community Enterprise Operating System）是 Linux 发行版之一，它是来自于 Red Hat Enterprise Linux(RHEL) 依照开放源代码规定发布的源代码所编译而成。由于出自同样的源代码，因此有些要求高度稳定性的服务器以 CentOS 替代商业版的 Red Hat Enterprise Linux 使用。

### 1、查看可用的 CentOS 版本

访问 CentOS 镜像库地址：https://hub.docker.com/_/centos?tab=tags&page=1。

可以通过 Sort by 查看其他版本的 CentOS 。默认是最新版本 centos:latest 。

[![img](https://www.runoob.com/wp-content/uploads/2019/11/docker-centos1.png)](https://www.runoob.com/wp-content/uploads/2019/11/docker-centos1.png)

你也可以在下拉列表中找到其他你想要的版本：

[![img](https://www.runoob.com/wp-content/uploads/2019/11/docker-centos2.png)](https://www.runoob.com/wp-content/uploads/2019/11/docker-centos2.png)

### 2、拉取指定版本的 CentOS 镜像，这里我们安装指定版本为例(centos7):

```
$ docker pull centos:centos7
```

[![img](https://www.runoob.com/wp-content/uploads/2019/11/docker-centos3.png)](https://www.runoob.com/wp-content/uploads/2019/11/docker-centos3.png)

### 3、查看本地镜像

使用以下命令来查看是否已安装了 centos7：

```
$ docker images
```

[![img](https://www.runoob.com/wp-content/uploads/2019/11/docker-centos4.png)](https://www.runoob.com/wp-content/uploads/2019/11/docker-centos4.png)

### 4、运行容器，并且可以通过 exec 命令进入 CentOS 容器。

```
$ docker run -itd --name centos-test centos:centos7
```

[![img](https://www.runoob.com/wp-content/uploads/2019/11/dcoker-centos6.png)](https://www.runoob.com/wp-content/uploads/2019/11/dcoker-centos6.png)

### 5、安装成功

最后我们可以通过 **docker ps** 命令查看容器的运行信息：

[![img](https://www.runoob.com/wp-content/uploads/2019/11/docker-centos7.png)](https://www.runoob.com/wp-content/uploads/2019/11/docker-centos7.png)