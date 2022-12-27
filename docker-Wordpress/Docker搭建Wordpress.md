Docker搭建一个Wordpress博客





要使用docker搭建一个自己的博客，必须有一个自己的linux服务器，可以使用阿里云服务器，或者虚拟机都行。如果不会虚拟机的话可以百度一下，很多教程。





搭建环境：





系统：centos7





技术：Docker





首先安装Docker：





1、对yum进行更新





yum update -y





2、安装Docker





```
yum install docker -y
--安装完成后进行查看
yum list | grep docker
--验证安装(查看版本号)
docker -v
```





3、因为Dokcer默认的下载地址是国外的，速度慢，所以改成国内的镜像





```
vi /etc/docker/daemon.json

在这个json文件中加入：
```





```bash
{  "registry-mirrors": ["https://6xacs6l2.mirror.aliyuncs.com"]}
```



![img](https://pic.rmb.bdstatic.com/bjh/down/51e409b11aa51c150090697429a953ed.gif)



4、启动Docker服务





```
systemctl start docker.service
```





5、为Docker创建普通用户，避免使用root





```
groupadd dockeruseradd -g docker docker
```





WordPress安装：





1、DOcker拉取WP最新镜像





```
docker pull wordpress:latest
```





2、Docker啦取Mysql数据库镜像





```
docker pull mysql:5.6
```





3、使用Mysql镜像运行容器：





```
docker run -d --privileged=true --name OLDMysql -v /data/mysql:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=123456 -p 33306:3306 mysql:5.6
```





参数说明：





- -p: 端口映射，33306表示宿主，3306表示容器中的端口。 这里表示将宿主机的33306映射给镜像的3306.
- -e: 环境变量， 环境变量和具体的Docker容器制作时设置有关，这里表示设置镜像中MySQL的root 密码时123456
- --name: 容器名称
- --privileged=true: CentOS系统下的安全Selinux禁止了一些安全权限，导致MySQL容器在运行时会因为权限不足而报错，所以需要增加该选项
- -v: 指定数据卷，也就是将我们MySQL容器的`/var/lib/mysql`映射到宿主机的`/data/mysql`





运行后使用 docker ps -a 查看运行状况，如果出现错误，使用 docker stop 容器名 停止运行，然后用 docker rm 容器名 删除容器。如图这里的容器名是 OLDMysql。





之后使用上面的命令，去掉 -d 选项重新运行排查错误。





4、运行WP





```
docker run -d --name OLDwp -e WORDPRESS_DB_HOST=mysql -e WORDPRESS_DB_USER=root -e WORDPRESS_DB_PASSWORD=123456 -e WORDPRESS_DB_NAME=myword -p 1080:80 --link OLDMysql:mysql wordpress
```





- -e WORDPRESS_DB_HOST : 链接的docker的MySQL的IP地址和端口，一般设置成mysql表示用默认的设置
- -e WORDPRESS_DB_USER : 以什么用户使用MySQL，默认是root
- -e WORDPRESS_DB_PASSWORD : 这设置MySQL的登录用户密码，由于上一项是默认的root，所以这一项和之前的"MYSQL_ROOT_PASSWORD“要相同。
- -e WORDPRESS_DB_NAME: 数据库的表名，如果不写这一个配置，默认为”wordpress"
- 注意 --link 链接到MySQL容器的名称
- 



![img](https://pics7.baidu.com/feed/30adcbef76094b36ceb9cfdd0a26f5d08c109dcf.png@f_auto?token=8d6c0bcac6304f122e3143c406e811fa)



备注：容器的80端口映射给主机的1080，不需要用到root权限，但CentOS默认的防火墙禁止了大于1000后的所有端口，所以要开启这个端口





```
firewall-cmd --zone=public --add-port=8000/tcp --permanentfirewall-cmd --reload
```





5、设置wp



![img](https://pics7.baidu.com/feed/14ce36d3d539b60023a2223448babc23c75cb73c.jpeg@f_auto?token=db1cb0d74f3f22282c256cd24e48dbd9)

![img](https://pics7.baidu.com/feed/241f95cad1c8a786fc8b2d3dcde3403471cf5057.png@f_auto?token=ed6d5b2913989c87f31fa1670a573c7a)

![img](https://pics0.baidu.com/feed/4a36acaf2edda3cc4e998380ae03b008203f9200.png@f_auto?token=048868b6d10ee5dd2e213725a1752005)