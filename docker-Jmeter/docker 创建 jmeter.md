我们都知道，jmeter 可以做接口测试，也可以用于性能测试，现在企业中性能测试也大多使用 jmeter。docker 是最近这些年流行起来的容器部署工具，可以创建一个容器，然后把项目放到容器中，就可以构建出一个独立的运行环境。

所以，有人就想，能否把他们俩弄到一块来使用？

今天，我就来给大家讲讲如何结合起来使用。

首先，选择一个 Linux 机器，安装 docker

用 docker 创建 jmeter 容器(普通 jmeter)
从 nmb-jmeter-docker: 使用 docker 运行 jmeter 进行测试上下载代码，到 Linux 机器的/opt 路径下

进入 base-jmeter-docker 文件夹

执行 sh build.sh, 构建本地 jmeter 镜像

默认版本是 jmeter5.1.1

待构建成功之后，把用 jmeter 创建的 jmx 脚本文件，上传到 Linux 机器的 base-jmeter-docker 路径下，执行

  sh jmeter.sh -n -t YouJMX_file \ 
-l JTL_date +%Y%m%d_%H%M%S.jtl \ 
-j jmeter.log \ 
-e -o Report_date +%Y%m%d_%H%M%S
1
2
3
4
也可以把你的 jmx 文件上传到其他路径，在运行 jmeter.sh 命令时，指定 jmx 文件路径

这个命令和 jmeter 的 CLI 模式命令是一样的，cli 的相关参数也是可以使用。

创建增强型 jmeter 容器(jmeter 带插件)
下载【jpgc-jmeter-docker】文件夹中所有文件
构建本地镜像：sh build.sh
使用构建的镜像，运行 jmx 文件
  sh jmeter.sh -n -t YouJMX_file \ 
-l YouJTL_date +%Y%m%d_%H%M%S.jtl \ 
-j jmeter.log \ 
-e -o report_date +%Y%m%d_%H%M%S
1
2
3
4
默认 jmeter 版本为 5.1.1

如果想要更改为其他版本，依次修改：Dockerfile、build.sh、jmeter.sh 文件中的版本号 5.1.1

注意： 请不要指定为低于 5 的版本，低于 5，生产的 HTML 报告可能有问题

在这个版本，改造了 HTML 报告和引入了 jpgc 插件，如果你还想要引入其他插件，可以自己打包压缩到 JmeterPlugins-jpgc.zip 文件包中。然后，执行 sh build.sh 构建新的镜像，

创建分布式 jmeter 容器(slave)
做性能测试，一般都会遇到 jmeter 不能产生足够数量的并发用户数，需要使用分布式来创建足够数量的并发用户数，但是，现实中，我们可能又不能获得足够数量的电脑。

使用 docker 创建 jmeter 的助攻服务，这样就能实现，理论上一台电脑上创建出任意多个 jmeter 助攻服务，产生出足够量的并发用户数。另外，在助攻机的维护上，也变的更加简单，因为所有的助攻机容器都是基于相同的镜像创建，理论上，所有容器都是一样。

下载【slave-jmeter-docker】文件夹中所有文件
构建本地 slave 镜像：sh build.sh
创建 slave 容器
  docker run -itd --name slave1 nmb/jmeter-slave:5.1.1 server

# 重复执行时，修改容器名称name值，则可创建多个slave容器
1
2
3
默认 jmeter 版本为 5.1.1

如果想要更改为其他版本，依次修改：Dockerfile、build.sh 文件中的版本号 5.1.1

注意：

1、该镜像中，加入 jpgc 插件，更改了 HTML 报告模板

2、请不要指定为低于 5 的版本，低于 5，生产的 HTML 报告可能有问题

3、助攻服务端口 1099， 5000， 因为后面 master 用 link 连接容器，所以，可以不用映射端口

想要创建多个 slave 容器，只需要修改创建容器命令中的指定的容器名称。

每个助攻服务的端口都是 1099 和 5000，如果直接映射到宿主机上，肯定会出现端口冲突的情况，所以，我们用 master 连接 link 每个 slave 容器，就不用担心端口冲突问题了。

创建分布式 jmeter 容器(master)
下载【master-jmeter-docker】文件夹中所有文件
构建本地 master 镜像：sh build.sh
修改 run-master.sh 文件中 --link 的数量和名称
冒号前面为 slave 容器名称，冒号后面为自定义别名

使用 master 容器执行分布式脚本

  sh run-master.sh -n \ 
-R 助攻机别名(多个时用逗号分隔) \ 
-t YouJMXfile \ 
-l YouJTL_date +%Y%m%d_%H%M%S.jtl \ 
-j jmeter.log \ 
-e -o report_date +%Y%m%d_%H%M%S
1
2
3
4
5
6
默认 jmeter 版本为 5.1.1

如果想要更改为其他版本，依次修改：Dockerfile、build.sh 文件中的版本号 5.1.1

注意： 请不要指定为低于 5 的版本，低于 5，生产的 HTML 报告可能有问题

注意：
该镜像构建成功后，会带有 jpgc 插件，可以执行使用 jpgc 插件编写的脚本
该镜像还对 jmeter 生产的 HTML 报告进行了改造，生产的报告将转换为中文
jmeter 分布式，主控和助攻机的 jmeter 必须一致，所以，master 和 slave 的 jmeter 版本务必一致
好了使用 docker 来创建 jmeter 进行性能测试的技术，已经讲完了，代码已经开源到 gitee。
————————————————
版权声明：本文为CSDN博主「爱吃 香菜」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/wx17343624830/article/details/125212133