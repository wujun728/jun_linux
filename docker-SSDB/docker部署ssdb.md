docker部署ssdb


1、下载centos镜像，版本按需下载

docker pull centos:7.7.1908

2、查看镜像

docker images

3、用镜像创建容器

注意端口映射主机6381对应容器ssdb默认端口8888，/bin/bash设置的是启动命令，可以直接设置为ssdb启动命令

docker run -p 6381:8888 --name ssdbServer -dit centos:7.7.1908 /bin/bash

创建完成使用docker ps 

4、

启动：docker start ssdbServer

进入：docker exec -it ssdbServer /bin/bash

5、编译和安装http://ideawu.github.io/ssdb-docs/install.html

wget --no-check-certificate https://github.com/ideawu/ssdb/archive/master.zip
unzip master
cd ssdb-master
make
make install
 6、如果缺少组件按照提示使用yum命令安装，如果已有autoconf，还提示安装autoconf， 其实是没有装which，使用命令

yum install -y which 之后再编译

7、

（1）启动服务, 此命令会阻塞住命令行

./ssdb-server ssdb.conf

或者启动为后台进程(不阻塞命令行)

./ssdb-server -d ssdb.conf

（2）客户端启动 ssdb 命令行

./tools/ssdb-cli -p 8888

（3）停止服务 ssdb-server

./ssdb-server ssdb.conf -s stop

8、ssdb.conf文件默认只能本机访问，远程访问修改ip为0.0.0.0，需要密码设置auth项



9、连接测试



10、语法：http://ssdb.io/ssdb-get-started.pdf，要用迅雷才能下，很奇怪 
