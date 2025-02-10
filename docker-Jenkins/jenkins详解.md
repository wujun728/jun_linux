# [jenkins详解](https://www.cnblogs.com/youyouxiaosheng-lh/p/11212340.html)

 

Jenkins是一个功能强大的应用程序，允许持续集成和持续交付项目，无论用的是什么平台。这是一个免费的源代码，可以处理任何类型的构建或持续集成。集成Jenkins可以用于一些测试和部署技术。Jenkins是一种软件允许持续集成。

开源的java语言开发持续集成工具，支持CI，CD。
易于安装部署配置：可通过yum安装,或下载war包以及通过docker容器等快速实现安装部署，可方便web界面配置管理。
消息通知及测试报告：集成RSS/E-mail通过RSS发布构建结果或当构建完成时通过e-mail通知，生成JUnit/TestNG测试报告。
分布式构建：支持Jenkins能够让多台计算机一起构建/测试。
文件识别:Jenkins能够跟踪哪次构建生成哪些jar，哪次构建使用哪个版本的jar等。
丰富的插件支持:支持扩展插件，你可以开发适合自己团队使用的工具，如git，svn，maven，docker等。



一、在你的本地电脑或者linux服务器上下载安装jenkins:
jenkins下载地址：https://jenkins.io/  下载网站的war包版本就好了

下载完后把它部署到你的tomcat上运行：放到tomcat的webapps目录下，启动tomcat（windows下双击startup.bat或者linux下运行sh startup.sh），然后通过浏览器访问，如我的电脑上访问：localhost:8080/jenkins 。启动后的界面如下：

 ![img](https://img2018.cnblogs.com/blog/1264752/201907/1264752-20190719113359634-1050292076.png)

 

然后到提示的文件中把里面的文本复制出来填到管理员密码中。

接着如果是在本地电脑跑，可能会出现：该jenkins实例似乎已离线 提示，如果出现，是因为本地https访问不了的原因。在浏览器中另打开一个界面http://localhost:8080/pluginManager/advanced，把升级站点中的url中的https改为http,保存更新。然后关掉tomcat服务器重启，就可以联网了。

​    接下来选择安装推荐的插件，这个需要一定的时间。最后额外推荐安装两个插件，在系统管理中可以安装插件：

1、 Rebuilder

2、 Safe Restart

 

二、在linux服务器中安装git, maven，创建一个jenkens目录，配置git的公钥到你的github上，这些步骤是使用jenkins的前提。
   安装git的目的是在自动化部署前实时从git远程仓库中拉取最新的代码。在linux(我用的是centos系统)安装git：

yum install git
   生成密钥：

ssh-keygen -t rsa -C "youremail@abc.com"
  可以不设置密钥密码直接按三次回车。 把家目录中生成的公钥内容复制到github或其他仓库上。   

  安装maven的目的是通过项目中的pom.xml文件自动解决项目依赖问题，构建项目。linux中通过wget+下载链接下载maven的zip包然后解压即可。配置maven环境变量：

vim /etc/profile

//在这个文件末尾加上
export MAVEN_HOME=/root/maven3.4.5
export PATH=$MAVEN_HOME/bin:$PATH

//保存后在命令行输入,启动配置
. /etc/profile
  创建jenkins目录，用来存储拉取下来的项目代码等。

 

三、将Linux服务器注册到Jenkins上
1、开启服务器上的ssh服务，可通过 netstat -anp | grep :22命令查看是否开启

2、先来测试一下怎么在jenkins中操作远程服务器

在jenkins中选择系统管理——》新建节点

 ![img](https://img2018.cnblogs.com/blog/1264752/201907/1264752-20190719113600246-584276434.png)

 

其中远程工作目录即你在Linux上创建的jenkins目录。在Credentials添加一个远程用户，输入你的远程机器用户名和密码保存。

![img](https://img2018.cnblogs.com/blog/1264752/201907/1264752-20190719113613774-2139001659.png)

 

点击TestEnv,启动代理。

在全局工具配置中配置git命令：

 ![img](https://img2018.cnblogs.com/blog/1264752/201907/1264752-20190719113630746-723093859.png)

 

3、自动化部署过程原理：

 ![img](https://img2018.cnblogs.com/blog/1264752/201907/1264752-20190719113639486-1634283410.png)

 

所以需要编写一个shell脚本来执行这个过程。

具体的创建Jenkins任务的过程为

1.创建jenkins任务

2.填写Server信息

3.配置git参数

4.填写构建语句（shell脚本）,实现自动部署。

 

四、创建自动化部署任务
1、编写shell部署脚本deploy.sh，并放到linux服务器中的jenkins目录下，在该目录下通过touch deploy.sh创建一个脚本，把下面的脚本复制到里面即可（到时每次自动部署都会执行它），脚本中的my-scrum为我要自动构建的项目名：

\#!/usr/bin/env bash
\#编译+部署项目站点

\#需要配置如下参数
\# 项目路径, 在Execute Shell中配置项目路径, pwd 就可以获得该项目路径
\# export PROJ_PATH=这个jenkins任务在部署机器上的路径

\# 输入你的环境上tomcat的全路径
\# export TOMCAT_APP_PATH=tomcat在部署机器上的路径

\### base 函数
killTomcat()
{
\#pid=`ps -ef|grep tomcat|grep java|awk '{print $2}'`
\#echo "tomcat Id list :$pid"
\#if [ "$pid" = "" ]
\#then
\# echo "no tomcat pid alive"
\#else
\# kill -9 $pid
\#fi
\#上面注释的或者下面的
cd $TOMCAT_APP_PATH/bin
sh shutdown.sh
}
cd $PROJ_PATH/my-scrum
mvn clean install

\# 停tomcat
killTomcat

\# 删除原有工程
rm -rf $TOMCAT_APP_PATH/webapps/ROOT
rm -f $TOMCAT_APP_PATH/webapps/ROOT.war
rm -f $TOMCAT_APP_PATH/webapps/my-scrum.war

\# 复制新的工程到tomcat上
cp $PROJ_PATH/scrum/target/order.war $TOMCAT_APP_PATH/webapps/

cd $TOMCAT_APP_PATH/webapps/
mv my-scrum.war ROOT.war

\# 启动Tomcat
cd $TOMCAT_APP_PATH/
sh bin/startup.sh
2、在jenkins上点击新建一个任务，填好任务名，填写运行的节点（上文中新建节点时创建的）：

 ![img](https://img2018.cnblogs.com/blog/1264752/201907/1264752-20190719113747258-58084675.png)

 

3、点击源码管理，填写github（或gitlab等）地址：

 ![img](https://img2018.cnblogs.com/blog/1264752/201907/1264752-20190719113754983-618345591.png)

 

4、点击add，选择check out to a sub-directory ,添加源码下载到jenkins目录下的指定目录（可以命名为你的项目名）：

![img](https://img2018.cnblogs.com/blog/1264752/201907/1264752-20190719113803459-1828680136.png)

 


5、填写构建任务时的shell脚本，然后保存，点击立即构建完成自动构建。（这里有一个坑，一定要给tomcat下所有sh文件加上x权限才能启动tomcat成功，具体为在tomcat目录上层执行chmod a+x  -R tomcat目录或者在tomcat的bin目录下执行chmod +x *.sh）

\#当jenkins进程结束后新开的tomcat进程不被杀死
BUILD_ID=DONTKILLME
\#加载变量
. /etc/profile
\#配置运行参数

\#PROJ_PATH为设置的jenkins目录的执行任务目录
export PROJ_PATH=`pwd`
\#配置tomcat所在目录
export TOMCAT_APP_PATH=/root/tomcats/tomcat-my-scrum

\#执行写好的自动化部署脚本
sh /root/jenkins/deploy.sh

![img](https://img2018.cnblogs.com/blog/1264752/201907/1264752-20190719113820146-9727451.png)

 


6、自动化构建成功：

 ![img](https://img2018.cnblogs.com/blog/1264752/201907/1264752-20190719113833856-1714559132.png)

 

7、后续代码如果有改动，只要push到github或者gitlab等上，在jenkins界面中再次执行构建任务就可以了，非常方便，自动化部署，再也不用手动上传项目到服务器了。



五、解决一个tomcat关闭，所有tomcat都被关闭了的问题（如果你的jenkins也是安装的服务器上的其中一个tomcat中，就可能被莫名杀掉）
    这是因为所有的tomcat的关闭脚本（shutdown.sh或者说catalina.sh）都默认监听的是8005端口。只要进去tomcat目录下的conf目录下的server.xml文件中，将

<Server port="8005" shutdown="SHUTDOWN">
<Listener className="org.apache.catalina.startup.VersionLoggerListener" />
<!-- Security listener. Documentation at /docs/config/listeners.html
<Listener className="org.apache.catalina.security.SecurityListener" />
-->
中的8005端口改为不同的端口，就不会一个tomcat关闭，所有的tomcat都被关闭了

六、以后可以在linux服务器中安装多个tomcat，来部署不同的项目，分别使用不同的端口，如我喜欢用8081,8082,8083等端口来解决多个tomcat端口冲突问题（在tomcat的conf目录下的server.xml中修改即可，默认为8080）。然后可以用jenkins来管理这些tomcat的自动化部署啦。

 

 

原文：https://blog.csdn.net/qq_37372007/article/details/81586751