---
layout: post
title: idea使用总结
category: other
tags: [other]
---

记录idea的一些常用快捷键

## 快捷键

1、进入实现方法的快捷键

> Ctrl + Alt + B 
> > Ctrl + Alt + 鼠标点击

2、自动给方法添加注释的快捷键

> 输入/**,然后回车

3、删除一行

> CTRL + Y / CTRL + X

4、复制一行

> CTRL + D

5、自动导入包

> ALT + Enter

6、生成getter、setter方式

> ALT + insert

7、实现接口方法

> CTRL + O

8、移动整个代码块

> Ctrl + SHIfT + 上下箭头 

9、返回至上次浏览的位置

> Ctrl + ALT + 左/右

10、查找和替换

> Ctrl + SHIfT + R，替换文本
> Ctrl + SHIfT + F，查找文本

11、 debug

> Ctrl+F1 ,显示结果  
> F9 ,下一个断点
> F8 ,下一步

12、 移动代码

> Alt+Shift+Up/Down，上/下移一行

13、显示类图

> Ctrl+Shift+Alt+U


## 错误 

1、maven导入项目报错

> Failed to read artifact descriptor for org.springframework.cloud:spring-cloud-starter-eureka-server:jar:1.3.0.RELE
> intellij inspects a maven model for resolution problems


不同project下面存在相同的module,导致此问题，删除其它project中项目，再次导入OK。


2、gradle no cached version available for offline mode

> Error:No cached version of org.springframework.boot:spring-boot-gradle-plugin:1.5.4.RELEASE available for offline mode.

抱这个错误直接把gradle中的offline work关掉就可以解决  
File > Settings > Gradle 中的offline work 的勾去掉。


## 其它

1、添加插件mac

Intellij IDEA 菜单 -》Preferences-》Plugins 选项卡 



2、开启自动 import 包的功能

Java就是这种包组合在一个的一个东西, 我们在写代码时常常需要引入一些类, 一些第三方的包. 在eclipse时我们使用快捷键引入, IDEA也可以使用Alt + Enter进行导入包.

如果我们在写代码时IDE自动帮我们引入相关的包, 是不是很酷的意见事情. IDEA提供了这个功能, 不过默认是关闭的. 打开自动导入包设置如下:

 
![](http://www.itmind.net/assets/images/2015/idea-auto-import.jpg)  

