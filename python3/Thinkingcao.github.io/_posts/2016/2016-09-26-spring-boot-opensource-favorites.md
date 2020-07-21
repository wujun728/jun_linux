---
layout: post
title: springboot实战：我们的第一款开源软件
category: springboot
tags: [云收藏]
---

在信息爆炸时代，如何避免持续性信息过剩，使自己变得专注而不是被纷繁的信息所累？每天会看到各种各样的新闻，各种新潮的技术层出不穷，如何筛选出自己所关心的？

各位看官会想，我们是来看开源软件的，你给我扯什么信息干嘛，别着急，听我慢慢道来。

##  背景

浏览器收藏夹应该是我们在收藏文章、网站的第一个利器，平时遇到喜欢的网站或者文章很方便的收藏到收藏夹中；很快我们的收藏夹就满了，于是就像我这样,创建文件夹来分组两层、三层都有：

![favorites_chrome](http://www.ityouknow.com/assets/images/2016/favorites_chrome.jpg)  


有的也会借助百度首页导航这样的一些功能来整理自己收藏的网站，以前我记得QQ还有一款产品叫做网络收藏夹，用过一段时间，后来QQ也把这款产品给淘汰了；也尝试了去用印象笔记、有道笔记这些产品，这些产品都偏向收藏一些具体的文章或者自己整理的日志信息方面。

当浏览器收藏夹收藏的网站或者文章在一百份以内的时候收藏和查找问题都不是特别大。当收藏大于1000份的时候，去查找自己收藏的内容绝对是个体力活，另外还有一些文章我仅仅只是暂时保存下来，准备随后找时间看看就行，也需要收藏、整理、删除的时候就很麻烦。

## 产品介绍

于是在这样的背景下，我就想着需要做这么一款产品，可以方便随时随地的收藏我喜欢的文章或者网站，方便整理，我日后需要的时候非常方便的去检索，另外如果可以的话，我是否可以分享我自己收藏的文章或者网站，同时也可以看看大牛们或者是同行都收藏了什么文章我是否感兴趣，于是就开发了这么一款产品:**云收藏**

核心功能点：

- 收藏、分类、检索文章
- 导出、导出（包活从浏览器中）
- 可以点赞、分享、讨论
- 注册、登录、个人账户
- 临时收藏、查看别人收藏
- 其它...

放产品一些截图:

主页  
![favorites_chrome](http://www.ityouknow.com/assets/images/2016/favorites_index.png)  

注册  
![favorites_chrome](http://www.ityouknow.com/assets/images/2016/favorites_register.png)  

首页  
![favorites_chrome](http://www.ityouknow.com/assets/images/2016/favorites_home.png)  

收藏  
![favorites_chrome](http://www.ityouknow.com/assets/images/2016/favorites_collect.png)  


## 技术点

这段时间我们团队主要在学习spring boot,这个开源项目也就成了我们的练习新技术的一个非常好的产品，主要的技术都是和spring boot相关，可以参考我以前文章 [spring boot系列文章](http://www.ityouknow.com/spring-boot.html)

### 网页端

[网页端收藏夹主页](https://cloudfavorites.github.io/favorites-web/)

**收藏快捷图标**

 这个是收藏的最关键一步，一段js代码，拖入到浏览器的收藏夹，每次点击收藏的时候负责读取网站的title、描述、网址等信息，并且提交到收藏的页面


**前端**

前端页面由[Angle - Bootstrap Admin theme](https://wrapbootstrap.com/theme/angle-bootstrap-admin-template-WB04HF123)这套主题改造而来;模版引擎使用了```thymeleaf```，可以参考这篇文章：[springboot(四)：thymeleaf使用详解](http://www.ityouknow.com/springboot/2016/05/01/spring-boot-thymeleaf.html)
 
**持久层**

数据库主要使用了 Spring data jpa模版来实现，可以参考这篇文章：[springboot(五)：spring data jpa的使用](http://www.ityouknow.com/springboot/2016/08/20/spring-boo-jpa.html)

**session**

session使用持久化技术来保存登录状态，登录一次保持需要会话30天，主要是依赖redis来实现，参考：[springboot(三)：Spring boot中Redis的使用](http://www.ityouknow.com/springboot/2016/03/06/spring-boot-redis.html)

**其它**

使用```grade```做为项目的构建工具、使用了一点```webjars```、```vuejs```、```Jsoup```、```Scheduled``` ...


### 客户端

客户端技术使用react native来开发安卓和IOS的app，目前还在开发中，完成之后也会开源出来。


## 未来计划做的内容

这个开源产品暂时只是开源了我们web端产品，安卓端、IOS端内容的开发还在进行中。

未来我们还会持续的来完善这些产品，做一些有意思的小功能，以下可能是我们近期准备要做的

- 可以自定义个人收藏页面
- 无登录可以查看热门收藏内容
- 首页展示热门收藏家
- 小纸条
- 智能推荐
- 其它...

大家有什么更好玩想法，也可以在建议给我们


**产品主页**  

[产品地址](http://favorites.ren/)  
[源码地址](https://cloudfavorites.github.io/favorites-web/)


**[示例代码-github](https://github.com/cloudfavorites/favorites-web)**

**[示例代码-码云](https://gitee.com/ityouknow/favorites-web)**


-------------

**作者：纯洁的微笑**  
**出处：[http://www.ityouknow.com/](http://www.ityouknow.com/)**    
**版权所有，欢迎保留原文链接进行转载：)**