Docker-study
============

**学习网站：**  
Docker Get Started：[https://docs.docker.com/windows/](https://docs.docker.com/windows/)  
Docker Docs：[https://docs.docker.com/](https://docs.docker.com/)  
Docker 中文指南：[http://docker.widuu.com/](http://docker.widuu.com/)  
Docker 从入门到实践：[https://yeasy.gitbooks.io/docker_practice/content/](https://yeasy.gitbooks.io/docker_practice/content/)  


**镜像：**  
1，Docker Hub：[https://hub.docker.com/](https://hub.docker.com/)


**DockerToolbox：**  
Docker官方2015年7月份发布了DockerToolbox（[Docker toolbox github](https://github.com/docker/toolbox/)），有Windows、Mac版本，同Boot2Docker一样，这两个工具都可以在Windows、Mac上运行管理Docker。  
**注意：**  
1，如果安装DockerToolbox前已安装过git，则安装时可不勾选git，安装后新增桌面图标Docker Quickstart Terminal，需要修改此图标的目标指向中的git地址后此图标方才可用；  


**命令：**  
***1.1，帮助***  
1.1.1，docker --help  
1.1.2，docker command --help   
1.1.3，docker version  
***1.2，列出本地镜像***  
1.2.1，docker images  
1.2.2，docker images -q  
1.2.3，docker images -a  
***1.3，运行镜像***  
1.3.1，docker run image  
1.3.2，docker run -i -t image  
1.3.3，docker run -d image  
1.3.4，docker run -idt image  
1.3.5，docker run -d -P image  
1.3.6，docker run -d -p hostPort:containerPort image  
1.3.7，docker run --name container_name -d image  
1.3.8，docker run -d image command  
***1.4，进入容器、容器信息***  
1.4.1，docker attach container  
1.4.2，docker exec -it container command  
1.4.3，docker exec -d container command  
1.4.4，docker rename old_container_name new_container_name  
1.4.5，docker inspect container  
***1.5，构建镜像***  
1.5.1，docker build -t image_name:tag Dockerfile_path_folder  
1.5.2，docker tag image_id image_name:tag  
1.5.3，docker history image  
1.5.4，docker inspect image  
1.5.5，docker commit -a author -m "message" --pause=false container image  
1.5.6，docker diff container  
***1.6，删除镜像***  
1.6.1，docker rmi image_id  
1.6.2，docker rmi -f image_id  
1.6.3，docker rmi $(docker images -q -f "dangling=true")  
1.6.4，docker rmi $(docker images | grep "^<none>" | awk "{print $3}")  
***1.7，镜像仓库***  
1.7.1，docker search image_name  
1.7.2，docker pull image_name:tag  
1.7.3，docker push image_name:tag  
***1.8，存出、载入镜像***  
1.8.1，docker save -o save_image.tar image  
&emsp;&emsp;&emsp;&nbsp;docker save --output="save_image.tar" image  
&emsp;&emsp;&emsp;&nbsp;docker save image > save_image.tar  
1.8.2，docker load -i load_image.tar  
&emsp;&emsp;&emsp;&nbsp;docker load --input="load_image.tar"  
&emsp;&emsp;&emsp;&nbsp;docker load < load_image.tar  
***1.9，列出运行中容器***  
1.9.1，docker ps  
1.9.2，docker ps -a -q  
***1.10，启动、停止、重启、创建容器***  
1.10.1，docker start container  
1.10.2，docker stop container  
1.10.3，docker restart container   
1.10.4，docker create [options] image [comman] [arg...]  
***1.11，容器运行相关***  
1.11.1，docker stats container  
1.11.2，docker top container  
1.11.3，docker port container  
1.11.4，docker kill container  
1.11.5，docker pause container  
1.11.6，docker unpause container  
***1.12，查看容器输出日志***  
1.12.1，docker logs -f -t container  
1.12.2，docker logs -f -t --tail=100 --since=2016-04-16 container  
1.12.3，docker logs -f -f --tail=f --since=1460692128 container  
***1.13，删除容器***  
1.13.1，docker rm stoped_container  
1.13.2，docker rm $(docker ps -a -q)  
***1.14，导出、导入容器***  
1.14.1，docker export -o container.tar container  
&emsp;&emsp;&emsp;&emsp;docker export --output="container.tar" container  
&emsp;&emsp;&emsp;&emsp;docker export container > container.tar  
1.14.2，docker import container.tar  
&emsp;&emsp;&emsp;&emsp;docker import container_tar_url  
&emsp;&emsp;&emsp;&emsp;docker import --change "ENV DEBUG true" container.tar  
***1.14，数据卷***  
1.14.1，docker volume ls  
1.14.2，docker volume inspect volume_name  
1.14.3，docker volume create --name=volume_name  
1.14.4，docker volume rm volume_name  
***1.15，数据卷容器*** [docker docs run](https://docs.docker.com/engine/reference/commandline/run/)  
1.15.1，docker run -d -v absolute_container_dest_path[:options] --name=volume_container_name image  
1.15.2，docker run -d -v volume_name:absolute_container_dest_path[:options] --name=volume_container_name image  
1.15.3，docker run -d -v absolute_local_path:absolute_container_dest_path[:options] --name=volume_container_name image  
1.15.4，options  are [rw|ro], [z|Z], [[r]shared|[r]slave|[r]private], and [nocopy]  
***1.16，数据卷容器挂载*** [Docker从入门到实践-数据卷容器](https://yeasy.gitbooks.io/docker_practice/content/data_management/container.html)  
1.16.1，docker run -d --volumes-from volume_container_name --name container_name image  
1.16.2，可以使用volumes-from级联挂载，可以使用多个--volumes-from volume_container_name参数来指定从多个数据卷容器挂载不同的数据卷，使用--volumes-from参数所挂载数据卷的容器自己并不需要保持在运行状态，一个数据卷容器可以被多个容器挂载  
1.16.3，[Docker从入门到实践-利用数据卷容器来备份、恢复、迁移数据卷](https://yeasy.gitbooks.io/docker_practice/content/data_management/management.html)  
***1.17，数据拷贝***  
1.17.1，docker cp container:src_path local_dest_path  
1.17.2，docker cp local_src_path container:dest_path  


**Dockerfile指令：**[Docker从入门到实践-Dockerfile指令](https://yeasy.gitbooks.io/docker_practice/content/dockerfile/instructions.html)

 命令 | 说明
 --- | ---
 # | 注释
 FROM image | 第一条指令，一个镜像只能一条
 MAINTAINER name | 维护者信息
 ENV key value | 环境变量，后续命令及运行时皆可用，可以有多条
 RUN command | building image时运行的命令，可以有多条
 CMD command | container运行时运行的命令，只能一条
 EXPOSE port [port...] | 对外暴露的端口
 COPY src dest | 复制本机src（Dockerfile相对路径）到容器中的dest，复制本地目录推荐使用COPY
 ADD src dest | 除了用于COPY指令的功能，src还可以是一个URL，或者是tar（自动解压为目录）
 ENTRYPOINT command | 配置容器启动后执行的命令，只能一条
 VOLUME volume | 挂载
 USER daemon | 指定运行容器时的用户名或 UID，后续的 RUN 也会使用指定用户
 WORKDIR path | 工作路径
 ONBUILD command | 配置当所创建的镜像作为其它新创建镜像的基础镜像时，所执行的操作指令
&nbsp;  
**约定：**  
1，docker命令执行对象image可由image_name:tag(tag为latest时简写image_name)或image_id标识；  
2，docker命令执行对象container可由container_id或container_name标识；  
3，docker run的镜像如果本地不存在，会自动尝试从远程仓库下载；  
4，docker命令的option比如save、export命令，-o file.tar同-out file.tar同-out="file.tar"等价；

**常用命令：**  
1，使用attach进入容器，如何退出而不停止容器；  
&emsp;&nbsp;&nbsp;Ctrl + P + Q  
2，  

**FAQ：**  
1，docker tag给一个镜像(根据镜像id)打标签，会生成一个新tag，同时旧有的tag仍然存在，同一个镜像打了不同的标签，怎样删除多余的标签？  
&emsp;&nbsp;&nbsp;解决：docker rmi image_name:tag  
&emsp;&nbsp;&nbsp;参考：[How to tag and remove tag on docker](http://blog.tmtk.net/post/2013-09-16-how_to_remove_tag_on_docker/)  
2，ubuntu容器apt-get安装软件提示：Could not resolve 'archive.ubuntu.com'，即容器内连不上外网，如何解决？  
&emsp;&nbsp;&nbsp;尝试：Windows下重启Docker Quickstart Terminal，删除中间状态的容器及镜像  
&emsp;&nbsp;&nbsp;其他：http://stackoverflow.com/questions/34141438/docker-build-failing-with-could-not-resolve-archive-ubuntu-com  
&emsp;&nbsp;&nbsp;&emsp;&emsp;&emsp;http://dockone.io/question/946  
&emsp;&nbsp;&nbsp;&emsp;&emsp;&emsp;https://forums.docker.com/t/could-not-resolve-archive-ubuntu-com-14-04-1-lts/639/3  
&emsp;&nbsp;&nbsp;&emsp;&emsp;&emsp;http://stackoverflow.com/questions/24991136/docker-build-could-not-resolve-archive-ubuntu-com-apt-get-fails-to-install-a  
3，windows docker build警告：SECURITY WARNING: You are building a Docker image from Windows against a non-Windows Docker host. All files and directories added to build context will have '-r wxr-xr-x' permissions. It is recommended to double check and reset permissions for sensitive files and directories.  
&emsp;&nbsp;&nbsp;解释：[docker github issues](https://github.com/docker/docker/issues/20397)  
4，ubuntu 14.04.3 LTS版本安装ssh，使用root用户进行ssh远程登录，提示被拒绝，是何原因？  
&emsp;&nbsp;&nbsp;解释：vi /etc/ssh/sshd_config，找到PermitRootLogin *，需要将其修改为PermitRootLogin yes，重启ssh服务/etc/init.d/ssh stop，/etc/init.d/ssh start