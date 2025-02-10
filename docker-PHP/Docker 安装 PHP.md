# Docker 安装 PHP

## 安装 PHP 镜像

### 方法一、docker pull php

查找 [Docker Hub](https://hub.docker.com/_/php?tab=tags) 上的 php 镜像:

[![img](https://www.runoob.com/wp-content/uploads/2016/06/0D34717D-1D07-4655-8559-A8661BCB4A3D.jpg)](https://www.runoob.com/wp-content/uploads/2016/06/0D34717D-1D07-4655-8559-A8661BCB4A3D.jpg)

可以通过 Sort by 查看其他版本的 php，默认是最新版本 **php:latest**。

此外，我们还可以用 docker search php 命令来查看可用版本：

```
runoob@runoob:~/php-fpm$ docker search php
NAME                      DESCRIPTION                                     STARS     OFFICIAL   AUTOMATED
php                       While designed for web development, the PH...   1232      [OK]       
richarvey/nginx-php-fpm   Container running Nginx + PHP-FPM capable ...   207                  [OK]
phpmyadmin/phpmyadmin     A web interface for MySQL and MariaDB.          123                  [OK]
eboraas/apache-php        PHP5 on Apache (with SSL support), built o...   69                   [OK]
php-zendserver            Zend Server - the integrated PHP applicati...   69        [OK]       
million12/nginx-php       Nginx + PHP-FPM 5.5, 5.6, 7.0 (NG), CentOS...   67                   [OK]
webdevops/php-nginx       Nginx with PHP-FPM                              39                   [OK]
webdevops/php-apache      Apache with PHP-FPM (based on webdevops/php)    14                   [OK]
phpunit/phpunit           PHPUnit is a programmer-oriented testing f...   14                   [OK]
tetraweb/php              PHP 5.3, 5.4, 5.5, 5.6, 7.0 for CI and run...   12                   [OK]
webdevops/php             PHP (FPM and CLI) service container             10                   [OK]
...
```

这里我们拉取官方的镜像,标签为5.6-fpm

```
runoob@runoob:~/php-fpm$ docker pull php:5.6-fpm
```

等待下载完成后，我们就可以在本地镜像列表里查到REPOSITORY为php,标签为5.6-fpm的镜像。

```
runoob@runoob:~/php-fpm$ docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
php                 5.6-fpm             025041cd3aa5        6 days ago          456.3 MB
```

------

## Nginx + PHP 部署

Nginx 部署可以查看：[Docker 安装 Nginx](https://www.runoob.com/docker/docker-install-nginx.html)，一些 Nginx 的配置参考这篇文章。

启动 PHP：

```
$ docker run --name  myphp-fpm -v ~/nginx/www:/www  -d php:5.6-fpm
```

命令说明：

- **--name myphp-fpm** : 将容器命名为 myphp-fpm。
- **-v ~/nginx/www:/www** : 将主机中项目的目录 www 挂载到容器的 /www

创建 ~/nginx/conf/conf.d 目录：

```
mkdir ~/nginx/conf/conf.d 
```

在该目录下添加 **~/nginx/conf/conf.d/runoob-test-php.conf** 文件，内容如下：

```
server {
    listen       80;
    server_name  localhost;

    location / {
        root   /usr/share/nginx/html;
        index  index.html index.htm index.php;
    }

    error_page   500 502 503 504  /50x.html;
    location = /50x.html {
        root   /usr/share/nginx/html;
    }

    location ~ \.php$ {
        fastcgi_pass   php:9000;
        fastcgi_index  index.php;
        fastcgi_param  SCRIPT_FILENAME  /www/$fastcgi_script_name;
        include        fastcgi_params;
    }
}
```

配置文件说明：

- **php:9000**: 表示 php-fpm 服务的 URL，下面我们会具体说明。
- **/www/**: 是 **myphp-fpm** 中 php 文件的存储路径，映射到本地的 ~/nginx/www 目录。

启动 nginx：

```
docker run --name runoob-php-nginx -p 8083:80 -d \
    -v ~/nginx/www:/usr/share/nginx/html:ro \
    -v ~/nginx/conf/conf.d:/etc/nginx/conf.d:ro \
    --link myphp-fpm:php \
    nginx
```

- **-p 8083:80**: 端口映射，把 **nginx** 中的 80 映射到本地的 8083 端口。
- **~/nginx/www**: 是本地 html 文件的存储目录，/usr/share/nginx/html 是容器内 html 文件的存储目录。
- **~/nginx/conf/conf.d**: 是本地 nginx 配置文件的存储目录，/etc/nginx/conf.d 是容器内 nginx 配置文件的存储目录。
- **--link myphp-fpm:php**: 把 **myphp-fpm** 的网络并入 ***nginx\***，并通过修改 **nginx** 的 /etc/hosts，把域名 **php** 映射成 127.0.0.1，让 nginx 通过 php:9000 访问 php-fpm。

接下来我们在 ~/nginx/www 目录下创建 index.php，代码如下：

```
<?php
echo phpinfo();
?>
```

浏览器打开 **http://127.0.0.1:8083/index.php**，显示如下：

![img](https://www.runoob.com/wp-content/uploads/2016/06/4CA3D4DE-3883-449C-B2F2-7C80D9A5B384.jpg)

 [Docker 安装 Node.js](https://www.runoob.com/docker/docker-install-node.html)

[Docker 安装 MySQL](https://www.runoob.com/docker/docker-install-mysql.html) 

## 1 篇笔记 写笔记

1. 

     pengqiangsheng

    294***2136@qq.com

    [ 参考地址](https://www.cnblogs.com/boundless-sky/p/7182410.html?utm_source=itdadao&utm_medium=referral)

   49

   **Docker 配置 nginx、php-fpm、mysql**

   **运行环境**

   ![img](https://www.runoob.com/wp-content/uploads/2018/08/1535703280-4104-20170715125030384-1014271798.png)

   **创建目录**

   ```
   mkdir -p /Users/sui/docker/nginx/conf.d && mkdir /Users/sui/www &&  cd /Users/sui/docker/nginx/conf.d && sudo touch default.conf
   ```

   **启动 php-fpm**

   解释执行 php 需要 php-fpm，先让它运行起来：

   ```
   docker run --name sui-php -d \
       -v /Users/sui/www:/var/www/html:ro \
       php:7.1-fpm
   ```

   **--name sui-php** 是容器的名字。

   **/Users/sui/www** 是本地 php 文件的存储目录，/var/www/html 是容器内 php 文件的存储目录，ro 表示只读。

   **编辑 nginx 配置文件**

   配置文件位置：/Users/sui/docker/nginx/conf.d/default.conf。

   ```
   server {
       listen       80;
       server_name  localhost;
   
       location / {
           root   /usr/share/nginx/html;
           index  index.html index.htm;
       }
   
       error_page   500 502 503 504  /50x.html;
       location = /50x.html {
           root   /usr/share/nginx/html;
       }
   
       location ~ \.php$ {
           fastcgi_pass   php:9000;
           fastcgi_index  index.php;
           fastcgi_param  SCRIPT_FILENAME  /var/www/html/$fastcgi_script_name;
           include        fastcgi_params;
       }
   }
   ```

   说明：

   - php:9000 表示 php-fpm 服务的访问路径，下文还会提及。
   - /var/www/html 是 sui***-php\*** 中 php 文件的存储路径，经 docker 映射，变成本地路径 /Users/sui/www（可以再看一眼 php-fpm 启动命令

   启动 nginx:

   ```
   docker run --name sui-nginx -p 80:80 -d \
       -v /Users/sui/www:/usr/share/nginx/html:ro \
       -v /Users/sui/docker/nginx/conf.d:/etc/nginx/conf.d:ro \
       --link sui-php:php \
       nginx
   ```

   -  -p 80:80 用于添加端口映射，把 ***sui-nginx\*** 中的 80 端口暴露出来。
   -  /Users/sui/www 是本地 html 文件的存储目录，/usr/share/nginx/html 是容器内 html 文件的存储目录。
   -  /Users/sui/docker/nginx/conf.d 是本地 nginx 配置文件的存储目录，/etc/nginx/conf.d 是容器内 nginx 配置文件的存储目录。
   -  --link sui-php:php 把 ***sui-php\*** 的网络并入 ***sui-nginx\***，并通过修改 ***sui-nginx\*** 的 /etc/hosts，把域名 ***php\*** 映射成 127.0.0.1，让 nginx 通过 php:9000 访问 php-fpm。

   ![img](https://www.runoob.com/wp-content/uploads/2018/08/1036583-20170715131816337-108470072.png)

   **测试结果**

   在 /Users/sui/www 下放两个文件：index.html index.php

   ![img](https://www.runoob.com/wp-content/uploads/2018/08/1036583-20170715132145759-1925306861.png)

   **mysql 和 phpmyadmin**

   mysql 服务器

   ```
   sudo mkdir -p /Users/sui/docker/mysql/data /Users/sui/docker/mysql/logs /Users/sui/docker/mysql/conf
   ```

   -  data 目录将映射为 mysql 容器配置的数据文件存放路径
   -  logs 目录将映射为 mysql 容器的日志目录
   -  conf 目录里的配置文件将映射为 mysql 容器的配置文件

   ```
   docker run -p 3307:3306 --name sui-mysql -v /Users/sui/docker/mysql/conf:/etc/mysql -v /Users/sui/docker/mysql/logs:/logs -v /Users/sui/docker/mysql/data:/mysql_data -e MYSQL_ROOT_PASSWORD=123456 -d --link sui-php mysql
   ```

   进入mysql客户端:

   ```
   docker run -it --link sui-mysql:mysql --rm mysql sh -c 'exec mysql -h"$MYSQL_PORT_3306_TCP_ADDR" -P"$MYSQL_PORT_3306_TCP_PORT" -uroot -p"$MYSQL_ENV_MYSQL_ROOT_PASSWORD"'
   ```

   注意：我本地 3306 端口有 mysql, 所以这里用3307端口。

   ![img](https://www.runoob.com/wp-content/uploads/2018/08/1036583-20170715143730290-1337674791.png)

   **phpmyadmin**

   ```
   docker run --name sui-myadmin -d --link sui-mysql:db -p 8080:80 phpmyadmin/phpmyadmin
   ```

   ![img](https://www.runoob.com/wp-content/uploads/2018/08/1036583-20170715144105462-703943679.png)

   大功告成:

   ![img](https://www.runoob.com/wp-content/uploads/2018/08/1535703283-3466-20170715144243790-455471563.png)

   [pengqiangsheng](https://www.runoob.com/note/34619)  pengqiangsheng 294***2136@qq.com [ 参考地址](https://www.cnblogs.com/boundless-sky/p/7182410.html?utm_source=itdadao&utm_medium=referral)4年前 (2018-08-31)