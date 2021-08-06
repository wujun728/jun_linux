超详细的CentOS7.4下载与图文安装

置顶 零碎de記憶 2020-02-29 14:12:29  361787  收藏 1584
分类专栏： Linux
版权

Linux
专栏收录该内容
12 篇文章4 订阅
订阅专栏
一、CentOS7.4下载
          官网下载地址：http://vault.centos.org/

    1、进入CentOS下载官网，找到CentOS7.4版本



 

 2、在CentOS7.4版本页面中，找到isos/



 

   3、进入页面后，可以看到x86_64



 

 4、在CentOS下载页面中，选择 CentOS-7-x86_64-DVD-1708.torrent进行下载



 

5、下载完成之后，由于“CentOS-7-x86_64-DVD-1708.torrent”只是一个BT种子文件，而且非常小，这就需要我们使用迅雷等工具来对源镜像进行下载了

   （1）打开迅雷，新建任务，把“CentOS-7-x86_64-DVD-1708.torrent”BT种子文件拖入到新建任务中，并点击立即下载



 

   （2）下载完成之后会生成如下的几个文件，CentOS-7-x86_64-DVD-1708.iso就是我们在工作中使用的镜像了



 

 

二、CentOS7.4安装
   1、打开你的VMware Workstation Pro，并点击“创建新的虚拟机”，没有安装VMware Workstation Pro请点击VMware Workstation 14下载与安装



 

2、点选典型(推荐)(T)，并点击“下一步”



 

3、点选稍后安装操作系统(S)，并点击“下一步”



 

 

4、点选Linux(L)，因为我们之前下载的 CentOS-7-x86_64-DVD-1708.iso 是64位 7.4版本的，所以这里我们选择CentOS 7 64位，并点击“下一步”



 

5、虚拟机名称可以更改也可以不更改看自己需求，修改虚拟机的安装路径，并点击“下一步”



 

6、磁盘选择默认为20.0GB，点选将虚拟磁盘存储为单个文件(O)，并点击“下一步”



 

7、点击“完成”



 

8、点击“编辑虚拟机设置”



 

9、点选“使用ISO映像文件(M)”，并添加我们之前下载好的CentOS-7-x86_64-DVD-1708.iso



 

10、默认为NAT 模式(N)：用于共享主机的IP地址即可



 

提示：11-13步骤 移除USB控制器、声卡和打印机 只是为了腾出更多的资源空间 (可以选择跳过 不移除)

11、选择USB 控制器，并点击“移除(R)”



 

12、选择声卡，并点击“移除(R)”



 

13、选择打印机，并点击“移除(R)”，最后点击“确定”



 

14、点击“开启此虚拟机”



 

15、正在开启虚拟机，鼠标移入到虚拟机中，并按下“↑”键，选择Install CentOS 7，最后按下“Enter 键”

        提示：  鼠标移动到虚拟机内部单击或者按下Ctrl + G，鼠标即可移入到虚拟机中
    
                     按下Ctrl + Alt，鼠标即可移出虚拟机
    
        注意：  在虚拟机中的操作，鼠标必须要移入到虚拟机中，否则虚拟机感应不到，无法对其进行操作



 

16、按下“Enter 键”





 

17、默认安装过程中的安装界面使用English (英语)，点击“Continue”



 

18、配置时区 (DATE & TIME)

       （1）选择DATE & TIME



​       

       （2）时区设置为 Region：Asia    City：Shanghai
    
                日期和时间 设置与自己的电脑时间同步，最后点击“Done”



 

19、设置软件选择 (SOFTWARE SELECTION)

         （1）选择SOFTWARE SELECTION



​        

       （2）点击勾选 Compatibility Libraries 和 Development Tools



 

如果希望安装带有界面的CentOS，请在左边Base Environment中，选择Server with GUI(带图形用户界面的服务器)，默认为Minimal Install (最小安装)，提示：如果安装有界面版本的，在如下的第22步骤中的操作会有所不同 (安装有界面版本的其实用处不大，都是可以通过命令行来设置的)，这里我没有安装有界面版本的



 

20、设置安装位置 (INSTALLATION DESTINATION)

      （1）选择INSTALLATION DESTINATION



 

   （2）点选 I will configuire parttioning，然后再点击“Done”



 

 （3）更改模式，标准分区Standard Partition，点击“+”按钮添加分区



​     

（4）添加 /boot分区，大小300MB，Add mount point





 

（5）添加 swap分区，一般情况是物理内存的2倍大小，用于物理内存不足时使用，但可能造成系统不稳定，所以看情况，可以设置小一点，甚至设置为0MB，这里我设置为512MB，Add mount point





 

（6）增加根分区，不填写大小，即默认剩余的空间都给根分区，Add mount point





 

（7）点击“Done”



 

（8）点击“Accept Changes”



 

21、点击“Begin Installation”，开始安装



 

22、设置系统用户root的密码 (ROOT PASSWORD)

    （1）选择ROOT PASSWORD



 

（2）为root设置密码 (密码长度最好不要小于6位数)，然后点击“Done”



 

23、等待安装完成，然后点击“Reboot”



 

三、CentOS7.4基本设置
1、登录CentOS，默认账号为root，密码为 你在前面安装时设置的root密码

提示：在输入密码时，linux为了安全起见，是看不到你输入的密码。同时，如果是使用的是键盘右边的数字键盘输入密码的话，建议查看一下，数字键盘是否开启 (建议使用字母按键上面一排的 数字键输入密码)



 

2、配置IP地址，网关

cd /etc/sysconfig/network-scripts/    //进入到network-scripts目录下  

vi ifcfg-ens32  //编辑配置文件 

//修改以下内容
BOOTPROTO=static  //启用静态IP地址
ONBOOT=yes      //开启自动启用网络连接


//添加以下内容
IPADDR=192.168.30.1      //设置IP地址
NETMASK=255.255.255.0   //子网掩码
GATEWAY=192.168.131.2   //设置网关










2.1、如何设置Linux的IP地址

1、在本地电脑打开“命令行窗口”，输入命令ipconfig，查看 以太网适配器 VMware Network Adapter VMnet8下的IPv4 地址

2、可以看到 以太网适配器 VMware Network Adapter VMnet8下的IPv4 地址为 192.168.30.2

3、当我们设置Linux的IP地址时，需要保证Linux的IP地址 与 VMnet8下的IPv4地址 的前面三位数必须相同，即 192.168.30 必须相同，这样Linux就能跟我们本地电脑互相通信，最后一位数不相同即可，例如Linux的IP地址可以设置为192.168.30.1 或者 192.168.30.124等



  

2.2、如何设置Linux的网关：

1、点击编辑(E) → 虚拟网络编辑器(N)



 

 2.3、如何设置Linux的网关，选择VMnet8，再点击"NAT设置"按钮，查看VMnet8 (NAT 模式)下的子网掩码





 

3、查看VMnet8 (NAT 模式)下的网关，选择VMnet8，再点击"NAT设置"按钮



 

 

3、重启网络服务

service network restart




4、设置DNS地址     

vi /etc/resolv.conf    //编辑 resolv.conf文件

nameserver 114.114.114.114   //添加DNS地址

 

可以添加多个DNS地址，格式为：
nameserver xxx1.xxx1.xxx1.xxx1
nameserver xxx2.xxx2.xxx2.xxx2


常用的DNS地址:

  阿里  223.5.5.5  或者  223.6.6.6

  谷歌  8.8.8.8

  国内移动、电信和联通通用的DNS  114.114.114.114




提示：如果是内网，配置上面的DNS地址有可能是访问不了外网的，在电脑右下角的网络图标中鼠标右键，选择打开"网络和Internet"设置，选择WLAN，然后在点击你连接的网络，查看网络信息



 

填写内网的IPv4 DNS 服务器地址即可



 

5、查看是否能够访问外网

ping -c3 www.baidu.com


PING www.a.shifen.com (14.215.177.38) 56(84) bytes of data.
64 bytes from 14.215.177.38 (14.215.177.38): icmp_seq=1 ttl=128 time=9.45 ms
64 bytes from 14.215.177.38 (14.215.177.38): icmp_seq=2 ttl=128 time=12.2 ms
64 bytes from 14.215.177.38 (14.215.177.38): icmp_seq=3 ttl=128 time=9.29 ms

--- www.a.shifen.com ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2004ms
rtt min/avg/max/mdev = 9.296/10.346/12.293/1.388 ms




6、永久关闭 firewalld防火墙（centos7默认的防火墙是firewalld防火墙，不是使用iptables，因此需要关闭firewalld服务）

systemctl stop firewalld.service  // 停止firewalld服务

systemctl disable firewalld.service // 开机禁用firewalld服务

iptables -L   //列出所有iptables规则




7、永久关闭SELinux防火墙

vi /etc/sysconfig/selinux       //编辑selinux文件

SELINUX=disabled         //把文件中的SELINUX=enforcing 改成 SELINUX=disabled 即可

sestatus    //查看SELinux状态




获取当前selinux防火墙的安全策略

sestatus
可以看到当前selinux防火墙的安全策略仍为enforcing，配置文件并未生效



 

 

这时需要我们重启，再去查看SELinux防火墙的状态，可以看到已经关闭了



 

8、给/etc/rc.d/rc.local 文件设置  “x”可执行权限，最初设置默认是没有可执行权限的

chmod +x /etc/rc.d/rc.local     //设置可执行权限


//设置前
-rwxr-xr--. 1 root root 473 Aug  5  2017 rc.local

//设置后
-rwxr-xr-x. 1 root root 473 Aug  5  2017 rc.local




9、输入“halt”，关闭虚拟机，并拍摄快照，保存当前配置





————————————————
版权声明：本文为CSDN博主「零碎de記憶」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/qq_39135287/article/details/83993574