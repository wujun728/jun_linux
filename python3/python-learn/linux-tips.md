#我的archlinux之旅

###连接wifi
自从使用archlinux发行版后，连接wifi变得非常简单。

1.执行`sudo wifi-menu` 选择你要连接的热点，然后输入一个配置文件文件名称，回车保存，保存在/etc/netctl内。

2.执行`sudo netctl start config-file-name` 即将连接成功,输入`ifconfig`查看一下，wlp3s0是我的无线网卡设备名称。

    lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
            inet 127.0.0.1  netmask 255.0.0.0
            inet6 ::1  prefixlen 128  scopeid 0x10<host>
            loop  txqueuelen 0  (Local Loopback)
            RX packets 8332  bytes 416640 (406.8 KiB)
            RX errors 0  dropped 0  overruns 0  frame 0
            TX packets 8332  bytes 416640 (406.8 KiB)
            TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
    
    wlp3s0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
            inet 192.168.1.101  netmask 255.255.255.0  broadcast 255.255.255.255
            inet6 fe80::7a92:9cff:fe82:fc26  prefixlen 64  scopeid 0x20<link>
            ether 78:92:9c:82:fc:26  txqueuelen 1000  (Ethernet)
            RX packets 25621  bytes 21315978 (20.3 MiB)
            RX errors 0  dropped 0  overruns 0  frame 0
            TX packets 27776  bytes 6419587 (6.1 MiB)
            TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0


###linux下有线网络和无线网络同时工作
使用场景：有线网络用来办公，无线网络用来浏览网页。

思路：除了办公网络以外，其他的访问都走无线网卡的默认路由。

`sudo route add default netmask 0.0.0.0 gw 192.168.1.1 dev wlan0`

###linux下设置键盘敲击速率

`xset r rate 200 60`

###linux下改键
在$HOME下创建一个.Xmodmap 文件。

    !
    ! Swap Caps_Lock and Control_R
    !
    remove Lock = Caps_Lock
    remove Control = Control_R
    keysym Control_R = Caps_Lock
    keysym Caps_Lock = Control_R
    add Lock = Caps_Lock
    add Control = Control_R


###linux 下修改笔记本显示器亮度
`sudo echo 1000 >/sys/class/backlight/intel_backlight/brightness`


###archlinux下，在chromium内使用fcitx输入法
`sudo pacman -S fcitx-gtk2`


### arch下如何连接openvpn
安装openvpn客户端 `sudo pacman -S openvpn`

创建配置文件`vpn.conf`

    client
    remote vpn.example.com 443
    ca ca.crt
    cert demo.crt
    key demo.key
    comp-lzo yes
    dev tun
    proto tcp
    tls-auth ta.key 1
    nobind
    auth-nocache
    script-security 2
    persist-key
    persist-tun

使用root权限连接,因为openvpn要创建tun设备 `sudo openvpn config_file`


### 连接vpn后，设置某个网段走vpn的线路
可以先`route -n`看一下,没有的话再添加。tun0是vpn连接后创建的设备。

添加路由，使特定网段走刚创建的vpn线路：`sudo route add -net 130.89.200.0 netmask 255.255.255.0 dev tun0`


### arch下如何远程连接windows计算机？
`rdesktop -f -P -z -r sound:off -u Administrator 130.89.200.3:3389`


### 远程连接本地的virtualbox虚拟机
`sudo pacman -S virtualbox-ext-oracle`，安装后，在虚拟机-->显示-->远程设置，之后启动虚拟机，就可以使用rdesktop对localhost:3389的虚拟机进行访问了。


### virtualbox的快速启动办法
如果已经通过virtualbox的GUI建立好了虚拟机,下次启动虚拟机的时候，只要输入`VBoxSDL -vm <vm name>`即可,比如我的虚拟机名称为work，所以输入`VBoxSDL -vm work`即可。由于我使用的是`awesome wm`，所以只需要按下`Mod4 + f`即可全屏了。


### 我的gpg public key
[pubic key link](http://pgp.mit.edu/pks/lookup?op=get&search=0x18FEFBDB637DFA8F)

finger print: `87EA 1022 682A 420C F226  CA6D 18FE FBDB 637D FA8F`
