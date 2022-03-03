# [Jenkins快速上手](https://www.cnblogs.com/puresoul/p/4813551.html)

**一、Jenkins下载安装**

1、到官网下载jenkins.war包：http://jenkins-ci.org/

2、安装方法有两种：

　　a) 把下载下来的jenkins.war包放到文件夹下,如C:\jenkins，然后打开命令行窗口并进到该目录下，执行java -jar jenkens.war命令，当提示：“Jenkins is fully up and running”时，表示启动成功，这时在浏览器窗口输入：http://localhost:8080/ 就可到jenkins的首页。

　　b) 如果有tomcat，把jenkins.war包放在tomcat的webapps文件夹下，启动tomcat时会自动启动jenkins，这时通过http://localhost:8080/jenkins就 可以访问jenkins的首页了。

3、我使用的是第一种方法，安装好后访问： http://localhost:8080

![img](https://images2015.cnblogs.com/blog/77835/201509/77835-20150916162408554-1960851946.jpg)

 

 **二、 \**Jenkins配置\****

1、修改jenkins的根目录：

　　默认地在C:\user\.jenkins ,可以通过设置环境变量来修改，例如：set JENKINS_HOME=D:\jenkins，然后重新启动jenkins。 

2、备份和恢复jenkins： 

　　只需要备份JENKINS_HOME下的所有文件和文件夹，恢复的时候需要先停止jenkins。 

3、移动，删除或修改jobs:

　　a) 移动或删除jobs：移动或删除%JENKINS_HOEM%\jobs目录。

　　b) 修改jobs的名字：修改%JENKINS_HOEM%\jobs下对应job的文件夹的名字。

　　c) 对于不经常使用的job，只需要对%JENKINS_HOEM%\jobs下对应的jobs的目录zip或tar后存储到其他的地方。 

 

***\*三\**、\**Jenkins架构(master-slave)\****

　　1、Master/Slave相当于Server和agent的概念，Master提供web接口让用户来管理job和slave，job可以运行在master本机或者被分配到slave上运行。一个master可以关联多个

slave用来为不同的job或相同的job的不同配置来服务。

　　2、在 Slave上执行JOB时，Slave需要安装可运行环境。

　　3、Slave可以是物理机也可以是虚拟机 

 

***\*四\**、管理节点(slave)**

1、点击系统管理-->管理节点-->新建节点，输入节点的名字，选中【Dumb Slave】，点击 【OK】

![img](https://images2015.cnblogs.com/blog/77835/201509/77835-20150916162943633-1079302593.jpg)

2、slave配置： 

　　a) of executors：表示在slave上可以并行执行几个线程，也可以点后面的问号看说明，一般设置为1。 

　　b) 远程工作目录：在slave上创建jenkins工作目录的路径，一般设置为D:\JK 

　　c) 标签：可以给slave加上一个或多个标签，通过标签选择slave 

　　d)启动方法：启动slave的方法，推荐选第二个Launch slave agents via Java Web Start 

![img](https://images2015.cnblogs.com/blog/77835/201509/77835-20150916163256586-1558047081.jpg)

3、设置好后，点击保存，出现在下图界面： 

![img](https://images2015.cnblogs.com/blog/77835/201509/77835-20150916164124054-493087039.jpg)

4、上面看到有三种方法可以启动slave,我们就使用第二种，在本机cmd输入：

```
　　javaws http://localhost:8080/computer/testa/slave-agent.jnlp
```

启动slave成功界面： 

![img](https://images2015.cnblogs.com/blog/77835/201509/77835-20150916164839758-576648167.jpg) ![img](https://images2015.cnblogs.com/blog/77835/201509/77835-20150916164848289-1560531419.jpg)

 

***\*五\**、配置JOB**

1、在jenkins首页点击【新建】任务的，选择【构建一个自由风格的软件项目】，输入名字后点击【OK】

2、进行JOB配置页面： 

a）Restrict where this project can be run: 创建slave时的标签就在这里用上了,用来指定这个Job在哪个标签的slave上执行
b）源码管理：推荐使用SVN，也不可选None 

![img](https://images2015.cnblogs.com/blog/77835/201509/77835-20150918144948117-918952953.jpg)

c)增加构建步骤：

　　1、Execute Windows batch commnd：这个就是windows命令行参数（默认当前路径是job的workspace，如果命令很多可以写成批处理文件放在job的工作目录下，在这引用就好）

　　2、Execute shell：运行shell、python，perl，ruby等脚本

　　3、Invoke Ant：支持Ant构建

　　4、Invoke top-level Maven targets：支持Maven构建

![img](https://images2015.cnblogs.com/blog/77835/201509/77835-20150918145632539-1829821138.jpg)

 d）增加构建后操作步骤：

　　这里有比较比的选项，可以根据自己的需要选择，常用的是发送邮件，也可以安装jenkins的插件，安装插件后这里会有相应的选项。

![img](https://images2015.cnblogs.com/blog/77835/201509/77835-20150918145735117-1614659112.jpg)

e)配置完成job后就可以保存，执行job。

 

**六、\**\*\*插件管理\*\**\***

1、点击系统管理-->管理插件，进入插件管理页面，可以选择需要的插件进行安装：

 ![img](https://images2015.cnblogs.com/blog/77835/201509/77835-20150916165923195-1717732222.jpg)

 2、选择【高级】这里可以上传插件后缀为hpi的文件，等他提示安装完成，然后重启Jenkins就可以完成安装了，插件下载地址：

　　http://mirrors.jenkins-ci.org/plugins/

 

**七、权限管理**

 未完待续...

 

 