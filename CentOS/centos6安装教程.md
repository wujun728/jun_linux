# centos6安装教程



1、首先，要有一张CentOS 6.4的安装介质，使用介质启动电脑出现如下界面

界面说明：

![centos 6.4安装教程](http://www.it165.net/uploadfile/2013/0822/20130822081722642.png)

Install or upgrade an existing system 安装或升级现有的系统

install system with basic video driver 安装过程中采用基本的显卡驱动

Rescue installed system 进入系统修复模式

Boot from local drive 退出安装从硬盘启动

Memory test 内存检测

注：用联想E49安装时选择第一项安装时会出现屏幕显示异常的问题，后改用第二项安装时就没有出现问题

2、介质直接“skip”就可以了

![centos 6.4安装教程](http://www.it165.net/uploadfile/2013/0822/20130822081728993.png)

3、出现引导界面，点击“next”

![centos 6.4安装教程](http://www.it165.net/uploadfile/2013/0822/20130822081729453.png)

4、选中“English（English）”否则会有部分乱码问题

![centos 6.4安装教程](http://www.it165.net/uploadfile/2013/0822/20130822081732717.png)

5、键盘布局选择“U.S.English”

![centos 6.4安装教程](http://www.it165.net/uploadfile/2013/0822/20130822081733299.png)

6、选择“Basic Storage Devies”点击”Next”

![centos 6.4安装教程](http://www.it165.net/uploadfile/2013/0822/20130822081734270.png)

7、询问是否忽略所有数据，新电脑安装系统选择”Yes,discard any data”

![centos 6.4安装教程](http://www.it165.net/uploadfile/2013/0822/20130822081736631.png)

8、Hostname填写格式“英文名.姓”

![centos 6.4安装教程](http://www.it165.net/uploadfile/2013/0822/20130822081738896.png)

9、网络设置安装图示顺序点击就可以了

![centos 6.4安装教程](http://www.it165.net/uploadfile/2013/0822/20130822081740789.png)

10、时区可以在地图上点击，选择“shanghai”并取消System clock uses UTC前面的对勾

![centos 6.4安装教程](http://www.it165.net/uploadfile/2013/0822/20130822081743600.png)

11、设置root的密码

![centos 6.4安装教程](http://www.it165.net/uploadfile/2013/0822/20130822081745297.png)

12、硬盘分区，一定要按照图示点选

![centos 6.4安装教程](http://www.it165.net/uploadfile/2013/0822/20130822081746662.png)

13、调整分区，必须要有/home这个分区，如果没有这个分区，安装部分软件会出现不能安装的问题

![centos 6.4安装教程](http://www.it165.net/uploadfile/2013/0822/20130822081749300.png)

14、询问是否格式化分区

![centos 6.4安装教程](http://www.it165.net/uploadfile/2013/0822/20130822081751533.png)

15、将更改写入到硬盘

![centos 6.4安装教程](http://www.it165.net/uploadfile/2013/0822/20130822081752608.png)

16、引导程序安装位置

![centos 6.4安装教程](http://www.it165.net/uploadfile/2013/0822/20130822081754278.png)

17、最重要的一步，也是本教程最关机的一步，也是其他教程没有提及的一步，按图示顺序点击

![centos 6.4安装教程](http://www.it165.net/uploadfile/2013/0822/20130822081755789.png)

18、取消以下内容的所有选项

**Applications**

**Base System**

**Servers**

并对Desktops进行如下设置

即取消如下选项：

**Desktop Debugging and Performance Tools**

**Desktop Platform**

**Remote Desktop Clients**

**Input Methods****中仅保留ibus-pinyin-1.3.8-1.el6.x86_64,其他的全部取消**

![centos 6.4安装教程](http://www.it165.net/uploadfile/2013/0822/20130822081758822.png)

![centos 6.4安装教程](http://www.it165.net/uploadfile/2013/0822/20130822081800585.png)

19、选中Languages，并选中右侧的Chinese Support然后点击红色区域

![centos 6.4安装教程](http://www.it165.net/uploadfile/2013/0822/20130822081802177.png)

20、调整完成后如下图所示

![centos 6.4安装教程](http://www.it165.net/uploadfile/2013/0822/20130822081806806.png)

21、至此，一个最精简的桌面环境就设置完成了，

![centos 6.4安装教程](http://www.it165.net/uploadfile/2013/0822/20130822081808408.png)

22、安装完成，重启

![centos 6.4安装教程](http://www.it165.net/uploadfile/2013/0822/20130822081811282.png)

23、重启之后，的License Information

![centos 6.4安装教程](http://www.it165.net/uploadfile/2013/0822/20130822081813126.png)

24、Create User

Username：填写您的英文名（不带.姓）

Full Name：填写您的英文名.姓（首字母大写）

![centos 6.4安装教程](http://www.it165.net/uploadfile/2013/0822/20130822081814825.png)

25、”Date and Time” 选中 “Synchronize data and time over the network”

Finsh之后系统将重启

![centos 6.4安装教程](http://www.it165.net/uploadfile/2013/0822/20130822081816791.png)

26、第一次登录，登录前不要做任何更改，这个很重要！！！登录之后紧接着退出

第二次登录，选择语言，在红色区域选择下拉小三角，选other，选中“汉语（中国）”

![centos 6.4安装教程](http://www.it165.net/uploadfile/2013/0822/20130822081818379.png)

![centos 6.4安装教程](http://www.it165.net/uploadfile/2013/0822/20130822081821997.png)

27、登录之后，请一定按照如下顺序点击！

至此，CentOS安装完成，如有其他问题，请随时与我联系！！

![centos 6.4安装教程](http://www.it165.net/uploadfile/2013/0822/20130822081823746.png)



### from murongqingqqq ： 

### 备注：联想Y460路过，只是使用的是U盘安装

在安装的时候有一些不同：

1，进入安装界面的时候，选择的是第一个：

Install or upgrade an existing system --- 安装或升级现有的系统

因为我安装使用第二个（install system with basic video driver）的时候，安装完成之后，分辨率不对。

2，在进行(16、引导程序安装位置)选项的时候，由于我的U盘被识别为sda4，硬盘被识别为sdbX，所以在这里需要设置(Change device)

设置为root相关的分区(vg0_lv1_root)即可