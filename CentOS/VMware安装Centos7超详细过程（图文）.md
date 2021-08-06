# VMware安装Centos7超详细过程（图文）



本篇文章主要介绍了VMware安装Centos7超详细过程（图文），具有一定的参考价值，感兴趣的小伙伴们可以参考一下

**1.软硬件准备**

软件：推荐使用VMwear，我用的是VMwear 12

镜像：CentOS7 ,如果没有镜像可以在官网下载 ：http://isoredirect.centos.org/centos/7/isos/x86_64/CentOS-7-x86_64-DVD-1804.iso

这里也放上百度云盘下载地址：

链接：https://pan.baidu.com/s/12oBtfjqTe0BAsXacZ4LEag 
提取码：ex9a 
 

![img](https://img-blog.csdn.net/20180711223703824?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JhYnl4dWU=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

硬件：因为是在宿主机上运行虚拟化软件安装centos，所以对宿主机的配置有一定的要求。最起码I5CPU双核、硬盘500G、内存4G以上。

![img](https://img-blog.csdn.net/20180711223715242?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JhYnl4dWU=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

**2.虚拟机准备**

1.打开VMwear选择新建虚拟机

![img](https://img-blog.csdn.net/20180711223726365?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JhYnl4dWU=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

2.典型安装与自定义安装

典型安装：VMwear会将主流的配置应用在虚拟机的操作系统上，对于新手来很友好。

自定义安装：自定义安装可以针对性的把一些资源加强，把不需要的资源移除。避免资源的浪费。

这里我选择自定义安装。

![img](https://img-blog.csdnimg.cn/img_convert/8afab7ddde63e03b8205d02505e266d7.png)![img](https://img-blog.csdn.net/20180711223827626?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JhYnl4dWU=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

3.虚拟机兼容性选择

这里要注意兼容性，如果是VMwear12创建的虚拟机复制到VM11、10或者更低的版本会出现一不兼容的现象。如果是用VMwear10创建的虚拟机在VMwear12中打开则不会出现兼容性问题。

![img](https://img-blog.csdnimg.cn/img_convert/103c72662d151f9f63c1c43ad14c6622.png)![img](https://img-blog.csdn.net/20180711223841653?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JhYnl4dWU=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

4.选择稍后安装操作系统

![img](https://img-blog.csdnimg.cn/img_convert/31a97c101935deb5734490b44c4aae71.png)![img](https://img-blog.csdn.net/20180711223854551?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JhYnl4dWU=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

5.操作系统的选择

这里选择之后安装的操作系统，正确的选择会让vm tools更好的兼容。这里选择linux下的CentOS

![img](https://img-blog.csdn.net/20180711223907671?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JhYnl4dWU=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

 

6.虚拟机位置与命名

虚拟机名称就是一个名字，在虚拟机多的时候方便自己找到。

VMwear的默认位置是在C盘下，我这里改成F盘。

![img](https://img-blog.csdn.net/20180711223917420?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JhYnl4dWU=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

![img](https://img-blog.csdnimg.cn/img_convert/0b920b4159a48142576f5d229a719495.png)

7.处理器与内存的分配

处理器分配要根据自己的实际需求来分配。在使用过程中CPU不够的话是可以再增加的。这次只做安装CentOS演示，所以处理器与核心都选1.

![img](https://img-blog.csdnimg.cn/img_convert/16ba0052da2de4c94b1b102d42f4158e.png)![img](https://img-blog.csdn.net/20180711223929865?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JhYnl4dWU=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

内存也是要根据实际的需求分配。我的宿主机内存是8G所以我给虚拟机分配2G内存。

![img](https://img-blog.csdn.net/20180711223943268?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JhYnl4dWU=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

![img](https://img-blog.csdnimg.cn/img_convert/315ac15d6b09449a80f6884ab47a38b1.png)

8.网络连接类型的选择，网络连接类型一共有桥接、NAT、仅主机和不联网四种。

桥接：选择桥接模式的话虚拟机和宿主机在网络上就是平级的关系，相当于连接在同一交换机上。

NAT：NAT模式就是虚拟机要联网得先通过宿主机才能和外面进行通信。

仅主机：虚拟机与宿主机直接连起来

桥接与NAT模式访问互联网过程，如下图所示

![img](https://img-blog.csdn.net/20180711224004659?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JhYnl4dWU=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

桥接与NAT区别

这里选择桥接模式

![img](https://img-blog.csdn.net/20180711224016785?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JhYnl4dWU=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)![img](https://img-blog.csdnimg.cn/img_convert/0a07bc5585641e1e361e75578db1fc22.png)

9.其余两项按虚拟机默认选项即可

![img](https://img-blog.csdn.net/20180711224042387?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JhYnl4dWU=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

10.磁盘容量

磁盘容量暂时分配100G即可后期可以随时增加，不要勾选立即分配所有磁盘，否则虚拟机会将100G直接分配给CentOS，会导致宿主机所剩硬盘容量减少。

勾选将虚拟磁盘拆分成多个文件，这样可以使虚拟机方便用储存设备拷贝复制。

![img](https://img-blog.csdn.net/20180711224059391?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JhYnl4dWU=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

11.磁盘名称，默认即可

![img](https://img-blog.csdn.net/20180711224115667?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JhYnl4dWU=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

12.取消不需要的硬件

点击自定义硬件

![img](https://img-blog.csdn.net/2018071122413290?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JhYnl4dWU=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

选择声卡、打印机等不需要的硬件然后移除。

![img](https://img-blog.csdn.net/20180711224147231?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JhYnl4dWU=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

13.点击完成，已经创建好虚拟机。

![img](https://img-blog.csdn.net/20180711224200707?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JhYnl4dWU=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

**3.安装CentOS**

1.连接光盘

右击刚创建的虚拟机，选择设置

![img](https://img-blog.csdn.net/20180711224217850?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JhYnl4dWU=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

先选择CD/DVD，再选择使用ISO映像文件，最后选择浏览找到下载好的镜像文件。启动时连接一定要勾选上后确定。

![img](https://img-blog.csdn.net/20180711224233121?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JhYnl4dWU=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

2.开启虚拟机

![img](https://img-blog.csdn.net/20180711224302639?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JhYnl4dWU=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

3.安装操作系统

开启虚拟机后会出现以下界面

1. Install CentOS 7 安装CentOS 7
2. Test this media & install CentOS 7 测试安装文件并安装CentOS 7
3. Troubleshooting 修复故障

选择第一项，安装直接CentOS 7，回车，进入下面的界面

![img](https://img-blog.csdnimg.cn/img_convert/12d7de06df36016247c4a8ddcb38f478.png)![img](https://img-blog.csdn.net/20180711224323926?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JhYnl4dWU=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

选择安装过程中使用的语言，这里选择英文、键盘选择美式键盘。点击Continue

![img](https://img-blog.csdn.net/2018071122433632?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JhYnl4dWU=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

首先设置时间

![img](https://img-blog.csdn.net/2018071122434772?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JhYnl4dWU=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

时区选择上海，查看时间是否正确。然后点击Done

![img](https://img-blog.csdn.net/20180711224410105?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JhYnl4dWU=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

选择需要安装的软件

![img](https://img-blog.csdn.net/20180711224421911?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JhYnl4dWU=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

选择 Server with Gui，然后点击Done

![img](https://img-blog.csdn.net/20180711224438720?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JhYnl4dWU=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

选择安装位置，在这里可以进行磁盘划分。

![img](https://img-blog.csdn.net/20180711224452307?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JhYnl4dWU=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

选择i wil configure partitioning（我将会配置分区），然后点击done

![img](https://img-blog.csdn.net/20180711224505907?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JhYnl4dWU=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

如下图所示，点击加号，选择/boot，给boot分区分200M。最后点击Add

![img](https://img-blog.csdn.net/20180711224522794?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JhYnl4dWU=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

然后以同样的办法给其他三个区分配好空间后点击Done

![img](https://img-blog.csdn.net/20180711224533382?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JhYnl4dWU=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

然后会弹出摘要信息，点击AcceptChanges(接受更改)

![img](https://img-blog.csdn.net/20180711224549412?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JhYnl4dWU=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

设置主机名与网卡信息

![img](https://img-blog.csdn.net/20180711224603320?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JhYnl4dWU=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

首先要打开网卡，然后查看是否能获取到IP地址(我这里是桥接)，再更改主机名后点击Done。

![img](https://img-blog.csdn.net/20180711224618785?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JhYnl4dWU=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

最后选择Begin Installation(开始安装)

![img](https://img-blog.csdn.net/2018071122463197?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JhYnl4dWU=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

设置root密码

![img](https://img-blog.csdn.net/2018071122464660?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JhYnl4dWU=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

设置root密码后点击Done

![img](https://img-blog.csdn.net/20180711224658899?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JhYnl4dWU=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

点击USER CREATION 创建管理员用户

![img](https://img-blog.csdn.net/20180711224711277?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JhYnl4dWU=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

输入用户名密码后点击Done

![img](https://img-blog.csdn.net/2018071122472498?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JhYnl4dWU=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

等待系统安装完毕重启系统即可

![img](https://img-blog.csdn.net/20180711224741348?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JhYnl4dWU=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

 

以上就是本文的全部内容，希望对大家的学习有所帮助。

**以下为我自己整理的克隆虚拟机和设置固定IP的方法，记录一下，以防忘记：**

***\**\*桥接模式网络配置\*\**\***

***\*1、配置ip地址等信息在/etc/sysconfig/network-scripts/ifcfg-ens33文件里做如下配置：\****

 命令：

```
vi   /etc/sysconfig/network-scripts/ifcfg-ens33
```

修改如下：

```
TYPE="Ethernet"   # 网络类型为以太网



BOOTPROTO="static"  # 手动分配ip



NAME="ens33"  # 网卡设备名，设备名一定要跟文件名一致



DEVICE="ens33"  # 网卡设备名，设备名一定要跟文件名一致



ONBOOT="yes"  # 该网卡是否随网络服务启动



IPADDR="192.168.220.101"  # 该网卡ip地址就是你要配置的固定IP，如果你要用xshell等工具连接，220这个网段最好和你自己的电脑网段一致，否则有可能用xshell连接失败



GATEWAY="192.168.220.2"   # 网关



NETMASK="255.255.255.0"   # 子网掩码



DNS1="8.8.8.8"    # DNS，8.8.8.8为Google提供的免费DNS服务器的IP地址
```

**2、\**配置网络工作\****

在/etc/sysconfig/network文件里增加如下配置

```
命令：



 



vi /etc/sysconfig/network



 



 



修改：



 



NETWORKING=yes # 网络是否工作，此处一定不能为no
```

3、***\**\*配置公共DNS服务(可选)\*\**\***

在/etc/resolv.conf文件里增加如下配置

```
nameserver 8.8.8.8
```

4、***\**\*关闭防火墙\*\**\***

```
systemctl stop firewalld # 临时关闭防火墙



systemctl disable firewalld # 禁止开机启动
```

5、***\**\*重启网络服务\*\**\***

```
service network restart
```

 下面是克隆虚拟机：

先查看虚拟机的网关

![img](https://img-blog.csdnimg.cn/20181118133935906.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2JhYnl4dWU=,size_16,color_FFFFFF,t_70)

2、将要克隆的虚拟机关机，右键点击要克隆的虚拟机：

右键点击虚拟机，选择“管理”、“克隆”

![img](https://img-blog.csdn.net/20180704204058261?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L21pamljaHVpMjE1Mw==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

然后下一步

![img](https://img-blog.csdn.net/20180704204226663?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L21pamljaHVpMjE1Mw==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

再下一步

![img](https://img-blog.csdn.net/20180704204252548?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L21pamljaHVpMjE1Mw==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

选择第二个“创建完整克隆”，后下一步

![img](https://img-blog.csdn.net/20180704204326257?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L21pamljaHVpMjE1Mw==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

给自己的克隆机命名、选择位置后点击“完成”。

![img](https://img-blog.csdn.net/20180704204850768?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L21pamljaHVpMjE1Mw==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

然后就开始克隆了，时间不会太久，整个过程大概1~2分钟。

完成克隆后点击关闭即克隆成功了。此时是可以在虚拟机列表中看到刚刚克隆的虚拟机“Clone”的。如下：

![img](https://img-blog.csdn.net/20180704204944459?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L21pamljaHVpMjE1Mw==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

此时这个克隆出来的虚拟机和原虚拟机各个配置都是一样的，我们接下来要对网络、主机名等进行配置。

修改配置文件***\*/etc/sysconfig/network-scripts/ifcfg-ens33中的IPADDR\****

```
IPADDR="192.168.220.102"
```

修改主机名：

```
hostnamectl set-hostname   xxxx(你要的主机名字)
```

 修改hosts文件，将名字和IP建立联系

输入命令“vi /etc/hosts”后，在配置文件中加入

```
127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4



::1         localhost localhost.localdomain localhost6 localhost6.localdomain6



192.168.220.103（你锁修改的主机IP）   xxxxxxxx(你要的主机名字)
```

重启:reboot 