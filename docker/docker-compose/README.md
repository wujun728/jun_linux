#### 基于Docker搭建的lnmp开发环境

> 包含组件：nginx-1.15.0、MySQL-5.7.22、PHP-7.1.19-fpm、Redis-4.0.10
> 
> Nginx、PHP、Redis使用的是Alpine-3.7
> 另外，由于搭建此环境时，有用到FFmpeg，所以PHP的镜像中，默认集成了FFmpeg；
> 
> 各个容器的配置信息都在conf目录下相应的目录中，可以根据需要进行调整；


-----


#### 重要提示

>在PHP项目中，MySQL和Redis的配置路径及端口号，不再是`localhost`和`127.0.0.1`，而是`docker-compose.yml`中设定的service的名称。在此`docker-compose.yml`中，分别是`mysql`和`redis`。
>
>MySQL的账号、密码、自动创建的数据库也都在`docker-compose.yml`中：
> 
> ```
> environment:
>         - MYSQL_ROOT_PASSWORD=root
>         - MYSQL_DATABASE=lumen
> ```
> 
> * 另：`docker.cmd`文件中记录的是搭建环境和平时使用时，经常用到的docker相关的命令；

-----

#### 更新记录

> - 2018-08-29 加入了根据自身需求构建镜像`image`的临时文件`Dockerfile`
> - 2018-08-28 `LNMP On Docker`开发过程中，在 Windows 或 macOS 上响应速度很慢。在此次更新中进行了优化，即在`volumes`映射时，加入了`:cached`，若为`linux`则无需此项；参考文档：
> 	1. [How to get a better disk performance in Docker for Mac](https://medium.com/@TomKeur/how-get-better-disk-performance-in-docker-for-mac-2ba1244b5b70)
> 	2. [Frequently asked questions (FAQ)](https://docs.docker.com/docker-for-mac/faqs/#qcow2-or-raw)

<br />
<br />
<br />
<br />
