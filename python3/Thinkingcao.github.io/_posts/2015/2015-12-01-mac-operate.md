---
layout: post
title: mac 常用操作
category: other
tags: [other]
---

## 1、shell命令下载

linux终端上面 执行sz操作后，文件目录

``` shell
/Users/neo/Documents/
```

## 2、如何强制退出Mac 应用

1）从苹果() 菜单中选取“强制退出”，或按下Command-Option-Esc。 这类似于在PC 上按下Control-Alt-Delete。

2）在“强制退出”窗口中，选择该应用，然后点按“强制退出”。

## 3、如何强制删除Mac应用

前往/go 前往“应用程序”,选择需要删除的应用 快捷键command+delete或者拖到垃圾箱


## 4、mac安装不同版本jdk，已经命令切换到不同版本

[jdk下载地址](http://www.oracle.com/technetwork/java/javase/downloads/index.html)

安装完之后，jkd 在 /Library/Java/JavaVirtualMachines 目录下

打开~/.bash_profile，没有的话创建 

``` shell
vim ~/.bash_profile 
```

``` shell
export JAVA_7_HOME=/Library/Java/JavaVirtualMachines/jdk1.7.0_80.jdk/Contents/Home
export JAVA_8_HOME=/Library/Java/JavaVirtualMachines/jdk1.8.0_144.jdk/Contents/Home

alias jdk7="export JAVA_HOME=$JAVA_7_HOME" #编辑一个命令jdk8，输入则转至jdk1.7
alias jdk8="export JAVA_HOME=$JAVA_8_HOME" #编辑一个命令jdk8，输入则转至jdk1.8

export JAVA_HOME=`/usr/libexec/java_home`  #最后安装的版本，这样当自动更新时，始终指向最新版本
```

验证 

``` shell
#使配置文件生效
. .bash_profile
jdk8
java  -version
jdk7
java -version
```

执行jdk7就会切换到jdk7的环境，输入jdk8就会切入到jdk8的环境。





