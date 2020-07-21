---
layout: post
title: Spring Boot 2 (九)：【重磅】Spring Boot 2.1.0 权威发布
category: springboot
tags: [springboot]
excerpt: 有哪些新特性值得我们关注
keywords: Spring Boot,Spring Boot 2.1,发布,Spring Boot 2.1 新特性
---

如果这两天登录 [https://start.spring.io/](https://start.spring.io/) 就会发现，Spring Boot 默认版本已经升到了 2.1.0。这是因为 Spring Boot 刚刚发布了 2.1.0 版本，我们来看下 Spring Boot 2 发布以来第一个子版本都发布了哪些内容？

## 2.1 中的新特性

- 将`spring-boot-starter-oauth2-oidc-client`重命名为`spring-boot-starter-oauth2-client`命名更简洁
- 添加 OAuth2 资源服务 starter，OAuth2 一个用于认证的组件。
- 支持 `ConditionalOnBean` 和 `ConditionalOnMissingBean` 下的参数化容器
- 自动配置 applicationTaskExecutor bean 的延迟加载来避免不必要的日志记录
- 将 DatabaseDriver＃SAP 重命名为 DatabaseDriver
- 跳过重启器不仅适用于 JUnit4，也适用于 JUnit5
- 在 Jest HealthIndicator 中使用集群端点
- 当 DevTools 禁用重启时添加日志输出
- 添加注解：`@ConditionalOnMissingServletFilter`提高 Servlet Filters 的自动装配。


同时还有一大堆以来组件进行了升级:

## 2.1 中的组件升级

- 升级 Hibernate 5.3，Hibernate 的支持升级到了 5.3
- 升级 Tomcat 9 ，支持最新的 tomcat 9
- 支持 Java 11，Java 现在更新越来越快，Spring 快赶不上了。
- 升级 Thymeleaf Extras Springsecurity 到 3.0.4.RELEASE ，`thymeleaf-extras-springsecurity` 是 Thymeleaf 提供集成 Spring Security 的组件
- 升级 Joda Time  2.10.1，Joda-Time， 面向 Java 应用程序的日期/时间库的替代选择，Joda-Time 令时间和日期值变得易于管理、操作和理解。
- 升级 Lettuce  5.1.2.RELEASE ，Lettuce 前面说过，传说中 Redis 最快的客户端。
- 升级 Reactor Californium-SR2 ，Californium 是物联网云服务的 Java COAP 实现。因此，它更专注的是可扩展性和可用性而不是像嵌入式设备那样关注资源效率。不过，Californium 也适合嵌入式的 JVM。
- 升级 Maven Failsafe Plugin 2.22.1 ，Maven 中的测试插件。
- 升级 Flyway 5.2.1 ， Flyway是一款开源的数据库版本管理工具
- 升级 Aspectj 1.9.2 ，AspectJ 是 Java 中流行的 AOP（Aspect-oriented Programming）编程扩展框架，是 Eclipse 托管给 Apache 基金会的一个开源项目。
- 升级 Mysql 8.0.13 ，Mysql 支持到 8。
- 升级 Undertow 2.0.14.Final ， Undertow 是一个用 java 编写的、灵活的、高性能的 Web 服务器，提供基于 NIO 的阻塞和非阻塞A PI。
- 升级 Rxjava2 2.2.3 ，RxJava是一个在 Java 虚拟机上的响应式扩展：一个用于通过使用可观察序列来编写异步和基于事件的程序的库。
- 升级 Hazelcast 3.11 ，Hazelcast 是一个开源的可嵌入式数据网格（社区版免费，企业版收费）。你可以把它看做是内存数据库，不过它与 Redis 等内存数据库又有些不同。
- 升级 Spring Kafka 2.2.0.RELEASE ，Kafka 高吞吐量、内置分区、支持数据副本和容错的 消息中间件。
- 升级 Spring Batch 4.1.0.RELEASE ，Spring 的批处理框架。
- 升级 Micrometer 1.1.0 ，Micrometer 是一款监控指标的度量类库，可以让您在没有供应商锁定的情况下对JVM 的应用程序代码进行调整。
- 升级 Spring Integration 5.1.0.RELEASE，Spring integration，它是一种便捷的事件驱动消息框架。
- 升级 Spring Data Lovelace SR2 ，**网上查了一下，仍然不知道 Spring Data Lovelace 是什么鬼，了解的朋友留言给我**
- 升级 Spring Framework 5.1.2.RELEASE ，对于的 Spring 也进行了升级。
- 升级 Byte Buddy 1.9.3 ，Byte Buddy 是一个字节码生成与维护的库,主要用于在 Java 应用运行时生成和修改 Java 类,并且不需要编译器来辅助。
- 升级 Spring Session Bean-RELEASE ，Spring 提供 Session 管理的组件。

详细内容参考这里：[Spring Boot 2.1 Release Notes](https://github.com/spring-projects/spring-boot/wiki/Spring-Boot-2.1-Release-Notes)

**每次看 Spring Boot 发布指南都要更新一遍脑子里面的技术名词，Spring Boot 体系太大，几乎集成了 Java 领域所有知名框架。**

我在 [Spring Boot 2.0 升级的时候说过一段话](https://gitbook.cn/gitchat/column/5b86228ce15aa17d68b5b55a/topic/5b968861780fdb5e97d3e157)：

> Spring Boot 2.0 是历时 4 年开发出来的巨作，在 Spring Boot 1.0 的基础上进行了大量的优化，淘汰了很多过期的 API，同时引入了一大批最新的技术，这些新技术在未来的一段时间内都具有引导性。

> 如果不是特别需要使用 Spring Boot 2.0 上面提到的新特性，就尽量不要着急进行升级，等 Spring Boot 2.0 彻底稳定下来后再使用。如果想要升级也请先从早期的版本升级到 Spring Boot 1.5X 系列之后，再升级到 Spring Boot 2.0 版本，Spring Boot 2.0 的很多配置内容和 Spring Boot 1.0 不一致需要注意。

这是因为 Spring Boot 2.0 刚刚发布会有一段时间的稳定期，现在 Spring Boot 2.1.0 的发布，意味着 Spring Boot 2.0 已经彻底稳定下来，如果公司比较喜欢尝新，现在可以大胆的使用了。

[另外我在 GitChat 的课程《精通 Spring Boot 42 讲》也会基于最新的 Spring Boot 2.1.0，大家感兴趣可以关注](https://gitbook.cn/gitchat/column/5b86228ce15aa17d68b5b55a#catalog)






