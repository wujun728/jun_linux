### docker-lnp 是一个封装了 Nginx+php7-fpm 以及多数常用的 php 扩展的 Dockerfile 仓库，旨在快速构建基于Docker的LNMP环境。

> 特性： 

- 1，自定义 Nginx, PHP-FPM, PHP 相关配置文件，完全定制
- 2，Docker 内采用 supervisor 管理 Nginx，FPM 进程，方便内部重启调试，统一管理
- 3，通过设置环境变量 SERVER_NAME 可自定义镜像中 nginx 虚拟机的 server_name
- 4，通过设置环境变量 DOCUMENT_ROOT 可自定义镜像中 nginx 虚拟机的 root
- 5，直接在 Dockerfile 中通过 RUN 命令执行 shell 命令来控制系统设置
- 6，通过 docker-compose 控制整个容器环境，可深度定制
- 7，Nginx采用官方stable-alpine稳定版，容器体积小且稳定
- 8，PHP版本跟随清华镜像源，升级更方便
- 9，代码简单，通俗易懂，流程清晰

> 版本说明：

- PHP: 7.1.17
- Nginx: 官方稳定镜像
- Docker-compose: 3

> 使用方式：

**推荐方式: 通过 docker-compose 直接拉取远端镜像运行**

```bash
docker-compose up
```
[远端镜像地址](https://hub.docker.com/r/komazhang/lnp/)

**step1 构建镜像**
```bash
cd <docker-lnp dir>

sudo docker-compose build
```
这里可能得需要一段时间，因为需要下载一些需要的包


**step2 查看镜像**
```bash
sudo docker images
```
如果没有错的话，上面的命令会显示出来刚刚构建好的镜像


**step3 运行镜像**
```bash
sudo docker-compose up -d
```
- -d 指定后台运行，也可以省略，则容器运行在前台


**step4 测试**
```bash
sudo docker ps
sudo docker inspect <container_id>
```
通过上面的命令找到映射IP，然后在本地通过IP或配置hosts文件来访问，注意代码位置需要通过Dockerfile中的卷映射出来


**step5 调试，如果需要的话**
```bash
sudo docker ps
sudo docker exec -it <container_id> bash
```
容器内部的Alpine linux系统提供一个bash环境，可进入到系统内部方便调试环境，重启则可通过 supervisorctl 


> 说明

- 该仓库的Dockerfile仅封装了Nginx和FPM，不包含Mysql
- 建议通过 docker-compose 来定义容器环境，详细请参考 docker-compose.yml 文件
- 该仓库提供的 docker-compose.yml 中定义了容器链接 Mysql 的方式，如有需要请参考


> 最后：
欢迎提建议指正，不定时更新中。。。。。By Koma > <komazhang@foxmail.com>
