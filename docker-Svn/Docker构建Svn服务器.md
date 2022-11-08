# Docker构建Svn服务器

 



## 概述

```
   本文提供Docker方式安装Svn服务器，有以下构建版本：1. garethflowers/svn-server，2. elleflorio/svn-server，3 krisdavison版本。第1种不支持http协议，需要配置才支持，第2种直接支持http协议。推荐使用第1种。
```

> **linux安装svn**
>
> 参考：https://jingyan.baidu.com/article/9158e000027674a2541228c4.html
>
> https://blog.csdn.net/u011200190/article/details/81776982
>
> https://blog.csdn.net/han_dongwei/article/details/8269639
>
> https://www.cnblogs.com/liuxianan/p/linux_install_svn_server.html

## 1. garethflowers/svn-server版本

**Docker下载Svn server**

\#docker pull garethflowers/svn-server

**根据镜像生成容器**

```
docker run --name svn-server-gf \    --detach \    --volume /usr/docker/svn/data:/var/opt/svn \    --publish 3690:3690 \    garethflowers/svn-server
```

**创建新项目仓库**

```
docker exec -it svn-server-gf svnadmin create proj1
```

- **备份项目仓库**

  docker exec -i svn-server-gf svnadmin dump proj1 > /backup/svn_bk20190506/proj_20190506.dump

- **从备份svn库文件中还原至新仓库**

  docker exec -i svn-server-gf svnadmin load proj1 < /backup/svn_bk20190506/proj_20190506.dump

**开启外网的svn端口**

安全端口开放**3690**访问

**SVN客户端测试连接**

**svn://47.xx.xx.xx:proj1，可以看到下图，svn客户端已经可以工作了。**

![watermark_type_ZmFuZ3poZW5naGVpdGk_shadow_10_text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3lhbl9kaw_size_16_color_FFFFFF_t_70](https://image.dandelioncloud.cn/images/20220204/0670560f1f4b419f86c7e271183ff73e.png)

**修改项目仓库的配置**

\#cd /usr/docker/svn/data/proj1

![20190506235844691.png](https://image.dandelioncloud.cn/images/20220204/e9d0e18750794b06a0b2cf81dcfa91b1.png)

修改 svnserve.conf

```
[general]anon-access = none             # 匿名用户不可读写，也可设置为只读 readauth-access = write            # 授权用户可写password-db = passwd           # 密码文件路径，相对于当前目录authz-db = authz               # 访问控制文件realm = /var/opt/svn/repo1     # 认证命名空间，会在认证提示界面显示，并作为凭证缓存的关键字，可以写仓库名称，#注意这里一定要写容器内的路径，不然连接会失败
```

配置账号与密码，修改 passwd，格式为“账号 = 密码”

```
[users]# harry = harryssecret# sally = sallyssecreteric = 123456
```

配置权限，修改 authz

```
[groups]owner = eric, user1[/]             # / 表示所有仓库eric = rw       # 用户 eric 在所有仓库拥有读写权限# 表示以下用户在仓库 repo1 的所有目录有相应权限[repo1:/]           user1 = rw@owner = rw         # 表示 owner 组下的用户拥有读写权限
```

说明，r 表示读，w 表示写。没有设置的用户默认为无权限。
注意：更改svnserve.conf，authz和passwd文件时不需要重启。

**配置SVN支持http访问**

## 2. elleflorio/svn-server版本

**Docker下载Svn server**

\#docker pull elleflorio/svn-server

**根据镜像生成容器**

```
docker run -d \    --name svn-server-ef \    -p 21080:80 \    -p 3690:3960 \    --volume /usr/docker/svn/data:/home/svn \    --volume /usr/docker/svn/apache/passwd:/etc/subversion/passwd \    elleflorio/svn-server
```

**创建 http 访问账号**

```
docker exec -t svn-server-ef htpasswd -b /etc/subversion/passwd <username> <password>
```

此账号和密码被写入容器中的 HTTP 认证文件（/etc/subversion/passwd），且密码是加密的。实践经验表明，既然用 http 协议访问只能查看，那么创建一个公共的账号，供大家使用即可。也可创建与 svn 认证文件中一样的账号和密码。

**创建新项目仓库**

```
docker exec -it svn-server-ef svnadmin create proj1
```

**修改项目仓库的配置**

## **同【1.】**

> 参考：https://www.joycc.cn/p/240.html

**导入项目**

创建一个新的项目仓库后，windows开发环境中，可以先执行svn checkout svn://ip/proj1，把新建的空项目下载下来，然后把新项目复制到这个目录，再svn右键菜单add目录，上传到svn上，再commit，这样就把整个目录上传到svn服务器了。

注意：新建项目要配置好权限，否则无法上传导入提交。见【**修改项目仓库的配置**】

## 问题记录

- svn 客户端操作比较版本时，报错“”Unreadable path encountered; access denied“”

解决：svn服务器的配置svnserve.conf设置anon-access=none;

> https://blog.csdn.net/hellboy0621/article/details/82802340