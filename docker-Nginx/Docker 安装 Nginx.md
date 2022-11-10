# Docker 安装 Nginx

Nginx 是一个高性能的 HTTP 和反向代理 web 服务器，同时也提供了 IMAP/POP3/SMTP 服务 。

### 1、查看可用的 Nginx 版本

访问 Nginx 镜像库地址： https://hub.docker.com/_/nginx?tab=tags。

可以通过 Sort by 查看其他版本的 Nginx，默认是最新版本 **nginx:latest**。

[![img](https://www.runoob.com/wp-content/uploads/2016/06/docker-nginx1.png)](https://www.runoob.com/wp-content/uploads/2016/06/docker-nginx1.png)

你也可以在下拉列表中找到其他你想要的版本：

[![img](https://www.runoob.com/wp-content/uploads/2016/06/docker-nginx2.png)](https://www.runoob.com/wp-content/uploads/2016/06/docker-nginx2.png)

此外，我们还可以用 **docker search nginx** 命令来查看可用版本：

```
$ docker search nginx
NAME                      DESCRIPTION                                     STARS     OFFICIAL   AUTOMATED
nginx                     Official build of Nginx.                        3260      [OK]       
jwilder/nginx-proxy       Automated Nginx reverse proxy for docker c...   674                  [OK]
richarvey/nginx-php-fpm   Container running Nginx + PHP-FPM capable ...   207                  [OK]
million12/nginx-php       Nginx + PHP-FPM 5.5, 5.6, 7.0 (NG), CentOS...   67                   [OK]
maxexcloo/nginx-php       Docker framework container with Nginx and ...   57                   [OK]
...
```

### 2、取最新版的 Nginx 镜像

这里我们拉取官方的最新版本的镜像：

```
$ docker pull nginx:latest
docker pull nginx:1.23.2
```

[![img](https://www.runoob.com/wp-content/uploads/2016/06/docker-nginx3.png)](https://www.runoob.com/wp-content/uploads/2016/06/docker-nginx3.png)

### 3、查看本地镜像

使用以下命令来查看是否已安装了 nginx：

```
$ docker images
```

[![img](https://www.runoob.com/wp-content/uploads/2016/06/docker-nginx4.png)](https://www.runoob.com/wp-content/uploads/2016/06/docker-nginx4.png)

在上图中可以看到我们已经安装了最新版本（latest）的 nginx 镜像。

### 4、运行容器

安装完成后，我们可以使用以下命令来运行 nginx 容器：

```
$ docker run --name nginx-test -p 8080:80 -d nginx
docker run --name nginx-proxy777 -p 80:80 -d nginx:1.23.2
docker run --name nginx-proxy -p 80:80 -v /home/nginx/nginx.conf:/etc/nginx/nginx.conf:rw -d nginx:1.23.2
```

参数说明：

- **--name nginx-test**：容器名称。
- **-p 8080:80**： 端口进行映射，将本地 8080 端口映射到容器内部的 80 端口。
- **-d nginx**： 设置容器在在后台一直运行。

[![img](https://www.runoob.com/wp-content/uploads/2016/06/docker-nginx5.png)](https://www.runoob.com/wp-content/uploads/2016/06/docker-nginx5.png)

### 5、安装成功

最后我们可以通过浏览器可以直接访问 8080 端口的 nginx 服务：

[![img](https://www.runoob.com/wp-content/uploads/2016/06/docker-nginx6.png)](https://www.runoob.com/wp-content/uploads/2016/06/docker-nginx6.png)




===========================================

  docker run \
  --name nginx80 \
   -p 80:80  -it -d \
  -v /home/nginx/html:/usr/share/nginx/html \
  -v /home/nginx/conf/nginx.conf:/etc/nginx/nginx.conf \
  -v /home/nginx/conf/conf.d:/etc/nginx/conf.d:ro \
  -v /home/nginx/log:/var/log/nginx \
  nginx:1.23.2



===========================================
 

Docker安装Nginx挂载宿主机文件及nginx.conf文件配置



1.docker 启动nginx
从启动nginx命令说起：
docker run --restart=always --name=nginx -it -p 80:80 -v /opt/nginx/conf/conf.d:/etc/nginx/conf.d -v /opt/nginx/conf/nginx.conf:/etc/nginx/nginx.conf -v /opt/nginx/log:/var/log/nginx -v /opt/nginx/html:/usr/share/nginx/html -d nginx:latest

===========================================



===========================================



命令	描述
-v /opt/nginx/conf/conf.d:/etc/nginx/conf.d	挂载该路径下的nginx配置文件
-v /opt/nginx/conf/nginx.conf:/etc/nginx/nginx.conf	挂载nginx.conf配置文件
-v /opt/nginx/log:/var/log/nginx	挂载nginx日志文件
-v /opt/nginx/html:/usr/share/nginx/html	挂载nginx内容



#nginx也可以是容器id
docker cp nginx:/etc/nginx/conf.d/default.conf ./ ###这里是将容器内文件复制到本地当前目录
docker cp ./default.conf nginx:/etc/nginx/conf.d/ ###这里是将本地当前目录的default.conf复制到容器内指定目录

2.访问nginx主页
因为映射的80端口，所以在浏览器访问服务器IP，但是网页显示404.NotFound
查看/opt/nginx/log目录下error.log日志文件，显示
“/etc/nginx/html/index.html” is not found (2: No such file or directory)


进入运行的nginx容器：docker exec -it 容器ID /bin/bash
在容器内进入/etc/nginx目录下,创建html文件夹：mkdir html
在html目录下创建index.html文件：touch index.html
index.html内容如下：

<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
html { color-scheme: light dark; }
body { width: 35em; margin: 0 auto;
font-family: Tahoma, Verdana, Arial, sans-serif; }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, the nginx web server is successfully installed and
working. Further configuration is required.</p>

<p>For online documentation and support please refer to
<a href="http://nginx.org/">nginx.org</a>.<br/>
Commercial support is available at
<a href="http://nginx.com/">nginx.com</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>

再次在浏览器访问服务器IP，网页正常显示

3.nginx的配置
在/opt/nginx/conf下新建配置文件nginx.conf，文件内容如下

 见附件nginx.conf



*include ./conf.d/*.conf指包含/opt/nginx/conf/conf.d/目录下所有的配置文件
所以在/opt/nginx/conf/conf.d目录下新建适用于自己服务的conf配置文件
需要注意的是配置文件中不要用 l o c a l h o s t ，而是用服务器 I P 代替 l o c a l h o s t \color{#FF0000}{需要注意的是配置文件中不要用localhost，而是用服务器IP代替localhost}需要注意的是配置文件中不要用localhost，而是用服务器IP代替localhost