# Introduction

Deploy lnmp(Linux, Nginx, MySQL, PHP7) using docker.

I want to share my ideas and designs about Web-Deploying using Docker with you.

### Architecture

![architecture][1]

The whole app is divided into three Containers:

1. Nginx is running in `Nginx` Container, which handles requests and makes responses.
2. PHP or PHP-FPM is put in `PHP-FPM` Container, it retrieves php scripts from host, interprets, executes then responses to Nginx. If necessary, it will connect to `MySQL` as well.
3. MySQL lies in `MySQL` Container, 

Our app scripts are located on host, you can edit files directly without rebuilding/restarting whole images/containers.

### Build and Run

At first, you should have had [Docker](https://docs.docker.com) and [Docker Compose](https://docs.docker.com/compose) installed.

Without building images one by one, you can make use of `docker-compose` and simply issue:

    $ sudo docker-compose up

For more operations to containers, please refer to:

    $ sudo docker-compose --help

Check out your https://\<docker-host\> and have fun :beer:

###注：

代码放到 /data/www目录下，
nginx的配置放到 /data/nginx/conf.d/ 目录下，参考defult.conf
直接运行start.sh就好啦。要想开启ssl模式，把default.conf第3到第8行注释去掉方可开启localhhost的https了，其它类似。

### Contributors

Micooz <micooz@hotmail.com>

sndnvaps <sndnvaps@gmail.com>

### License

MIT

  [1]: architecture.png

