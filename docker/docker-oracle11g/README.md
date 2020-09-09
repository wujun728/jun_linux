#### 项目介绍
基于Oracle Linux 7.5实现了Oracle Database 11gR2 企业版容器化运行;

本脚本仅用作研究如何把oracle database制作成镜像,请勿作商用,谢谢.

有疑问请联系:rancococ@qq.com

#### 前期准备
从Oracle官方下载安装包到本地的http服务器某个目录,如下:

1. http://192.168.8.100/oracle11g/p13390677_112040_Linux-x86-64_1of7.zip
2. http://192.168.8.100/oracle11g/p13390677_112040_Linux-x86-64_2of7.zip

从docker hub或国内docker加速站点上下载oralcelinux:7的docker镜像,并重新打标签为:
192.168.8.251/library/oraclelinux:7

#### 安装教程
1. build preinstall:./01preinstall/01build.sh
2. build installed:./02installed/01build.sh
3. build database:./03database/01build.sh

#### 使用说明
数据库信息
sid:orcl
port:1521
system/oracle

镜像用法
docker run -it --rm --memory=2g --shm-size=2g --name="oracle-11g-ee-database" --hostname="database" \
           -p 1521:1521 192.168.8.251/library/oracle-11g-ee:database
或采用docker-compose进行管理

#### 参与贡献
1. rancococ@qq.com

#### 特别说明
- oraclelinux做为基础镜像,有了oracle-rdbms-server-11gR2-preinstall包能自动做一些预处理;
- 准备一个http服务,用wget从http服务器上下载安装包并解压;
- oracle对共享内存有要求,在build或run的时候需要指定参数:--memory=2g --shm-size=2g;
- 执行安装脚本需要注意权限,有的脚本是以root账号执行,有的是以oracle账号执行;
- 脚本中注意单引号和双引号的区别;
- 注意ins_emagent.mk引起的BUG,即:在makefile中添加链接libnnz11库的参数,修改/u01/app/oracle/product/11.2.0/dbhome_1/sysman/lib/ins_emagent.mk",将\$(MK_EMAGENT_NMECTL)修改为:\$(MK_EMAGENT_NMECTL)-lnnz11
- oracle数据库跟主机名强相关,build的时候随机生成了一个主机名,导致启动时会报错,所以在启动脚本entrypoint_oracle.sh中增加了两个方法,即:根据当前新的主机名修改tnsnames.ora和listener.ora,再启动监听器和实例
- 注意创建数据库实例的响应文件db_create.rsp611行相关参数:
INITPARAMS="java_jit_enabled=false,memory_target=0,sga_target=1024,pga_aggregate_target=100,processes=1000,open_cursors=1000"
特别是java_jit_enabled=false否则要出错
