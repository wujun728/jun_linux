---
layout: post
title: springcloud(十四)：Spring Cloud 开源软件都有哪些？
category: springcloud
tags: [springcloud]
keywords: Spring Cloud,open source
---

学习一门新的技术如果有优秀的开源项目，对初学者的学习将会是事半功倍，通过研究和学习优秀的开源项目，可以快速的了解此技术的相关应用场景和应用示例，参考优秀开源项目会降低将此技术引入到项目中的成本。为此抽了一些时间为大家寻找了一些非常优秀的 Spring Cloud 开源软件供大家学习参考。

上次写了一篇文章[Spring Boot 2 (三)：Spring Boot 开源软件都有哪些](http://www.ityouknow.com/springboot/2018/03/05/spring-boot-open-source.html) 给大家介绍优秀的 Spring Boot 开源项目，本篇文章给介绍 Spring Cloud 的优秀开源项目。Spring Cloud 开源项目主要集中在 Github/码云 ，本文所有项目地址也均来自于这两个网站。

## 1、 [awesome-spring-cloud](https://github.com/ityouknow/awesome-spring-cloud)

首先给大家介绍的就是 Spring Cloud 中文索引，这是一个专门收集 Spring Cloud 相关资料的开源项目，也有对应的导航页面。

**产品主页**

[http://springcloud.fun/](http://springcloud.fun/)  

**项目主页**

[https://github.com/ityouknow/awesome-spring-cloud](https://github.com/ityouknow/awesome-spring-cloud)

**产品截图**

![](http://www.itmind.net/assets/images/2018/springcloud/awesome-spring-cloud.png)


## 2、 [PiggyMetrics](https://github.com/sqshq/PiggyMetrics)

一个简单的个人财务系统，基于 Spring Boot，Spring Cloud 和 Docker 简单演示了微服务的架构模式，整个项目几乎包含了 Spring Cloud 的所有特性包括 配置中心、Gateway zuul API 网关、Eureka 服务发现、Hystrix、Turbine仪 表盘应用健康监控等等。

PiggyMetrics 被分解为三个核心微服务。这些服务都是围绕某些业务能力组织的可独立部署的应用程序。

![](http://www.itmind.net/assets/images/2018/springcloud/PiggyMetrics_sercive.png)

PiggyMetrics 的项目架构图

![](http://www.itmind.net/assets/images/2018/springcloud/PInfrastructure.png)

**项目主页**

[https://github.com/sqshq/PiggyMetrics](https://github.com/sqshq/PiggyMetrics)

**产品截图**

![](http://www.itmind.net/assets/images/2018/springcloud/piggyMetrics.png)

## 3、 [spaascloud-master](https://github.com/paascloud/paascloud-master)

spring cloud + vue 全家桶实战，模拟商城，完整的购物流程、后端运营平台，可以实现快速搭建企业级微服务项目。

功能点：
模拟商城，完整的购物流程、后端运营平台对前端业务的支撑，和对项目的运维，有各项的监控指标和运维指标。

技术点：
核心技术为springcloud+vue两个全家桶实现，采取了取自开源用于开源的目标，所以能用开源绝不用收费框架，整体技术栈只有
阿里云短信服务是收费的，都是目前java前瞻性的框架，可以为中小企业解决微服务架构难题，可以帮助企业快速建站。由于服务
器成本较高，尽量降低开发成本的原则，本项目由10个后端项目和3个前端项目共同组成。真正实现了基于RBAC、jwt和oauth2的
无状态统一权限认证的解决方案，实现了异常和日志的统一管理，实现了MQ落地保证100%到达的解决方案。


**产品主页**

[http://mall.paascloud.net/index](http://mall.paascloud.net/index)  

**项目主页**

[https://github.com/paascloud/paascloud-master](https://github.com/paascloud/paascloud-master)

**产品截图**

![](http://www.itmind.net/assets/images/2018/springcloud/paascloud.png)


## 4、 [Cloud-Admin](https://gitee.com/minull/ace-security)

Cloud-Admin是国内首个基于Spring Cloud微服务化开发平台，核心技术采用Spring Boot2以及Spring Cloud Gateway相关核心组件，前端采用vue-element-admin组件。具有统一授权、认证后台管理系统，其中包含具备用户管理、资源权限管理、网关API管理等多个模块，支持多业务系统并行开发，可以作为后端服务的开发脚手架。代码简洁，架构清晰，适合学习和直接项目中使用。


**项目主页**

[https://gitee.com/minull/ace-security](https://gitee.com/minull/ace-security)

**项目架构**

![](http://www.itmind.net/assets/images/2018/springcloud/ace-security.png)



## 5、 [spring-cloud-rest-tcc](https://github.com/prontera/spring-cloud-rest-tcc)

基于Spring Cloud Netflix的TCC柔性事务和EDA事件驱动示例，结合Spring Cloud Sleuth进行会话追踪和Spring Boot Admin的健康监控，并辅以Hystrix Dashboard提供近实时的熔断监控.

**项目主页**

[https://github.com/prontera/spring-cloud-rest-tcc](https://github.com/prontera/spring-cloud-rest-tcc)

**项目架构**

![](http://www.itmind.net/assets/images/2018/springcloud/spring-cloud-rest-tcc.png) 


## 6、 [pig](https://gitee.com/log4j/pig)

基于Spring Cloud、oAuth2.0开发，基于Vue前后分离的开发平台，支持账号、短信、SSO等多种登录

**产品主页**

[https://www.pig4cloud.com/](https://www.pig4cloud.com/)  

**项目主页**

[https://gitee.com/log4j/pig](https://gitee.com/log4j/pig)

**产品截图**

![](http://www.itmind.net/assets/images/2018/springcloud/ping.png) 


## 7、 [xxpay-master](https://gitee.com/jmdhappy/xxpay-master)

XxPay聚合支付使用Java开发，包括spring-cloud、dubbo、spring-boot三个架构版本，已接入微信、支付宝等主流支付渠道，可直接用于生产环境。

**产品主页**

[http://www.xxpay.org/](http://www.xxpay.org/)  

**项目主页**

[https://gitee.com/jmdhappy/xxpay-master](https://gitee.com/jmdhappy/xxpay-master)

**产品截图**

![](http://www.itmind.net/assets/images/2018/springcloud/xxpay.png) 


## 8、 [spring-boot-cloud](https://github.com/zhangxd1989/spring-boot-cloud)

基于 Spring Boot、Spring Cloud、Spring Oauth2 和 Spring Cloud Netflix 等框架构建的微服务项目

**项目主页**

[https://github.com/zhangxd1989/spring-boot-cloud](https://github.com/zhangxd1989/spring-boot-cloud)

**项目架构**

![](http://www.itmind.net/assets/images/2018/springcloud/spring-boot-cloud.jpg) 


## 9、 [FCat](https://gitee.com/xfdm/FCat)

FCat项目基于 Angular 4 + Spring Cloud 的企业级基础功能框架。

**项目主页**

[https://gitee.com/xfdm/FCat](https://gitee.com/xfdm/FCat)

**项目架构**

![](http://www.itmind.net/assets/images/2018/springcloud/FCat.png) 


## 10、 [spring-cloud-examples](https://github.com/ityouknow/spring-cloud-examples)

Spring Cloud 技术栈示例代码，快速简单上手教程，一个帮助大家学习 Spring Cloud 的开源示例项目，每个 Spring Cloud 组件都有独立的示例供大家参考学习。

**项目主页**

[https://github.com/ityouknow/spring-cloud-examples](https://github.com/ityouknow/spring-cloud-examples)

**项目截图**

![](http://www.itmind.net/assets/images/2018/springcloud/spring-cloud-examples.png) 

> 应该还有更多优秀的 Spring Cloud 开源项目，目前仅发现这些，也希望大家多反馈一些优秀的 Spring Cloud 开源项目，统一将这些项目收集到 awesome-spring-cloud 中，方便后续大家学习查找。


## 参考

[Spring Cloud 中文索引](http://springcloud.fun/)  
