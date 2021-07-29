# [linux下各安装包的安装方法](https://www.cnblogs.com/Mr-liyang/p/7645729.html)

一、rpm包安装方式步骤： 
1、找到相应的软件包，比如soft.version.rpm，下载到本机某个目录； 

2、打开一个终端，su -成root用户； 

3、cd soft.version.rpm所在的目录； 

4、输入rpm -ivh soft.version.rpm


**详细介绍：**

\1. 安装：
　　我只需简单的一句话，就可以说完。执行：
　　rpm –ivh rpm的软件包名
　  更高级的，请见下表：
　　rpm参数 参数说明
　　-i 安装软件
　　-t 测试安装，不是真的安装
　　-p 显示安装进度
　　-f 忽略任何错误
　　-U 升级安装
　　-v 检测套件是否正确安装
　　这些参数可以同时采用。更多的内容可以参考RPM的命令帮助。
\2. 卸载：
　　我同样只需简单的一句话，就可以说完。执行：
　　rpm –e 软件名
　　不过要注意的是，后面使用的是软件名，而不是软件包名。例如，要安装software-1.2.3-1.i386.rpm这个包时，应执行：
　　rpm –ivh software-1.2.3-1.i386.rpm
　　而当卸载时，则应执行：
　　rpm –e software。
另外，在Linux中还提供了象GnoRPM、kpackage等图形化的RPM工具，使得整个过程会更加简单。

二、deb包安装方式步骤： 
1、找到相应的软件包，比如soft.version.deb，下载到本机某个目录； 

2、打开一个终端，su -成root用户； 

3、cd soft.version.deb所在的目录； 

4、输入dpkg -i soft.version.deb

**详细介绍：**
    这是Debian Linux提供的一个包管理器，它与RPM十分类似。

​    但由于RPM出现得更早，所以在各种版本的Linux都常见到。

​    而debian的包管理器dpkg则只出现在Debina Linux中，其它Linux版本一般都没有。
　　1. 安装
　  dpkg –i deb的软件包名
　　如：dpkg –i software-1.2.3-1.deb
　　2. 卸载
　　 dpkg –e 软件名
　　如：dpkg –e software

​    3.查询：查询当前系统安装的软件包：

​    dpkg –l ‘*软件包名*’

​    如：dpkg –l '*software*'

三、tar.gz源代码包安装方式： 
1、找到相应的软件包，比如soft.tar.gz，下载到本机某个目录； 

2、打开一个终端，su -成root用户； 

3、cd soft.tar.gz所在的目录； 

4、tar -xzvf soft.tar.gz //一般会生成一个soft目录 

5、cd soft 

6、./configure 

7、make 

8、make install

**详细介绍：**

\1. 安装：
　　整个安装过程可以分为以下几步：
　　1） 取得应用软件：通过下载、购买光盘的方法获得；
　　2）解压缩文件：一般tar包，都会再做一次压缩，如gzip、bz2等，所以你需要先解压。如果是最常见的gz格式，则可以执行：“tar –xvzf 软件包名”，就可以一步完成解压与解包工作。如果不是，则先用解压软件，再执行“tar –xvf 解压后的tar包”进行解包；
　　3） 阅读附带的INSTALL文件、README文件；
　　4） 执行“./configure”命令为编译做好准备；
　　5） 执行“make”命令进行软件编译；
　　6） 执行“make install”完成安装；
　　7） 执行“make clean”删除安装时产生的临时文件。
　　好了，到此大功告成。我们就可以运行应用程序了。但这时，有的读者就会问，我怎么执行呢？这也是一个Linux特色的问题。其实，一般来说， Linux的应用软件的可执行文件会存放在/usr/local/bin目录下！不过这并不是“放四海皆准”的真理，最可靠的还是看这个软件的 INSTALL和README文件，一般都会有说明。
\2. 卸载：
　　通常软件的开发者很少考虑到如何卸载自己的软件，而tar又仅是完成打包的工作，所以并没有提供良好的卸载方法。
　　那么是不是说就不能够卸载呢！其实也不是，有两个软件能够解决这个问题，那就是Kinstall和Kife，它们是tar包安装、卸载的黄金搭档。

四、tar.bz2源代码包安装方式： 
1、找到相应的软件包，比如soft.tar.bz2，下载到本机某个目录； 

2、打开一个终端，su -成root用户； 

3、cd soft.tar.bz2所在的目录； 

4、tar -xjvf soft.tar.bz2 //一般会生成一个soft目录 

5、cd soft 

6、./configure 

7、make 

8、make install 

五、apt方式安装：（安装deb包）
1、打开一个终端，su -成root用户； 

2、apt-cache search soft 注：soft是你要找的软件的名称或相关信息 

3、如果2中找到了软件soft.version，则用apt-get install soft.version命令安装软件

 

注：只要你可以上网，只需要用apt-cache search查找软件，用apt-get install软件 
**详细介绍：**

apt-get是debian，ubuntu发行版的包管理工具，与红帽中的yum工具非常类似。

apt-get命令一般需要[root权限](http://baike.baidu.com/view/3967294.htm)执行，所以一般跟着sudo命令例sudo apt-get xxxx

```
apt-get install packagename——安装一个新软件包（参见下文的aptitude）
apt-get remove packagename——卸载一个已安装的软件包（保留配置文件）
apt-get --purge remove packagename——卸载一个已安装的软件包（删除配置文件）
dpkg --force-all --purge packagename ——有些软件很难卸载，而且还阻止了别的软件的应用，就可以用这个，不过有点冒险。
apt-get autoremove——因为apt会把已装或已卸的软件都备份在硬盘上，所以如果需要空间的话，可以让这个命令来删除你已经删掉的软件。
apt-get autoclean——定期运行这个命令来清除那些已经卸载的软件包的.deb文件。通过这种方式，可以释放大量的磁盘空间。如果需求十分迫切，可以使用apt-get clean以释放更多空间。这个命令会将已安装软件包裹的.deb文件一并删除。
apt-get clean——这个命令会把安装的软件的备份也删除，不过这样不会影响软件的使用的。
apt-get upgrade——更新所有已安装的软件包
apt-get dist-upgrade——将系统升级到新版本
apt-cache search string——在软件包列表中搜索字符串
apt-cache showpkg pkgs——显示软件包信息。
apt-cache stats——查看库里有多少软件
apt-cache dumpavail——打印可用软件包列表。
apt-cache show pkgs——显示软件包记录，类似于dpkg –print-avail。
apt-cache pkgnames——打印软件包列表中所有软件包的名称
（需要定期运行这一命令以确保您的软件包列表是最新的）
 
```

 

六、yum方式安装：(安装rpm包)

rpm 是linux的一种软件包名称，以.rmp结尾，安装的时候语法为：rpm -ivh。
rpm包的安装有个很大的缺点就是文件的关联性太大，有时装一个软件要安装很多其他的软件包，很麻烦。
所以为此RedHat小红帽开发了yum安装方法，他可以彻底解决这个关联性的问题，很方便，只要配置两个文件即可安装，安装方法是：yum -y install 。
yum并不是一中包，而是安装包的软件

```
七、bin文件安装： 
如果你下载到的软件名是soft.bin，一般情况下是个可执行文件，安装方法如下： 

1、打开一个终端，su -成root用户； 

2、chmod +x soft.bin 

3、./soft.bin //运行这个命令就可以安装软件了 


八、不需要安装的软件： 
有了些软件，比如lumaqq，是不需要安装的，自带jre解压缩后可直接运行。假设 

下载的是lumaqq.tar.gz，使用方法如下： 

1、打开一个终端，su -成root用户； 

2、tar -xzvf lumaqq.tar.gz //这一步会生成一个叫LumaQQ的目录 

3、cd LumaQQ 

4、chmod +x lumaqq //设置lumaqq这个程序文件为可运行 

5、此时就可以运行lumaqq了，用命令./lumaqq即可，但每次运行要输入全路径或 

切换到刚才生成的LumaQQ目录里 

6、为了保证不设置路径就可以用，你可以在/bin目录下建立一个lumaqq的链接， 

用命令ln -s lumaqq /bin/ 即可，以后任何时候打开一个终端输入lumaqq就可以 

启动QQ聊天软件了 

7、 如果你要想lumaqq有个菜单项，使用菜单编辑工具，比如Alacarte Menu 

Editor，找到上面生成的LumaQQ目录里的lumaqq设置一个菜单项就可以了，当然你 

也可以直接到 /usr/share/applications目录，按照里面其它*.desktop文件的格 

式生成一个自己的desktop文件即可。
```

 

 

===================================================================================
软件的安装 
　　---- Linux下软件的安装主要有两种不同的形式。第一种安装文件名为filename.tar.gz。另一种安装文件名为 filename.i386.rpm。以第一种方式发行的软件多为以源码形式发送的。第二种方式则是直接以二进制形式发行的。i386即表示该软件是按 Inter 386指令集编译生成的。 
　　---- 对于第一种，安装方法如下： 
　　---- 首先，将安装文件拷贝至你的目录中。例如，如果你是以root身份登录上的，就将软件拷贝至/root中。 
　　---- #cp filename.tar.gz /root 
　　---- 由于该文件是被压缩并打包的，所以，应对其解压缩。命令为： 
　　---- #tar xvzf filename.tar.gz 
　　---- 执行该命令后，安装文件按路径，解压缩在当前目录下。用ls命令可以看到解压缩后的文件。通常在解压缩后产生的文件中，有名为"INSTALL"的文件。该文件为纯文本文件，详细讲述了该软件包的安装方法。 
　　---- 对于多数需要编译的软件，其安装的方法大体相同。执行解压缩后产生的一个名为configure的可执行脚本程序。它是用于检查系统是否有编译时所需的库，以及库的版本是否满足编译的需要等安装所需要的系统信息。为随后的编译工作做准备。命令为： 
　　---- #./configure 
　　---- 如果检查过程中，发现有错误，configure将给予提示，并停止检查。你可以跟据提示对系统进行配置。再重新执行该程序。检查通过后，将生成用于编译 的MakeFile文件。此时，可以开始进行编译了。编译的过程视软件的规模和计算机的性能的不同，所耗费的时间也不同。命令为： 
　　---- #make 
　　---- 成功编译后，键入如下的命令开始安装： 
　　---- #make install 
　　---- 安装完毕，应清除编译过程中产生的临时文件和配置过程中产生的文件。键入如下命令： 
　　#make clean 
　　#make distclean 
　　至此，软件的安装结束。 
　　---- 对于第二种，其安装方法要简单的多。 
　　---- 同第一种方式一样，将安装文件拷贝至你的目录中。然后使用rpm来安装该文件。命令如下： 
　　---- #rpm -i filename.i386.rpm 
　　---- rpm将自动将安装文件解包，并将软件安装到缺省的目录下。并将软件的安装信息注册到rpm的数据库中。参数i的作用是使rpm进入安装模式。 
　　---- 另外，还有一些Linux平台下的商业软件。在其安装文件中，有Setup安装程序，其安装方法同Windows平台下的一样。如:Corel WordPerfect。 
　　软件的卸载 
　　---- 软件的卸载主要是使用rpm来进行的。卸载软件首先要知道软件包在系统中注册的名称。键入命令： 
　　---- #rpm -q -a 
　　---- 即可查询到当前系统中安装的所有的软件包。参数q的作用是使rpm进入查询命令模式。参数a是查询模式的子参数，意为全部（ALL）。查询到的信息较多，可使用less人屏显示。 
　　---- 确定了要卸载的软件的名称，就可以开始实际卸载该软件了。键入命令： 
　　---- #rpm -e [package name] 
　　---- 即可卸载软件。参数e的作用是使rpm进入卸载模式。对名为[package name]的软件包进行卸载。由于系统中各个软件包之间相互有依赖关系。如果因存在依赖关系而不能卸载，rpm将给予提示并停止卸载。你可以使用如下的命 令来忽略依赖关系，直接开始卸载： 
　　---- #rpm -e [package name] -nodeps 
　　---- 忽略依赖关系的卸载可能会导致系统中其它的一此软件无法使用。你可以使用 
　　---- #rpm -e [package name] -test 
　　---- 使rpm进行一次卸载预演，而不是真正卸载。这样可以使你检查一下软件是否存在有依赖关系。卸载过程中是否有错误。