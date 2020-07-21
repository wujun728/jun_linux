---
layout: post
title: 如何构建云收藏项目
no-post-nav: true
category: springboot 
tags: [springboot]
---

很多人github上面反馈我们的springboot开源项目无法构建，这里简单写一下构建的流程希望可以帮助到大家。

问题列表如下，Issues有好几个都是因为构建的问题：

[问题列表](https://github.com/cloudfavorites/favorites-web/issues)


我这里以idea为例，演示一下如果导入构建项目：

1、手动下载[favorites-web](https://github.com/cloudfavorites/favorites-web)代码到本地，或者通过idea的VCS功能下载到本地。

 
![](http://www.itmind.net/assets/images/2017/cloudfavorites/gradle1.png)


2、导入项目

 
![](http://www.itmind.net/assets/images/2017/cloudfavorites/gradle2.png)


 
![](http://www.itmind.net/assets/images/2017/cloudfavorites/gradle3.png)


3、选择gradle的方式导入

 
![](http://www.itmind.net/assets/images/2017/cloudfavorites/gradle4.png)


 
![](http://www.itmind.net/assets/images/2017/cloudfavorites/gradle5.png)


4、导入完成之后，选择Project Stucture查看项目依赖(最新版本已经修复，使用最新版本构建可以跳过第4、5步)


 
![](http://www.itmind.net/assets/images/2017/cloudfavorites/gradle6.png)


发现有部分的jar包级别是Provided  

 
![](http://www.itmind.net/assets/images/2017/cloudfavorites/gradle7.png)


5、将标红色部分的jar级别由Provided改为Compile(最新版本已经修复，使用最新版本构建可以跳过第4、5步)

 
![](http://www.itmind.net/assets/images/2017/cloudfavorites/gradle8.png)

修改对应的配置文件为本地配置信息，在运行Application项目便可成功启动


6、mvn导入方式

已经有网友提供了项目的mvn支持，导入方式和上面的流程相同，只是在第三步的时候选择maven既可。


 
![](http://www.itmind.net/assets/images/2017/cloudfavorites/mvn3.png)


感谢@souvc提供mvn的支持！  
感谢@shatangege提供本地化支持！