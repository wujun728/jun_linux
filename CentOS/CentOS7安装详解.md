# [CentOS7安装详解](https://www.cnblogs.com/wcwen1990/p/7630545.html)

本文基于vmware workstations进行CentOS7安装过程展示，关于vmware workstations安装配置本人这里不再介绍，基本过程相当于windows下安装个软件而已。

1、打开vmware workstations，文件->新建虚拟机，出现如下界面，选择“自定义（高级）”选项，下一步继续：

[![wps7D66.tmp](https://images2017.cnblogs.com/blog/669905/201710/669905-20171006071737818-372983880.jpg)](http://images2017.cnblogs.com/blog/669905/201710/669905-20171006071736802-1906225668.jpg)

2、此步骤默认，下一步继续：

[![wps7D67.tmp](https://images2017.cnblogs.com/blog/669905/201710/669905-20171006071739833-72059645.jpg)](http://images2017.cnblogs.com/blog/669905/201710/669905-20171006071738818-1553699584.jpg)

3、在出现下面界面，选中“稍后安装操作系统”选项，下一步继续：

[![wps7D68.tmp](https://images2017.cnblogs.com/blog/669905/201710/669905-20171006071741927-1547834409.jpg)](http://images2017.cnblogs.com/blog/669905/201710/669905-20171006071740880-1902912328.jpg)

4、在出现如下界面，客户机操作系统选择“linux”，版本选择“CentOS 64位”，下一步继续：

[![wps7D78.tmp](https://images2017.cnblogs.com/blog/669905/201710/669905-20171006071743896-688396999.jpg)](http://images2017.cnblogs.com/blog/669905/201710/669905-20171006071742943-1597915319.jpg)

5、出现如下界面，输入自定义虚拟机名称，虚拟机名称最好能做到望文生义，这里是“CentOS7_CDH_bd06”，指定虚拟机位置，这里是“D:\Virtual Machines\CentOS7_CDH_bd06”，然后下一步继续：

[![wps7D79.tmp](https://images2017.cnblogs.com/blog/669905/201710/669905-20171006071745740-1381909701.jpg)](http://images2017.cnblogs.com/blog/669905/201710/669905-20171006071744818-819040062.jpg)

6、出现下面界面，选择处理器数量和每个处理器核心数量，这里分别是2和4，下一步继续：

[![wps7D7A.tmp](https://images2017.cnblogs.com/blog/669905/201710/669905-20171006071747474-735520918.jpg)](http://images2017.cnblogs.com/blog/669905/201710/669905-20171006071746646-1542985113.jpg)

7、出现如下界面，指定虚拟机占用内存大小，这里是2048M，下一步继续：

[![wps7D7B.tmp](https://images2017.cnblogs.com/blog/669905/201710/669905-20171006071749443-1312168864.jpg)](http://images2017.cnblogs.com/blog/669905/201710/669905-20171006071748505-2122025636.jpg)

8、出现如下界面，选择网络连接类型，这里选择“使用桥接网络”，各位安装虚拟机过程根据需要自行选择，安装向导中已经针对各种模式进行了比较规范的说明，这里补充说明如下：

1）使用桥接网络：虚拟机ip与本机在同一网段，本机与虚拟机可以通过ip互通，本机联网状态下虚拟机即可联网，同时虚拟机与本网段内其他主机可以互通，这种模式常用于服务器环境架构中。

2）使用网络地址转换（NAT）：虚拟机可以联网，与本机互通，与本机网段内其他主机不通。

3）使用仅主机模式网络：虚拟机不能联网，与本机互通，与本机网段内其他主机不通。

下一步继续：

[![wps7D8C.tmp](https://images2017.cnblogs.com/blog/669905/201710/669905-20171006071751490-236348975.jpg)](http://images2017.cnblogs.com/blog/669905/201710/669905-20171006071750458-129155751.jpg)

9、默认，下一步继续：

[![wps7D8D.tmp](https://images2017.cnblogs.com/blog/669905/201710/669905-20171006071753380-442859115.jpg)](http://images2017.cnblogs.com/blog/669905/201710/669905-20171006071752380-1289806342.jpg)

10、默认、下一步继续：

[![wps7D8E.tmp](https://images2017.cnblogs.com/blog/669905/201710/669905-20171006071754927-1164418288.jpg)](http://images2017.cnblogs.com/blog/669905/201710/669905-20171006071753958-2109425562.jpg)

11、默认，下一步继续：

[![wps7D8F.tmp](https://images2017.cnblogs.com/blog/669905/201710/669905-20171006071757208-1412437905.jpg)](http://images2017.cnblogs.com/blog/669905/201710/669905-20171006071756130-183445493.jpg)

12、出现下面界面，输入虚拟机磁盘大小，默认20g一般不够使用，建议设置略大一些，这里设置虚拟机磁盘大小为80G，下一步继续：

[![wps7DA0.tmp](https://images2017.cnblogs.com/blog/669905/201710/669905-20171006071759958-918371762.jpg)](http://images2017.cnblogs.com/blog/669905/201710/669905-20171006071758380-1586259999.jpg)

13、默认，下一步继续：

[![wps7DA1.tmp](https://images2017.cnblogs.com/blog/669905/201710/669905-20171006071801802-630743786.jpg)](http://images2017.cnblogs.com/blog/669905/201710/669905-20171006071800849-1024142249.jpg)

14、默认、点击“完成”结束虚拟机创建：

[![wps7DA2.tmp](https://images2017.cnblogs.com/blog/669905/201710/669905-20171006071804052-1347787670.jpg)](http://images2017.cnblogs.com/blog/669905/201710/669905-20171006071802771-27592816.jpg)

15、退出安装向导后，我们可以在虚拟机管理界面左侧栏看到刚刚创建的虚拟机，右侧栏可以看到虚拟机详细配置信息：

[![wps7DA3.tmp](https://images2017.cnblogs.com/blog/669905/201710/669905-20171006071805802-1910943490.jpg)](http://images2017.cnblogs.com/blog/669905/201710/669905-20171006071804865-524162098.jpg)

16、上图界面中点击“编辑虚拟机设置”选项，出现如下界面：

[![wps7DB3.tmp](https://images2017.cnblogs.com/blog/669905/201710/669905-20171006071808911-1235897852.jpg)](http://images2017.cnblogs.com/blog/669905/201710/669905-20171006071807161-504120480.jpg)

17、上图中需要指定“CD/DVD(IDE)”安装镜像，移除“USB控制器”、“声卡”和“打印机”，然后点击确定，按照上述设置后界面如下图所示：

[![wps7DB4.tmp](https://images2017.cnblogs.com/blog/669905/201710/669905-20171006071810740-658854816.jpg)](http://images2017.cnblogs.com/blog/669905/201710/669905-20171006071809896-1311546118.jpg)

18、点击开启虚拟机进入CentOS7操作系统安装过程：

19、虚拟机控制台出现界面，选择Install CentOS liunx 7，点击回车键继续：

[![wps7DB5.tmp](https://images2017.cnblogs.com/blog/669905/201710/669905-20171006071811599-1737746260.jpg)](http://images2017.cnblogs.com/blog/669905/201710/669905-20171006071811161-1876776252.jpg)

20、根据提示点击回车键继续：

[![wps7DC6.tmp](https://images2017.cnblogs.com/blog/669905/201710/669905-20171006071812224-484202586.jpg)](http://images2017.cnblogs.com/blog/669905/201710/669905-20171006071811943-317391416.jpg)

21、如下界面默认选择English，点击Continue继续：

[![wps7DC7.tmp](https://images2017.cnblogs.com/blog/669905/201710/669905-20171006071814396-331925083.jpg)](http://images2017.cnblogs.com/blog/669905/201710/669905-20171006071813365-1344875987.jpg)

22、CentOS7安装配置主要界面如下图所示，根据界面展示，这里对以下3个部分配置进行说明：

[![wps7DC8.tmp](https://images2017.cnblogs.com/blog/669905/201710/669905-20171006071815958-1270128155.jpg)](http://images2017.cnblogs.com/blog/669905/201710/669905-20171006071815068-1064354835.jpg)

Localization和software部分不需要进行任何设置，其中需要注意的是sofrware selection选项，这里本次采用默认值（即最小化安装，这种安装的linux系统不包含图形界面）安装，至于其他组件，待后期使用通过yum安装即可。

[![wps7DD8.tmp](https://images2017.cnblogs.com/blog/669905/201710/669905-20171006071817833-1571126874.jpg)](http://images2017.cnblogs.com/blog/669905/201710/669905-20171006071816958-1229131599.jpg)

如上图，system部分需要必须规划配置的是图中红色部分选项，即磁盘分区规划，另外可以在安装过程中修改network & host name选项中修改主机名（默认主机名为localhost.localdomain）。具体配置过程如下：

点击“installation destination”，进入如下界面，选中80g硬盘，下来滚动条到最后，选中“i will configure partitioning”，即自定义磁盘分区，最后点击左上角done进行磁盘分区规划：

[![wps7DD9.tmp](https://images2017.cnblogs.com/blog/669905/201710/669905-20171006071819990-2131929440.jpg)](http://images2017.cnblogs.com/blog/669905/201710/669905-20171006071818958-819488798.jpg)

23、CentOS7划分磁盘即在下图界面进行，这里先说明一下前期规划：

/boot：1024M，标准分区格式创建。

swap：4096M，标准分区格式创建。

/：剩余所有空间，采用lvm卷组格式创建。

规划后界面如下，点击done完成分区规划，在弹出对话框中点击“accept changs”：

[![wps7DDA.tmp](https://images2017.cnblogs.com/blog/669905/201710/669905-20171006071822099-1174518184.jpg)](http://images2017.cnblogs.com/blog/669905/201710/669905-20171006071821083-404771004.jpg)

[![wps7DDB.tmp](https://images2017.cnblogs.com/blog/669905/201710/669905-20171006071824380-203767532.jpg)](http://images2017.cnblogs.com/blog/669905/201710/669905-20171006071823271-461474199.jpg)

24、完成磁盘规划后，点击下图红框部分，修改操作系统主机名，这里修改为db06（如第二图所示），然后点击done完成主机名配置，返回主配置界面：

[![wps7DEC.tmp](https://images2017.cnblogs.com/blog/669905/201710/669905-20171006071826302-1752373087.jpg)](http://images2017.cnblogs.com/blog/669905/201710/669905-20171006071825552-285207268.jpg)

[![wps7DED.tmp](https://images2017.cnblogs.com/blog/669905/201710/669905-20171006071828115-186809784.jpg)](http://images2017.cnblogs.com/blog/669905/201710/669905-20171006071827286-533589872.jpg)

25、在下图中，其实从第24步配置开始我们就可以发现右下角“begin installtion”按钮已经从原本的灰色变成蓝色，这说明已经可以进行操作系统安装工作了，点击“begin installtion”进行操作系统安装过程。

[![wps7DEE.tmp](https://images2017.cnblogs.com/blog/669905/201710/669905-20171006071830130-184608162.jpg)](http://images2017.cnblogs.com/blog/669905/201710/669905-20171006071829130-1467864820.jpg)

26、在下图用户设置中需要做的仅是修改root用户密码，点击“root password”，设置密码，如果密码安全度不高，比如我这里的密码为“oracle”，那么可能需要点击2次确定才可以。当root密码设置成功再次返回安装界面时我们可以发现之前user setting界面红色警告消失了，对比下面图1和图3：

[![wps7DEF.tmp](https://images2017.cnblogs.com/blog/669905/201710/669905-20171006071832411-402376230.jpg)](http://images2017.cnblogs.com/blog/669905/201710/669905-20171006071831380-1984967087.jpg)

[![wps7E00.tmp](https://images2017.cnblogs.com/blog/669905/201710/669905-20171006071834536-1629166918.jpg)](http://images2017.cnblogs.com/blog/669905/201710/669905-20171006071833411-109628928.jpg)

[![wps7E01.tmp](https://images2017.cnblogs.com/blog/669905/201710/669905-20171006071836943-94074526.jpg)](http://images2017.cnblogs.com/blog/669905/201710/669905-20171006071835583-251932656.jpg)

27、在下图，操作系统安装已经完成，点击reboot重启操作系统。

[![wps7E02.tmp](https://images2017.cnblogs.com/blog/669905/201710/669905-20171006071838958-2097659848.jpg)](http://images2017.cnblogs.com/blog/669905/201710/669905-20171006071837974-1254981571.jpg)

28、使用root用户登录（即root/oracle），修改IP地址（vi /etc/sysconfig/network-scripts/ifcfg-ens32）：

[![wps7E03.tmp](https://images2017.cnblogs.com/blog/669905/201710/669905-20171006071839974-287939019.jpg)](http://images2017.cnblogs.com/blog/669905/201710/669905-20171006071839661-1313673276.jpg)

[![wps7E13.tmp](https://images2017.cnblogs.com/blog/669905/201710/669905-20171006071841083-1142062348.jpg)](http://images2017.cnblogs.com/blog/669905/201710/669905-20171006071840740-1083731854.jpg)

按字符键“i”进入编辑模式，修改/etc/sysconfig/network-scripts/ifcfg-ens32文件内容如下：

[![wps7E14.tmp](https://images2017.cnblogs.com/blog/669905/201710/669905-20171006071842990-502092640.jpg)](http://images2017.cnblogs.com/blog/669905/201710/669905-20171006071842146-723365803.jpg)

按“esc”键后，输入:wq回车，完成配置文件编辑。

输入：service network restart命令重启网卡，生效刚刚修改ip地址，ping www.baidu.com测试网络连通性。

[![wps7E15.tmp](https://images2017.cnblogs.com/blog/669905/201710/669905-20171006071845193-207653875.jpg)](http://images2017.cnblogs.com/blog/669905/201710/669905-20171006071844177-147853264.jpg)

好了，至此，CentOS7操作系统安装成功了。

 

************************************************************