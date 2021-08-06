# 快速优雅的在linux服务器上安装jdk8

2019-06-17阅读 3.7K0

> 对于开发者来说，安装jdk按理说是非常简单的事，但在linux下安装着实费了我这个一直玩windows的小白不少劲。这里简单把步骤梳理下，希望能帮助像我这样的纯小白人士少踩点坑。

这里介绍两种安装方式：

- yum安装（力荐）
- 从官网下载包安装

# **获得一台linux服务器**

要在linux下安装jdk，首先你得先有一台linux服务器，作为小白，手头的机器肯定都是windows的，搞个虚拟机安装对我这种小白简直是折磨人；这里使用最简单的方式获得一台linux服务器，就是从阿里云或者腾讯云上租一台。镜像选择CentOS7.3 64位。

![img](https://ask.qcloudimg.com/http-save/yehe-4220914/ey746ij6m5.png?imageView2/2/w/1620)

# **yum安装jdk**

在linux上使用yum安装是非常粗暴无脑的，但仍然有需要注意的点，不然会掉坑里。这里说一下步骤。

- 执行命令`yum -y list java*`查看可安装java版本。执行成功后可以看见如下的结果

![img](https://ask.qcloudimg.com/http-save/yehe-4220914/2coenbxks2.jpeg?imageView2/2/w/1620)

- 选择一个java版本进行安装，这里我们希望安装java1.8，因为我们的机器是64位的，所以选择安装**java-1.8.0-openjdk-devel.x86_64**。 这里有个地方要注意，上图中我用红框圈起来的两个java版本，要选择-devel的安装，因为这个安装的是jdk，而那个不带-devel的安装完了其实是jre。
- 执行命令`yum install -y java-1.8.0-openjdk-devel.x86_64`。执行完后会看见控制台刷出很多输出。 耐心等待至自动安装完成

![img](https://ask.qcloudimg.com/http-save/yehe-4220914/viia74jgf8.png?imageView2/2/w/1620)

- 输入`java -version`查看已安装的jdk版本，当出现如下输出表示安装成功。

![img](https://ask.qcloudimg.com/http-save/yehe-4220914/8c69ec4duv.png?imageView2/2/w/1620)

- 你可能好奇，yum安装的jdk，被安装到哪里去了？可以执行

```javascript
1rpm -ql java-1.8.0-openjdk
```

获取安装目录，你发现在`/usr/lib/jvm`目录下可以找到他们。

![img](https://ask.qcloudimg.com/http-save/yehe-4220914/fs4wvy17x3.png?imageView2/2/w/1620)

至此，yum安装jdk完成。

# **从官网下载包安装jdk**

如果你不喜欢yum安装的方式，想要使用官方提供的安装包进行传统方式的安装，可以使用如下步骤。

- 执行命令`useradd java`，新建用户java

![img](https://ask.qcloudimg.com/http-save/yehe-4220914/l6kdi08sds.png?imageView2/2/w/1620)

- 执行命令`passwd java`，设置java用户密码

![img](https://ask.qcloudimg.com/http-save/yehe-4220914/xmqqsbrzxo.png?imageView2/2/w/1620)

- 进入oracle官网，java8下载页面http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html。

![img](https://ask.qcloudimg.com/http-save/yehe-4220914/pe4roy3kzf.jpeg?imageView2/2/w/1620)

- 选择**Accept License Agreement**，点击**jdk-8u131-linux-x64.tar.gz**，获取到下载链接。注意，获取到的下载链接有时效（具体有效多久不清楚，反正隔天肯定不能用），请尽快复制到linux上进行下载。
- 进入到`/home/java`目录下，输入wget +地址，即可开始下载

![img](https://ask.qcloudimg.com/http-save/yehe-4220914/rhu989gbus.jpeg?imageView2/2/w/1620)

- 等待下载成功

![img](https://ask.qcloudimg.com/http-save/yehe-4220914/gwi1aqztqa.png?imageView2/2/w/1620)

- 查看文件，发现下载后的文件名有奇怪的后缀，重命名下载文件

![img](https://ask.qcloudimg.com/http-save/yehe-4220914/4e7dwyf5eg.png?imageView2/2/w/1620)

- 输入命令`tar zxvf jdk-8u131-linux-x64.tar.gz`解压安装包 如果提示没有`tar`命令，输入`yum install -y tar`先安装tar。

![img](https://ask.qcloudimg.com/http-save/yehe-4220914/cbxopgjjk3.png?imageView2/2/w/1620)

- 输入命令`vim /etc/profile`，打开环境变量配置文件 在文件底部输入以下信息，并保存

```javascript
1JAVA_HOME=/home/java/jdk1.8.0_131
2JRE_HOME=$JAVA_HOME/jre
3PATH=$PATH:$JAVA_HOME/bin
4CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar
5export JAVA_HOME
6export JRE_HOME
7export PATH
8export CLASSPATH
```

- 输入命令`source /etc/profile`，刷新环境变量配置文件使其立刻生效；输入`java -version`查看已安装的jdk版本

![img](https://ask.qcloudimg.com/http-save/yehe-4220914/w55m32qiai.png?imageView2/2/w/1620)

你要以为这就完成了，那就掉坑里了。虽然大部分时候这就够了，但还有一步操作最好做一下。建一个`/usr/bin/java`的java的超链接。 `ln -s /home/java/jdk1.8.0_131/bin/java /usr/bin/java`

为什么要建这个超链接，因为一些自己注册的linux服务（如springboot的jar注册的服务），默认情况下从`/usr/bin/java`路径使用java，yum安装的时候，这个超链接会自动创建，如果你自己下载包安装的话，这个超链接就需要你手动创建了。 至此，从官网下载包安装jdk完成。