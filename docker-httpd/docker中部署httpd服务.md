docker中部署httpd服务
1. 生成container中软件源文件
mkdir /root/docker  
#事先将web的内容放在/root/docker/www/目录，web首页是index.php
cat >/root/docker/local.repo <<END
[BaseOS]
name=Base
enabled=1
gpgcheck=0
baseurl=https://mirrors.aliyun.com/centos-vault/8.3.2011/BaseOS/x86_64/os/
[AppStream]
name=AppStream
enabled=1
gpgcheck=0
baseurl=https://mirrors.aliyun.com/centos-vault/8.3.2011/AppStream/x86_64/os/
[EPEL]
name=epel
enabled=1
gpgcheck=0
baseurl=https://mirrors.tuna.tsinghua.edu.cn/epel/8/Everything/x86_64/
END
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
2. 生成dockerfile
cat > /root/docker/dockerfile <<END
FROM centos
MAINTAINER mack
RUN rm /etc/yum.repos.d/*
COPY local.repo /etc/yum.repos.d/
RUN yum install wget -y
RUN yum install vim -y
RUN yum install tar vim -y
RUN yum install httpd -y
RUN sed -i '/DirectoryIndex index.html/cDirectoryIndex index.php' /etc/httpd/conf/httpd.conf
EXPOSE 80
CMD ["httpd","-DFOREGROUND"]
END
1
2
3
4
5
6
7
8
9
10
11
12
13
3. build镜像
cd /root/docker
docker build -t centos/nginx:mack .
docker images
REPOSITORY     TAG       IMAGE ID       CREATED          SIZE
centos/nginx   mack      5f3c527c40be   35 minutes ago   421MB
centos         latest    5d0da3dc9764   9 months ago     231MB
1
2
3
4
5
6
4. run 容器
方法一docker运行后httpd直接运行
方法一：
docker run -dit --name nginxmack -p 80:80 -v /root/docker/www/:/var/www/html/  centos/nginx:mack

方法二docker运行后需要使用systemctl start httpd启动httpd服务
方法二：
docker run -dit --name nginxmack -p 80:80 -v /root/docker/www/:/var/www/html/ --privileged=true centos/nginx:mack /sbin/

#注意
容器内使用systemctl 命令时出现（System has not been booted with systemd as init system (PID 1). Can't operat....信息。

解决方案：/sbin/init
加上/sbin/init和--privileged=true可以解决容器内使用systemctl 命令时报错问题
--privileged=true一定要加上的
1
2
3
4
5
6
7
8
9
10
11
12
13
14
5. 进入容器，开启httpd服务
这一步在第四步采用方法二时执行，否则不执行
docker exec -it nginxmack /bin/bash
在容器内执行如下命令
systemctl start httpd
1
2
3
4
6. 查看web内容
在浏览器输入宿主机IP:80 ,即可查看web内容。
————————————————
版权声明：本文为CSDN博主「mackzhaohan」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/weixin_49888547/article/details/125490436