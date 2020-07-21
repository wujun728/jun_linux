---
layout: post
title: Spring Boot 2(一)：【重磅】Spring Boot 2.0权威发布
category: springboot
tags: [springboot]
excerpt: 有哪些新特性值得我们关注
keywords: Spring Boot,Spring Boot2.0,发布,Spring Boot 2.0新特性
---

就在今天Spring Boot`2.0.0.RELEASE`正式发布，今天早上在发布Spring Boot2.0的时候还出现一个小插曲，将Spring Boot2.0同步到Maven仓库的时候出现了错误，然后Spring Boot官方又赶紧把 GitHub 上发布的 v2.0.0.RELEASE 版本进行了撤回。到了下午将问题修复后，又重新进行了上传，至此Spring Boot2.0正式推出！

要知道这是Spring Boot1.0发布4年之后第一次重大修订，因此有多的新功能和特性值得大家期待！在Spring Boot官方博客中我们了解到：Spring Boot2.0版本经历了 17 个月的开发，有 215 个不同的使用者提供了超过 6800 次的提交，并表示非常感谢提供贡献的每一位用户，和所有对这些里程碑版本提供重要反馈的早期采用者。

熟悉Spring Boot/Cloud的技术者们都知道，Spring Boot依赖于Spring，而Spring Cloud又依赖于Spring Boot，因此Spring Boot2.0的发布正式整合了Spring5.0的很多特性，同样后面Spring Cloud最新版本的发布也需要整合最新的Spring Boot2.0内容。

![](http://www.itmind.net/assets/images/2018/springboot/new.jpg)

## 新版本特性

新版本值得关注的亮点有哪些：

**基于 Java 8，支持 Java 9**

也就是说Spring Boot2.0的最低版本要求为JDK8，据了解国内大部分的互联网公司系统都还跑在JDK1.6/7上，因此想要升级到Spring Boot2.0的同学们注意啦，同时支持了Java9，也仅仅是支持而已。

**响应式编程**

使用 Spring WebFlux/WebFlux.fn提供响应式 Web 编程支持， Webflux 是一个全新的非堵塞的函数式 Reactive Web 框架，可以用来构建异步的、非堵塞的、事件驱动的服务，在伸缩性方面表现非常好，此功能来源于Spring5.0。

Spring Boot2.0也提供对响应式编程的自动化配置，如：Reactive Spring Data、Reactive Spring Security 等

**HTTP/2支持**

在Tomcat, Undertow 和 Jetty 中均已支持 HTTP/2

**对Kotlin支持**

引入对 Kotlin 1.2.x 的支持，并提供了一个 runApplication 函数，让你通过惯用的 Kotlin 来运行 Spring Boot 应用程序。

**全新的执行器架构**

全新的执行器架构，支持 Spring MVC, WebFlux 和 Jersey

**支持 Quartz**

Spring Boot1.0并没有提供对 Quartz 的支持，之前出现了各种集成方案，Spring Boot2.0给出了最简单的集成方式。

**Security**

大大的简化了安全自动配置

**Metrics**

Metrics 方面，Spring Boot 2引入了Micrometer，来统一metrics的规范，使得开发人员更好的理解和使用metrics的模块，而不需要关心对接的具体存储是什么。

**监控方面**

Spring Boot 2 增强了对 Micrometer 的集成。RabbitMQ、JVM 线程和垃圾收集指标会自动进行 instrument 监控，异步控制器(controller)也会自动添加到监控里。通过集成，还可以对 InfluxDB 服务器进行监控。

**数据方面**

- db方面，默认引入了HikariCP，替代了之前的tomcat-pool作为底层的数据库连接池， 对比于tomcat-pool， HikariCP拥有更好的性能，总而言之就是提高了db的访问速度  
- JOOQ的支持
- Redis方面， 默认引入了Lettuce, 替代了之前的jedis作为底层的redis链接方式
- MongoDB\Hibernate优化

**Thymeleaf 3**

Spring Boot 2支持了Thymeleaf 3，Thymeleaf 3相对于Thymeleaf 2性能提升可不是一点点，因为2.0的性能确实不咋地，同时也使用了新的页面解析系统。

**OAuth 2.0**

同时也加入了 对于OAuth 2.0的支持， 使得开发人员更加友好的使用spring-security来完成权限模块的开发

**依赖组件的更新**

- Jetty 9.4
- Tomcat 8.5
- Flyway 5
- Hibernate 5.2
- Gradle 3.4
- Thymeleaf 3.0


> 最后还有一个小彩蛋，Spring Boot2.0支持了动态gif的启动logo打印.


## 技术名词解释

Spring 现在作为Java开源界的老大，它的一举一动都影响着行业的技术方向，在这次发布的 Release Notes中发现有很多的技术都还没有了解过，也分享出来：

**WebFlux 是什么？**

WebFlux 模块的名称是 spring-webflux，名称中的 Flux 来源于 Reactor 中的类 Flux。Spring webflux 有一个全新的非堵塞的函数式 Reactive Web 框架，可以用来构建异步的、非堵塞的、事件驱动的服务，在伸缩性方面表现非常好。

非阻塞的关键预期好处是能够以小的固定数量的线程和较少的内存进行扩展。在服务器端 WebFlux 支持2种不同的编程模型：
- 基于注解的 @Controller 和其他注解也支持 Spring MVC
- Functional 、Java 8 lambda 风格的路由和处理

![](http://www.itmind.net/assets/images/2018/springboot/webflux.jpg)

默认情况下，Spring Boot 2使用Netty WebFlux，因为Netty在异步非阻塞空间中被广泛使用，异步非阻塞连接可以节省更多的资源，提供更高的响应度。通过比较Servlet 3.1非阻塞I / O没有太多的使用，因为使用它的成本比较高，Spring WebFlux打开了一条实用的通路。

值得注意的是：支持reactive编程的数据库只有MongoDB, redis, Cassandra, Couchbase 


**HTTP/2**

相比 HTTP/1.x，HTTP/2 在底层传输做了很大的改动和优化：

- HTTP/2 采用二进制格式传输数据，而非 HTTP/1.x 的文本格式。二进制格式在协议的解析和优化扩展上带来更多的优势和可能。
- HTTP/2 对消息头采用 HPACK 进行压缩传输，能够节省消息头占用的网络的流量。而 HTTP/1.x 每次请求，都会携带大量冗余头信息，浪费了很多带宽资源。头压缩能够很好的解决该问题。
- 多路复用，直白的说就是所有的请求都是通过一个 TCP 连接并发完成。HTTP/1.x 虽然通过 pipeline 也能并发请求，但是多个请求之间的响应会被阻塞的，所以 pipeline 至今也没有被普及应用，而 HTTP/2 做到了真正的并发请求。同时，流还支持优先级和流量控制。
- Server Push：服务端能够更快的把资源推送给客户端。例如服务端可以主动把 JS 和 CSS 文件推送给客户端，而不需要客户端解析 HTML 再发送这些请求。当客户端需要的时候，它已经在客户端了。

**JOOQ**

JOOQ 是基于Java访问关系型数据库的工具包。JOOQ 既吸取了传统ORM操作数据的简单性和安全性，又保留了原生sql的灵活性，它更像是介于 ORMS和JDBC的中间层。对于喜欢写sql的码农来说，JOOQ可以完全满足你控制欲，可以是用Java代码写出sql的感觉来。

**Lettuce**

Lettuce是一个可伸缩的线程安全的Redis客户端，用于同步，异步和反应使用。 多个线程可以共享同一个RedisConnection。它利用优秀netty NIO框架来高效地管理多个连接。 支持先进的Redis功能，如Sentinel，集群，流水线，自动重新连接和Redis数据模型。

国内使用Jedis的居多，看来以后要多研究研究Lettuce了。

**HikariCP**

HikariCP是一个高性能的JDBC连接池。Hikari是日语“光”的意思。可能是目前java业界最快的数据库连接池。

**Flyway**    

Flyway是独立于数据库的应用、管理并跟踪数据库变更的数据库版本管理工具。用通俗的话讲，Flyway可以像SVN管理不同人的代码那样，管理不同人的sql脚本，从而做到数据库同步。

**Gson**

Gson 是google解析Json的一个开源框架,同类的框架fastJson,JackJson等等

> 看完 Spring Boot 2.0 Release Notes ，发现又有很多不知道的新技术了，以后有的学了


## 是否选择升级

通过以上内容可以看出Spring Boot2.0相对于1.0增加了很多新特性，并且最重要的是Spring Boot2.0依赖的JDK最低版本是1.8，估计国内大多互联网公司还么这么激进。另外一个新的重大版本更新之后，难免会有一些小Bug什么的，往往需要再发布几个小版本之后，才会慢慢稳定下来。

因此我的建议是，如果不是特别想使用Spring Boot2.0上面提到的新特性，就尽量不要着急进行升级，等Spring Boot2.0彻底稳定下来后再使用。如果想要升级也请先从早期的版本升级到Spring Boot1.5X系列之后，再升级到Spring Boot2.0版本，Spring Boot2.0的很多配置内容和Spring Boot1.0不一致需要注意。

**Spring Boot1.0发布之后给我们带来了全新的开发模式，Spring Boot2.0发布标志着Spring Boot已经走向成熟，对Java界带来的变革已经开启！**


## 写在最后

前两天在看池建强老师文章时，发现老师刚好也介绍了Spring Boot2.0，其中有这么一个观点：Java 语言为什么能够长期占据编程兵器排行榜第一名的位置呢？因为命好。

> Java 能长盛不衰，主要是命好。每当人们觉得 Java 不行了的时候，总会有英雄横刀救美。

> 最初 Java 开发出来不知道有什么用的时候，发现可以用 Applet 在网页上做动画。后来企业级软件开发时代 JavaEE 大行其道，开源社区 Spring 桃李满天下。等到了移动时代，人们觉得 Java 要完蛋了，Google 拍马救市，收购并开放了 Android 平台，当家语言就是 Java，于是 Java 再次焕发勃勃生机。目前大数据领域，Java 同样是当仁不让的好手。

> 现在 Spring Framework 那套东西使用了十几年，正当大家被长达几千行的 ApplicationContext 配置文件折磨的死去活来的时候，Spring Boot 诞生了。什么是 Spring Boot？用来简化 Spring 应用程序开发的。

> 换句话说就是，当你觉得 Java 不好用的时候，我做了个轻量级的 S，让你好好用 Java。等你觉的 S 也不够轻了，我做了个 SB，让你觉得 S 还是挺轻的。

从2002年Rod Johnson的`interface21`到如今的`Spring Boot2.0`，Spring 走过了16年的春秋，经历了N多的贡献者，Spring 也从一个小小的开源框架，发展成Java领域最成功的开源软件没有之一！同时做为一名Java开发从业者，也特别的感谢Spring这类的开源组织，为推动企业级开发做了巨大的贡献，全世界的Java开发者都是它的受益者！

![](http://www.itmind.net/assets/images/2018/life/spring.jpg)

**向Spring致敬，向开源致敬！**

[点我了解更多Spring Boot系列文章](http://www.ityouknow.com/spring-boot.html)

## 参考

[Spring Boot 2.0 Release Notes](https://github.com/spring-projects/spring-boot/wiki/Spring-Boot-2.0-Release-Notes)  
[Spring Boot 2.0 goes GA](https://spring.io/blog/2018/03/01/spring-boot-2-0-goes-ga)    
[​Spring Boot 2.0 同步至 Maven 仓库出错，已撤回……](https://www.oschina.net/news/93772/spring-boot-2-0-released-not-yet)   

