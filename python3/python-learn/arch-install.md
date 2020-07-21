#硬盘安装archlinux
###1.复制grub4dos-0.4.4下的grldr/grldr.mbr/menu.lst到c盘
###2.复制archlinux-2014.12.01-dual.iso到c:\archlinux.iso
###3.复制archlinux-2014.12.01-dual.iso\arch\boot\x86_64\下的vmlinuz archiso.img到c盘根目录
###4.c盘下新建boot.ini
cat <<EOF> boot.ini
[boot loader]
[operating systems]
c:\grldr.mbr="Grub4Dos"
EOF

###5.编辑menu.lst文件
cat <<EOF >> menu.lst
    title archlinux  install
    root  (hd0,0)
    kernel  /vmlinuz  archisolabel=archiso
    initrd  /archiso.img
    boot
EOF

###6.重启,选择"grub4dos",选择最后一项"archlinux install"

###7.当出现如下错误信息时（::Mounting  '/dev/disk/by-label/archiso '  to  '/run/archiso/bootmnt'）
mkdir  /win
mount  /dev/sda1  /win
modprobe  loop
losetup  /dev/loop6  /win/archlinux-2012.12.01-dual.iso
ln  -s  /dev/loop6  /dev/disk/by-label/archiso
exit
上面代码是将/win/archlinux.iso与/dev/disk/by-label/archiso联系起来连接

###8.接下来就是正常的安装了
reference:http://blog.csdn.net/holdsky/article/details/8497764

#archlinux 安装步骤
###1. 建立分区
cgdisk /dev/sda
12G
/ 8G
/home 3.5G
swap 0.5G

###2. 格式化分区
mkfs.ext4 /dev/sda1
mkfs.ext4 /dev/sda2
mkswap /dev/sda3
swapon /dev/sda3

###3. 挂载分区
mount /dev/sda1 /mnt
cd /mnt && mkdir home
mount /dev/sda2 /mnt/home

###4. 更新pacman mirror list
http://mirror.bit.edu.cn/archlinux/
http://mirrors.sohu.com/archlinux/$repo/os/i686
pacman -Sy

###5. 安装基本系统
pacstrap /mnt base base-devel

###6. 生成fstab
genfstab /mnt >> /mnt/etc/fstab

###7. 切换root并且设置密码
arch-chroot /mnt
passwd

###8. 设置hostname
echo arch > /etc/hostname

###9. 设置时区(实践表明，设置了反而会有问题)
date
ln -s /usr/share/zoneinfo/Asia/Taipei /etc/localtime
date

###10. 建立初始ramdisk环境
mkinitcpio -p linux

###11.啟用 DHCP 服務，以使安裝於 VirtualBox 的 Arch Linux 系統能連接網路 
systemctl enable dhcpcd.service

### 12.或者安装grub
pacman -S os-prober grub
pacman -S grub
grub-install --target=i386-pc --recheck --debug /dev/sda
grub-mkconfig -o /boot/grub/grub.cfg

###13.安装连接无线网络的必要package
pacman -S dialog netctl dhcpcd ifplugd wpa_actiond wpa_supplicant

###14.卸載分割區並重啟系統 
exit
unmount -R /mnt
reboot
poweroff
修改虚拟机设置 移除cd



##重启以后的设置
###15. 创建用户
useradd -m -G wheel -s /bin/bash demo

###16. 安装配置sudo
pacman -S sudo
vi /etc/sudoers

###17. 安装X
pacman -S xorg-server xorg-xinit xorg-server-utils
pacman -S awesome
cp /etc/skel/.x* ~
vi ~/.xinitrc
加exec awesome 在最下面
vi ~/.config/awesome/rc.lua
修改主题为zenburn

###18 安装openssh pkgfile net-tools
pacman -S openssh pkgfile net-tools

###19. 如果是vrtualbox,配置共享文件夹
###pacman -S virtualbox-guest-modules
###modprobe -a vboxsf
###echo vboxsf >/etc/modules-load.d/virtualbox.conf
###mount -t vboxsf CDs /mnt/cds/

###20. 安装slim
pacman -S slim
pacman -S slim-themes archlinux-themes-slim
sudo systemctl enable slim.service
修改/etc/slim.conf
default_user = <username>
focus_password = yes
所有的主题可以在/usr/share/slim/theme看到
current_theme = archlinux-simplyblack

###在登录的时候启动X
加在.bashrc [[ -z $DISPLAY && $XDG_VTNR -eq 1 ]] && exec startx

###vritualbox内运行archlinux的话还需要安装
pacman -S xf86-video-vesa

###如果安装了win8或者win7导致grub引导被覆盖了
1.安装EasyBCD
2.添加一个启动项: Add New Entry --> Linux/BSD --> Type GRUB(Legacy) --> Drive (你的linux boot所在分区) --> 勾上Use EaseBCD's copy of GRUB --> Add Entry.
3.重启选择刚添加的启动项，如果报错，先root (hd0,7)选择你的linux boot所在分区.
3.cat /boot/grub/grub.cfg, 找到关于你的arch启动的那一块，拍照或者先记录下来类似/boot/vmxxx 这样的段落.
4.kernel /boot/vmlinuz-linux root=UUID=XXXXXXXXX 手动输入一遍这个不能写错
5.initrd /boot/initramfs-linux.img
6.boot
7.不出意外，你就进入到了你的linux系统了。
8.这个时候，赶紧安装grub到你的/dev/sda.
grub-install --target=i386-pc --recheck --debug /dev/sda
grub-mkconfig -o /boot/grub/grub.cfg


安装字体 配置xterm
######################## ~/.Xresources内容################################
XTerm*utf8Title: true
XTerm*faceName: DejaVu Sans Mono:antialias=True:pixelsize=16
XTerm*faceNameDoublesize: WenQuanYi Micro Hei Mono:antialias=True:pixelsize=16
XTerm*inputMethod: fcitx
!xterm*faceSize: 10
xterm*vt100*geometry: 80x60
xterm*saveLines: 16384
xterm*loginShell: true
xterm*charClass: 33:48,35:48,37:48,43:48,45-47:48,64:48,95:48,126:48
xterm*termName: xterm-color
xterm*eightBitInput: false
xterm*foreground: rgb:a8/a8/a8
xterm*background: rgb:00/00/00
xterm*color0: rgb:00/00/00
xterm*color1: rgb:a8/00/00
xterm*color2: rgb:00/a8/00
xterm*color3: rgb:a8/54/00
xterm*color4: rgb:00/00/a8
xterm*color5: rgb:a8/00/a8
xterm*color6: rgb:00/a8/a8
xterm*color7: rgb:a8/a8/a8
xterm*color8: rgb:54/54/54
xterm*color9: rgb:fc/54/54
xterm*color10: rgb:54/fc/54
xterm*color11: rgb:fc/fc/54
xterm*color12: rgb:54/54/fc
xterm*color13: rgb:fc/54/fc
xterm*color14: rgb:54/fc/fc
xterm*color15: rgb:fc/fc/fc
######################## ~/.Xresources内容################################

mpd/mpc播放歌曲
db_file            "~/.config/mpd/database"
log_file           "~/.config/mpd/log"
music_directory    "~/music"
playlist_directory "~/.config/mpd/playlists"
pid_file           "~/.config/mpd/pid"
state_file         "~/.config/mpd/state"
sticker_file       "~/.config/mpd/sticker.sql"
input {
        plugin "curl"
}
audio_output {
        type            "alsa"
        name            "My ALSA Device"
}

前台运行
mpd --no-daemon 

显示所有歌曲
mpc listall 

添加所有歌曲
mpc listall|mpc add

开始播放
mpc play

播放下一首
mpc next

###如果archlinux没有声音
amixer sset Master unmute
