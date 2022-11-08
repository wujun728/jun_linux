
###使用须知
> 将服务分别以组建的形式提供服务, 避免其中一个改变影响整个镜像的问题发生. 多个镜像通过docker-compose来进行配置.
> 使使用过程更简单快捷.

> docker镜像可跨平台使用, 所以能使环境部署成本大大降低.

> 使用此镜像需要安装 docker, docker-compose.

> 默认目录为: ~/opt/www/default
> 优化了代码结构, 相关镜像文件放在resource中, docker-compose放在stack中, 扩展以支持多个docker-compose的结构.

```
/alidata
```




### 构建与重新加载
```
docker-compose build
docker-compose up -d
```

### MAC/Windows 使用教程

> 在MAC/Windows上使用时, 都需要安装VirtualBox, 安装过程比较繁琐
> docker提供 [Docker Toolbox](https://www.docker.com/products/docker-toolbox) 来快捷安装docker支持, 也可以通过[灵雀云下载此工具](http://get.alauda.cn/toolbox)

> 要通过`Docker Quickstart Terminal` 打开的终端进行相关操作...

```
Run the Docker Quickstart Terminal app
Run docker-machine restart default
Run eval $(docker-machine env default)
```


### 镜像加速
##### 阿里云的镜像加速方案

```
# 系统要求 CentOS 7 以上，Docker 1.9 以上。

sudo cp -n /lib/systemd/system/docker.service /etc/systemd/system/docker.service
sudo sed -i "s|ExecStart=/usr/bin/docker daemon|ExecStart=/usr/bin/docker daemon --registry-mirror=https://ng889j52.mirror.aliyuncs.com|g" /etc/systemd/system/docker.service
sudo systemctl daemon-reload
sudo service docker restart
```
