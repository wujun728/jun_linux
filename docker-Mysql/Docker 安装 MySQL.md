# Docker 安装 MySQL

MySQL 是世界上最受欢迎的开源数据库。凭借其可靠性、易用性和性能，MySQL 已成为 Web 应用程序的数据库优先选择。

### 1、查看可用的 MySQL 版本

访问 MySQL 镜像库地址：https://hub.docker.com/_/mysql?tab=tags 。

可以通过 Sort by 查看其他版本的 MySQL，默认是最新版本 **mysql:latest** 。

[![img](https://www.runoob.com/wp-content/uploads/2016/06/docker-mysql1.png)](https://www.runoob.com/wp-content/uploads/2016/06/docker-mysql1.png)

你也可以在下拉列表中找到其他你想要的版本：

[![img](https://www.runoob.com/wp-content/uploads/2016/06/docker-mysql2.png)](https://www.runoob.com/wp-content/uploads/2016/06/docker-mysql2.png)

此外，我们还可以用 **docker search mysql** 命令来查看可用版本：

```
$ docker search mysql
NAME                     DESCRIPTION                                     STARS     OFFICIAL   AUTOMATED
mysql                    MySQL is a widely used, open-source relati...   2529      [OK]       
mysql/mysql-server       Optimized MySQL Server Docker images. Crea...   161                  [OK]
centurylink/mysql        Image containing mysql. Optimized to be li...   45                   [OK]
sameersbn/mysql                                                          36                   [OK]
google/mysql             MySQL server for Google Compute Engine          16                   [OK]
appcontainers/mysql      Centos/Debian Based Customizable MySQL Con...   8                    [OK]
marvambass/mysql         MySQL Server based on Ubuntu 14.04              6                    [OK]
drupaldocker/mysql       MySQL for Drupal                                2                    [OK]
azukiapp/mysql           Docker image to run MySQL by Azuki - http:...   2                    [OK]
...
```

### 2、拉取 MySQL 镜像

这里我们拉取官方的最新版本的镜像：

```
$ docker pull mysql:latest
```

[![img](https://www.runoob.com/wp-content/uploads/2016/06/docker-mysql3.png)](https://www.runoob.com/wp-content/uploads/2016/06/docker-mysql3.png)

### 3、查看本地镜像

使用以下命令来查看是否已安装了 mysql：

```
$ docker images
```

[![img](https://www.runoob.com/wp-content/uploads/2016/06/docker-mysql6.png)](https://www.runoob.com/wp-content/uploads/2016/06/docker-mysql6.png)

在上图中可以看到我们已经安装了最新版本（latest）的 mysql 镜像。

### 4、运行容器

安装完成后，我们可以使用以下命令来运行 mysql 容器：

```
$ docker run -itd --name mysql-test -p 3306:3306 -e MYSQL_ROOT_PASSWORD=123456 mysql
```

参数说明：

- **-p 3306:3306** ：映射容器服务的 3306 端口到宿主机的 3306 端口，外部主机可以直接通过 **宿主机ip:3306** 访问到 MySQL 的服务。
- **MYSQL_ROOT_PASSWORD=123456**：设置 MySQL 服务 root 用户的密码。

[![img](https://www.runoob.com/wp-content/uploads/2016/06/docker-mysql4.png)](https://www.runoob.com/wp-content/uploads/2016/06/docker-mysql4.png)

### 5、安装成功

通过 **docker ps** 命令查看是否安装成功：

[![img](https://www.runoob.com/wp-content/uploads/2016/06/docker-mysql5.png)](https://www.runoob.com/wp-content/uploads/2016/06/docker-mysql5.png)

本机可以通过 root 和密码 123456 访问 MySQL 服务。

[![img](https://www.runoob.com/wp-content/uploads/2016/06/docker-mysql7.png)](https://www.runoob.com/wp-content/uploads/2016/06/docker-mysql7.png)

 [Docker 安装 PHP](https://www.runoob.com/docker/docker-install-php.html)

[Docker 安装 Tomcat](https://www.runoob.com/docker/docker-install-tomcat.html) 

## 2 篇笔记 写笔记

1. 

     Brian

    153***2799@qq.com

   191

   最新官方MySQL(5.7.19)的docker镜像在创建时映射的配置文件目录有所不同，在此记录并分享给大家：

   官方原文：

   The MySQL startup configuration is specified in the file `/etc/mysql/my.cnf`, and that file in turn includes any files found in the `/etc/mysql/conf.d` directory that end with `.cnf`. Settings in files in this directory will augment and/or override settings in `/etc/mysql/my.cnf`. If you want to use a customized MySQL configuration, you can create your alternative configuration file in a directory on the host machine and then mount that directory location as `/etc/mysql/conf.d` inside the `mysql` container.

   大概意思是说：

   MySQL(5.7.19)的默认配置文件是 /etc/mysql/my.cnf 文件。如果想要自定义配置，建议向 /etc/mysql/conf.d 目录中创建 .cnf 文件。新建的文件可以任意起名，只要保证后缀名是 cnf 即可。新建的文件中的配置项可以覆盖 /etc/mysql/my.cnf 中的配置项。

   具体操作：

   首先需要创建将要映射到容器中的目录以及.cnf文件，然后再创建容器

   ```
   # pwd
   /opt
   # mkdir -p docker_v/mysql/conf
   # cd docker_v/mysql/conf
   # touch my.cnf
   # docker run -p 3306:3306 --name mysql -v /opt/docker_v/mysql/conf:/etc/mysql/conf.d -e MYSQL_ROOT_PASSWORD=123456 -d imageID
   4ec4f56455ea2d6d7251a05b7f308e314051fdad2c26bf3d0f27a9b0c0a71414
   ```

   命令说明：

   - **-p 3306:3306：**将容器的3306端口映射到主机的3306端口
   - **-v /opt/docker_v/mysql/conf:/etc/mysql/conf.d：**将主机/opt/docker_v/mysql/conf目录挂载到容器的/etc/mysql/conf.d
   - **-e MYSQL_ROOT_PASSWORD=123456：**初始化root用户的密码
   - **-d:** 后台运行容器，并返回容器ID
   - **imageID:** mysql镜像ID

   **查看容器运行情况**

   ```
   # docker ps
   CONTAINER ID IMAGE          COMMAND          ... PORTS                    NAMES
   4ec4f56455ea c73c7527c03a  "docker-entrypoint.sh" ... 0.0.0.0:3306->3306/tcp   mysql
   ```

   [Brian](javascript:;)  Brian 153***2799@qq.com5年前 (2017-09-08)

2. 

     liaozesong

    lia***song@yeah.net

    [ 参考地址](http://note.youdao.com/groupshare/?token=AE9F46916C444460B4B4F7F591727871&gid=80144203)

   340

   **docker 安装 mysql 8 版本**

   ```
   # docker 中下载 mysql
   docker pull mysql
   
   #启动
   docker run --name mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=Lzslov123! -d mysql
   
   #进入容器
   docker exec -it mysql bash
   
   #登录mysql
   mysql -u root -p
   ALTER USER 'root'@'localhost' IDENTIFIED BY 'Lzslov123!';
   
   #添加远程登录用户
   CREATE USER 'liaozesong'@'%' IDENTIFIED WITH mysql_native_password BY 'Lzslov123!';
   GRANT ALL PRIVILEGES ON *.* TO 'liaozesong'@'%';
   ```

   [liaozesong](https://www.runoob.com/note/33381)  liaozesong lia***song@yeah.net [ 参考地址](http://note.youdao.com/groupshare/?token=AE9F46916C444460B4B4F7F591727871&gid=80144203)4年前 (2018-07-30)