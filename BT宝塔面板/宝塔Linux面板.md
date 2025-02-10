## 宝塔Linux面板环境

[点击去>>Linux版和Window版安装使用（宝塔官网使用教程）](https://www.bt.cn/?invite_code=MV9ya3Rpb2o=)

1、操作系统：全新系统(支持CentOS、Ubuntu、Debian、Fedora、Deepin)

2、确保是干净的操作系统，没有安装过其它环境带的Apache/Nginx/php/MySQL

3、宝塔Linux6.0版本是基于centos7开发的，强烈建议使用centos7.x 系统

4、内存要求：内存要求最低512MB，推荐768MB以上，纯面板约占系统60MB内存

## Linux安装宝塔面板方法

1.对硬盘进行挂载

使用SSH工具连接到你的云服务器，运行挂载命令：

> ```
> yum install wget -y && wget -O auto_disk.sh http://download.bt.cn/tools/auto_disk.sh && bash auto_disk.sh
> ```


出现提示按Y回车



2.执行宝塔安装命令



Centos安装命令：

> ```
> yum install -y wget && wget -O install.sh https://download.bt.cn/install/install_6.0.sh && sh install.sh ed8484bec
> ```

Ubuntu/Deepin安装命令：

> ```
> wget -O install.sh https://download.bt.cn/install/install-ubuntu_6.0.sh && sudo bash install.sh ed8484bec
> ```

Debian安装命令：

> ```
> wget -O install.sh https://download.bt.cn/install/install-ubuntu_6.0.sh && bash install.sh ed8484bec
> ```

Fedora安装命令:

> ```
> wget -O install.sh http://download.bt.cn/install/install_6.0.sh && bash install.sh
> ```

万能安装脚本:

> ```
> if [ -f /usr/bin/curl ];then curl -sSO https://download.bt.cn/install/install_panel.sh;else wget -O install_panel.sh https://download.bt.cn/install/install_panel.sh;fi;bash install_panel.sh ed8484bec
> ```