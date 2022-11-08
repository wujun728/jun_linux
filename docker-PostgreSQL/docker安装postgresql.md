docker安装postgresql


1.查询postgresql镜像 docker search postgres

NAME                  --镜像名称

DESCRIPTION    --镜像描述

STARS                 --标星数

OFFICIAL             --官方的

AUTOMATED      -- 自动化



        圈红的地方为postgres官方镜像文件！

2.拉去镜像文件 docker pull postgres:14.2



我这里拉去的是官方14.2版本的镜像文件，也可以拉去最新的版本，按需拉取镜像文件，新手最好拉取官方镜像（ps网上的文档较多，出现问题可以招到解决办法）

3.镜像文件是否成功拉取 docker images



 4.创建挂载文件夹

cd /                

cd data

mkdir postgresql  



在data目录创建挂载文件夹（我这是在正式服务器，所有镜像的挂载目录都在data目录，方便后期维护）

 6.启动docker 镜像

docker run --name postgres \
    --restart=always \
    -e POSTGRES_PASSWORD=password \
    -p 5432:5432 \
    -v /data/postgresql:/var/lib/postgresql/data \
    -d postgres:14.2 



 run: 创建并运行一个容器；

 --restart=always 表示容器退出时,docker会总是自动重启这个容器；
–name: 指定创建的容器的名字；
-e POSTGRES_PASSWORD=password: 设置环境变量，指定数据库的登录口令为password；
-p 5432:5432: 端口映射将容器的5432端口映射到外部机器的5432端口；

-v  /data/postgresql:/var/lib/postgresql/data   将运行镜像的/var/lib/postgresql/data目录挂载到宿主机/data/postgresql目录
-d postgres:11.4: 指定使用postgres:11.4作为镜像。

7.查看启动日志 docker logs postgres



8.查看运行的容器，看看镜像是否启动成功 docker ps 



 9.本地连接测试数据库是否连接成功



安装成功（ps:输入命令时候端口映射出现了问题，后面通过直接更改配置文件，更改了端口映射关系）

10.数据库连接失败可能的原因：

        1.容器启动失败，端口冲突
    
        解决方案：更改容器映射端口
    
        2.服务器端口没有开放
    
       解决方案： 在服务器安全组，配置出入站规则
    
        还有其他原因，暂时没有遇到

以上就是使用docker安装postgresql的全过程，如有问题，请及时与人联系，欢迎大家指正！（ps：后续有

 nignx，Redis，fastdfs，nexus，portainter，kuboard，kibana，gitlab，rabbitmq

会慢慢的写出来，有兴趣的，评论区交流，互相提高技术）

 
