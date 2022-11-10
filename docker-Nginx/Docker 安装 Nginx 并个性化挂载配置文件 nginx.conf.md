# Docker 安装 Nginx 并个性化挂载配置文件 nginx.conf

  

 

## 一、Docker pull 安装 Nginx 

###   1、查看docker仓库中的 nginx 命令

```
# 使用 docker search 命令搜索存放在 Docker Hub 中的镜像
docker search nginx1.2.3.
```

  以看到下图所示的信息：

​    

![Docker 安装 Nginx 并个性化挂载配置文件 nginx.conf_ui](https://s2.51cto.com/images/blog/202209/08141619_631988b363c641655.png?x-oss-process=image/watermark,size_16,text_QDUxQ1RP5Y2a5a6i,color_FFFFFF,t_30,g_se,x_10,y_10,shadow_20,type_ZmFuZ3poZW5naGVpdGk=/format,webp/resize,m_fixed,w_1184)

###   2、为选定需要pull到系统中的官方 Nginx 镜像

```
# docker pull nginx -------- nginx 为选定需要pull到系统中的官方 nginx 镜像

docker pull nginx1.2.3.
```

​    

![Docker 安装 Nginx 并个性化挂载配置文件 nginx.conf_docker_02](https://s2.51cto.com/images/blog/202209/08141619_631988b3833d135410.png?x-oss-process=image/watermark,size_16,text_QDUxQ1RP5Y2a5a6i,color_FFFFFF,t_30,g_se,x_10,y_10,shadow_20,type_ZmFuZ3poZW5naGVpdGk=/format,webp/resize,m_fixed,w_1184)

  整个pull过程需要花费一些时间，耐心等待。

  若见下图证明pull成功。 

​    

![Docker 安装 Nginx 并个性化挂载配置文件 nginx.conf_操作系统_03](https://s2.51cto.com/images/blog/202209/08141619_631988b3a004b57353.png?x-oss-process=image/watermark,size_16,text_QDUxQ1RP5Y2a5a6i,color_FFFFFF,t_30,g_se,x_10,y_10,shadow_20,type_ZmFuZ3poZW5naGVpdGk=/format,webp/resize,m_fixed,w_1184)

## 二、查看并启动Docker 镜像

###   1、列出已下载的镜像

```
# 使用 docker images 命令即可列出已下载的镜像

docker images1.2.3.
```

  执行命令后，可看到类似于如下的表格：

​    

![Docker 安装 Nginx 并个性化挂载配置文件 nginx.conf_运维_04](https://s2.51cto.com/images/blog/202209/08141619_631988b3bc5e58812.png?x-oss-process=image/watermark,size_16,text_QDUxQ1RP5Y2a5a6i,color_FFFFFF,t_30,g_se,x_10,y_10,shadow_20,type_ZmFuZ3poZW5naGVpdGk=/format,webp/resize,m_fixed,w_1184)

###   2、列出运行中的容器

```
# 使用 docker ps 命令即可列出运行中的容器
docker ps


# 使用 docker ps -a 命令即可列出所有（包括已停止的）的容器
docker ps -a
1.2.3.4.5.6.7.
```

  执行命令后，可看到类似于如下的表格：

​    

![Docker 安装 Nginx 并个性化挂载配置文件 nginx.conf_docker_05](https://s2.51cto.com/images/blog/202209/08141619_631988b3db2a640943.png?x-oss-process=image/watermark,size_16,text_QDUxQ1RP5Y2a5a6i,color_FFFFFF,t_30,g_se,x_10,y_10,shadow_20,type_ZmFuZ3poZW5naGVpdGk=/format,webp/resize,m_fixed,w_1184)

  可以发现，目前没有运行的 nginx 容器。故，接下来我们新建并启动一个 nginx 容器。

​    

![Docker 安装 Nginx 并个性化挂载配置文件 nginx.conf_ui_06](https://s2.51cto.com/images/blog/202209/08141620_631988b40301256480.png?x-oss-process=image/watermark,size_16,text_QDUxQ1RP5Y2a5a6i,color_FFFFFF,t_30,g_se,x_10,y_10,shadow_20,type_ZmFuZ3poZW5naGVpdGk=/format,webp/resize,m_fixed,w_1184)

## 三、启动容器，部署nginx并修改配置文件

###   1、启动跑个静态网页，测试下 nginx 容器

```
# 启动一个名为nginx81(名字自己根据需求起名字，一般见名知意即可) 的容器 
docker run --name nginx81 -d -p 80:80 -v /usr/docker/nginx/html:/usr/share/nginx/html nginx


# 默认容器对这个目录有可读写权限，可以通过指定ro，将权限改为只读（readonly）
# docker run --name my-nginx -d -p 80:80 -v /usr/docker/nginx/html:/usr/share/nginx/html:ro -d nginx1.2.3.4.5.6.
```

​    

![Docker 安装 Nginx 并个性化挂载配置文件 nginx.conf_ui_07](https://s2.51cto.com/images/blog/202209/08141620_631988b427d0410982.png?x-oss-process=image/watermark,size_16,text_QDUxQ1RP5Y2a5a6i,color_FFFFFF,t_30,g_se,x_10,y_10,shadow_20,type_ZmFuZ3poZW5naGVpdGk=/format,webp/resize,m_fixed,w_1184)

  访问 http://Docker宿主机IP:指定的Docker宿主机端口 ，可以访问说明

​    

![Docker 安装 Nginx 并个性化挂载配置文件 nginx.conf_nginx_08](https://s2.51cto.com/images/blog/202209/08141620_631988b44391f36257.png?x-oss-process=image/watermark,size_16,text_QDUxQ1RP5Y2a5a6i,color_FFFFFF,t_30,g_se,x_10,y_10,shadow_20,type_ZmFuZ3poZW5naGVpdGk=/format,webp/resize,m_fixed,w_1184)

###   2、部署nginx 项目并修改配置文件

  一般情况下docker启动时进行配置，只要把配置文件的目录挂载出来就可以，但是nginx却是先加载一个主配置文件nginx.conf，在nginx.conf里再加载conf.d目录下的子配置文件（一般最少一个default.conf文件）。 

```
# 普通的挂载方式
docker run --name mynginx2 --mount source=/var/www,target==/usr/share/nginx/html,readonly \
--mount source=/var/nginx/conf,target=/etc/nginx/conf,readonly -p 80:80 -d nginx1.2.3.
```

  docker 启动 nginx 加载自定义配置：

```
# 1. 第一个“-v”，是项目位置，把项目放到挂载到的目录下即可 
# 2. 第二个“-v”，是挂载的主配置文件"nginx.conf"，注意"nginx.conf"文件内有一行 
#    "include /etc/nginx/conf.d/*.conf;" ，
#    这个include指向了子配置文件的路径，此处注意include后所跟的路径一定不能出错
# 3. 第三个“-v”，把docker内子配置文件的路径也挂载了出来，注意要与 “2.” 中include指向路径一致
# 4. nginx.conf是挂载了一个文件（docker是不推荐这样用的），conf.d挂载的是一个目录

docker run \
  --name nginx81 \
  -d -p 81:80 \
  -v /usr/docker/nginx81/html:/usr/share/nginx/html \
  -v /etc/docker/nginx81/nginx.conf:/etc/nginx/nginx.conf:ro \
  -v /etc/docker/nginx81/conf.d:/etc/nginx/conf.d \
  nginx1.2.3.4.5.6.7.8.9.10.11.12.13.14.15.
```

  准备挂载的 nginx.conf :

```
user  nginx;
worker_processes  1;

error_log  /var/log/nginx/error.log warn;
pid        /var/run/nginx.pid;


events {
    worker_connections  1024;
}


http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    sendfile        on;
    #tcp_nopush     on;

    keepalive_timeout  65;

    #gzip  on;

    include /etc/nginx/conf.d/*.conf;
}1.2.3.4.5.6.7.8.9.10.11.12.13.14.15.16.17.18.19.20.21.22.23.24.25.26.27.28.29.30.31.32.
```

​    准备挂载的 default.conf :

```
server {
    listen       80;
    server_name  localhost;

    #charset koi8-r;
    #access_log  /var/log/nginx/host.access.log  main;

    location / {
        root   /usr/share/nginx/html;
        index  index.html index.htm;
    }

    location /api{
        proxy_pass http://192.168.1.1:9999/api;
        # access_log "logs/test.log";
    }
   


}1.2.3.4.5.6.7.8.9.10.11.12.13.14.15.16.17.18.19.20.
```

  

  上述的依然不够灵活，可以直接进入容器操作：

  1) 启动

```
# 启动一个名 nginx81 的 nginx 容器
docker run --name nginx81 -d -p 81:80 -v \
/usr/docker/nginx81/html/:/usr/share/nginx/html:ro -d nginx1.2.3.
```

 

```
# 添加日志记录启动
docker run --name nginx81 -d -p 81:80 -v /usr/docker/nginx81/html/:/usr/share/nginx/html:ro \
 -v /logs:/var/log/nginx -d nginx1.2.3.
```

​    

![Docker 安装 Nginx 并个性化挂载配置文件 nginx.conf_nginx_09](https://s2.51cto.com/images/blog/202209/08141620_631988b45ee8492247.png?x-oss-process=image/watermark,size_16,text_QDUxQ1RP5Y2a5a6i,color_FFFFFF,t_30,g_se,x_10,y_10,shadow_20,type_ZmFuZ3poZW5naGVpdGk=/format,webp/resize,m_fixed,w_1184)

  2）拷贝容器内的配置文件到本地，进行个性化配置等操作

```
docker cp nginx:/etc/nginx/nginx.conf /usr/docker/nginx81/nginx.conf
1.2.
```

  3）重新指定配置文件启动

```
docker run --name nginx81 -d -p 81:80 -v /usr/docker/nginx81/html:/usr/share/nginx/html:ro 
-v $PWD/logs:/var/log/nginx -v /usr/docker/nginx81/nginx.conf:/etc/nginx/nginx.conf:ro -d nginx1.2.3.
```

  4）进入容器

```
sudo docker exec -it d3a86da6fad1 /bin/bash

# 退出容器：Ctrl+P+Q1.2.3.4.
```

## 四、通过 Dockerfile 构建 Nginx 

相关链接

  · docker 官网 Nginx 安装文档: [ https://docs.docker.com/samples/library/nginx/#hosting-some-simple-static-content](https://docs.docker.com/samples/library/nginx/#hosting-some-simple-static-content)

 

· Nginx 官网文档：[ https://www.nginx.com/blog/deploying-nginx-nginx-plus-docker/](https://www.nginx.com/blog/deploying-nginx-nginx-plus-docker/) 