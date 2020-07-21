---
layout: post
title: 是时候给大家介绍 Spring Boot/Cloud 背后豪华的研发团队了。
category: springboot
tags: [springboot]
keywords: Spring Boot,Pivotal,Spring Cloud, 研发团队
---

看了 Pivotal 公司的发展历史，这尼玛就是一场商业大片呀。

我们刚开始学习 Spring Boot 的时候肯定都会看到这么一句话：

> Spring Boot 是由 Pivotal 团队提供的全新框架，其设计目的是用来简化新 Spring 应用的初始搭建以及开发过程。

这里的 Pivotal 团队肯定就是 Spring Boot 的研发团队了，那么这个 Pivotal 团队到底是个什么来头呢？和 Spring 又有那些关系？不着急且听我慢慢道来。

要说起这个 Pivotal 公司的由来，我得先从 Spring 企业的这条线来说起。

## Spring 的发展

时间回到 2002 年，当时正是 Java EE 和 EJB 大行其道的时候，很多知名公司都是采用此技术方案进行项目开发。这时候有一个美国的小伙子认为 EJB 太过臃肿，并不是所有的项目都需要使用 EJB 这种大型框架，应该会有一种更好的方案来解决这个问题。

他为了证明自己的想法是正确的，在 2002 年 10 月写了一本书《Expert One-on-One J2EE》，介绍了当时 Java 企业应用程序开发的情况，并指出了 Java EE 和 EJB 组件框架中存在的一些主要缺陷。在这本书中，他提出了一个基于普通 Java 类和依赖注入的更简单的解决方案。

在书中，他展示了如何在不使用 EJB 的情况下构建高质量、可扩展的在线座位预留系统。为了构建应用程序，他编写了超过 30,000 行的基础结构代码，项目中的根包命名为 `com.interface21`，所以人们最初称这套开源框架为 interface21，这就是 Spring 的前身。

这个小伙子是谁呢？他就是大名鼎鼎的 Rod Johnson（下图），Rod Johnson 在悉尼大学不仅获得了计算机学位，同时还获得了音乐学位，更令人吃惊的是在回到软件开发领域之前，他还获得了音乐学的博士学位。现在 Rod Johnson 已经离开了 Spring，成为了一个天使投资人，同时也是多个公司的董事，早已走上人生巅峰。

![](http://www.itmind.net/assets/images/2018/springboot/rod.jpg)

在这本书发布后，一对一的 J2EE 设计和开发一炮而红。这本书免费提供的大部分基础架构代码都是高度可重用的。2003 年 Rod Johnson 和同伴在此框架的基础上开发了一个全新的框架命名为 Spring，据 Rod Johnson 介绍 Spring 是传统 J2EE 新的开始，随后 Spring 发展进入快车道。

- 2004 年 03 月，1.0 版发布。
- 2006 年 10 月，2.0 版发布。
- 2007 年 11 月，更名为 SpringSource，同时发布了 Spring 2.5。
- 2009 年 12 月，Spring 3.0 发布。
- 2013 年 12 月，Pivotal 宣布发布 Spring 框架 4.0。
- 2017 年 09 月，Spring 5.0 发布。


网上有一张图，清晰的展示了 Spring 发展：

![](http://www.itmind.net/assets/images/2018/springboot/springhistoryinfographic.jpg)

从上面这个时间线我们可以看出 Pivotal 团队和 Spring 在 2013 年交上了线，这是为什么呢？

> 友情提示，接下来科技行业的一系列商业并购大片即将开启。

## Pivotal 公司

上面说的 Pivotal 团队是指 Pivotal 公司，先给大家来一段 Pivotal 公司的简介：

> Pivotal 成立于2013年4月，致力于“改变世界构造软件的方式（We are transforming how the world builds software）”，提供云原生应用开发 PaaS 平台及服务，帮助企业客户采用敏捷软件开发方法论，从而提高软件开发人员工作效率、减少运维成本，实现数字化转型、IT 创新，并最终实现业务创新。
 
> 截至目前，财富 100 强中超过三分之一的企业使用 Pivotal 云原生平台。Pivotal 部分大型客户在采用 Pivotal 产品后，开发人员与运营人员比例可提高到 200:1，开发人员专注于编写软件代码时间增长了 50%。

看了简介大家可能会有点犯迷糊，这不是一个 2013 年成立的 IT 服务公司吗，和 2002 年发展起来的 Spring 又是怎么扯上关系的呢？其实呀，要说起 Pivotal 公司的起源要追溯到 1989 年的  Pivotal Labs 实验室。


![Pivotal 中国办公室环境](http://www.ityouknow.com/assets/images/2018/springboot/pivotaoffice.jpeg)


## Pivotal Labs 公司

1989 年，Rob Mee 创立的咨询公司 Pivotal Labs，专注于快速的互联网式软件开发，即敏捷编程。创立 Pivotal Labs 的时候，它还是一家非常小的软件顾问公司，它的主营业务就是与客户合作，帮助客户开发软件。

Pivotal Labs 一直是敏捷开发领域的领导者，为部分硅谷最有影响力的公司塑造了软件开发文化，并树立了良好口碑，其中 Google、Twitter 都曾是 Pivotal Labs 客户。

时间很快到了 2012 年，深受客户喜爱的 Pivotal 终于引起了商用软件巨头 EMC 的关注，EMC 在 2012 年以现金方式收购了 Pivotal 并照单全收了它的 200 名员工。

刚开始的时候，公司并没有发生太大的变化，只是作为新部门成为了 EMC 的一部分，Pivotal Labs 仍然继续像以前样与客户合作。

但是到 2013 年的时候，EMC 突然扔下了一颗重磅炸弹。它将 Pivotal Labs 的核心业务分拆出去，成立了一家名为 Pivotal Software 的新公司。这家新公司的股东是 EMC 、 VMware 和通用电气，之前在 EMC 子公司 VMware 担任首席执行官的马瑞兹出任公司的首席执行官。

EMC 和 VMware 分拆出其 Cloud Foundry、Pivotal Labs、Greenplum 等云计算、大数据资源，GE 投资 1.05 亿美元，成立新公司 Pivotal。新生的 Pivotal 是名副其实的“富二代”，这轮估值高达 10.5 亿美元。

## 那么 EMC 和 VMware 又有什么关联呢？

2003 年 12 月， EMC 公司宣布以 6.35 亿美元收购了 VMware 公司。

EMC 于 1979 年成立于美国麻州 Hopkinton 市，1989 年开始进入企业数据储存市场。二十多年来，EMC 全心投注在各项新的储存技术，已获得了 1,300 个已通过或审核中的储存技术专利。无论是全球外接 RAID 储存系统、网络储存亦或是储存管理软件等储存专业领域，EMC 均是业界公认的领导厂商。

EMC 是全球第六大企业软件公司，全球信息基础架构技术与解决方案的领先开发商与提供商。同时也是美国财富五百强之一，在全世界拥有超过四万二千名员工，在全球 60 个国家或地区拥有分支机构。我们接触比较多就是 EMC 的各种存储产品。

EMC 公司做大 EMC 的秘诀，就是研发与并购双轮驱动，研发与并购的投入占当年营业收入的 22% 左右，并购投入略高于研发。从 2003 年到2 015 年的 12 年间，EMC 总共投入超过 420 亿美元用于研发和收购。其中，206 亿美元用于研发，213 亿美元用于并购，总共并购了 100 多家公司。

## VMware 收购 Spring

2009 年是 Spring 企业的一个转折点，VMware 以 4.2 亿美元收购 Spring Source (3.6亿现金外加5800万股份） 。

**可以说虚拟化就是 VMware 发明的**

VMware 于 1998 年成立，公司总部位于美国加州帕洛阿尔托，是全球云基础架构和移动商务解决方案厂商，提供基于VMware的解决方案，企业通过数据中心改造和公有云整合业务，借助企业安全转型维系客户信任，实现任意云端和设备上运行、管理、连接及保护任意应用。2018 财年全年收入 79.2 亿美元。

相信作为研发人员肯定都使用过 VMware 公司的产品，最常用的是 VMware 的虚拟机产品，但其实  VMware 公司的产品线非常多。

从发展路线来看，VMware 具备三大特点：

- 第一，是技术具备领先性，虚拟化技术在70年代就已出现，但VMware是第一个将这项技术应用到X86服务器上，并在这个基础上不断完善，使其能够满足企业级客户需求；
- 第二，是瞄准大型企业客户。VMware 刚刚上市时，年营收不到4亿美金，但已经覆盖80%的财富1000强客户；
- 第三，是高度产品化。VMware 的毛利率长期保持在 85% 左右，咨询业务占比非常少，几乎将所有部署工作都交给合作伙伴。

VMware 也是一个并购大户，通过投资和收购补全业务线，客户资源是一大优势。
![](http://www.itmind.net/assets/images/2018/springboot/vmare.JPG)

> 2012 年 Rod Johnson 宣布他将要离开 Spring Source 。


## EMC 又被收购

2015 年的时候，曾经被大量报道 EMC 考虑被子公司 VMware 收购，让人大跌眼镜，竟然可以有这样的骚动作，这是为什么呢？

EMC 在 2003 年斥资 6.25 亿美元收购了 VMware，四年之后，EMC 选择让 VMware 分拆上市，结果独立上市的 VMware 发展越来越好，反观 EMC 的各项业务持续陷入低潮。到 2015 年的时候，VMware 的市值已达到约 370 亿美元，占据了 EMC 总市值的近 75%。

可能各方利益不能达成一致，最终 EMC 却被戴尔（dell）收购。

2015 年 10 月 12 日，戴尔（Dell）和EMC（易安信）公司宣布签署最终协议，戴尔公司与其创始人、主席和首席执行官麦克尔•戴尔，与 MSD Partner 以及银湖资本一起，收购 EMC 公司，交易总额达 670亿 美元，成为科技史上最大并购。

当时业界最关心的云计算软件商 VMware 仍然保持独立上市公司的身份。据悉，EMC 当前持有 VMware 大约 80% 的股权，市值约为 320 亿美元。而戴尔收购 EMC 实际上是项庄舞剑，VMware 才是戴尔收购 EMC 的关键。

## 戴尔的故事

1984 年，创办人迈克尔·戴尔在德州大学奥斯汀分校就学时创立了 PCs Limited 这家计算机公司。在 1985 年，公司生产了第一部拥有自己独特设计的计算机“Turbo PC”，售价为 795 美元。从此开启了戴尔公司的发展史，下面为戴尔公司的里程碑

- 1984年 - 年仅19岁的Michael Dell凭借1,000美元的资金建立了PC's Limited，并且树立了颠覆技术行业的愿景。
- 1988年 - 我们完成了首次公开募股，募集了3,000万美元资金，公司市值从1,000美元增长到8500万美元。
- 1992年 - 戴尔跻身财富500强公司行列，Michael Dell也成为榜单上最年轻的CEO。
- 1996年 - Dell.com上线，该站点上线仅六个月之后，每天销售额即达100万美元。
- 2001年 - 戴尔成为 全球第一大计算机系统提供商。
- 2005年 - 在《财富》杂志的“美国最受赞赏公司”排名中，戴尔位列第一。
- 2010年 - 戴尔被 Gartner, Inc.评为世界第一大医疗保健信息技术服务提供商。
- 2013年 - Michael Dell携手私人股本公司Silver Lake Partners，从公众股东手里买回了戴尔股份，旨在加快解决方案战略的实施并专注于大多数客户重视的创新和长期投资。
2016年 - 戴尔与EMC合并为Dell Technologies，这是业内最大的技术集成事件。
戴尔提供的工作

2018年的时候又传出，VMware 反收购戴尔？写到这里的时候我都感觉有点乱了？戴尔收购了 EMC， ECM 收购了 VMware ，那么 VMware 就差不多算戴尔的重孙子，那么怎么又来 VMware 反收购戴尔？

原来是这样，在 2015 年 10 月 12 日业界正式爆料戴尔收购 EMC（包括 VMware），当时的 VMware 股价在 60－70 美元左右。到了 2016 年 9 月戴尔宣布正式并购 EMC 包括 VMware，只是让 VMware 独立运营，VMware 当时股价也还是在 70 美元左右。

可是到了 2018 年初一看，VMware 股价已经到达了 130 多美元，在 2018 年的最高点，股价甚至达到了 160 多美元，股价又 TM 涨了一倍多，VMware 公司简直发展太好了。VMware 最新的市值快到了 6000 亿美金，当初收购时 VMware 市值也就 200 多亿美金，简直赚翻了呀！

传言只是传言，最终 2018 年 7 月，戴尔还是选择了独立上市，拥有 VMware 80% 的股份。

## 并购时间表 

上面写的有点乱，大家看完之后也许有点迷糊，在这里重新整理一下这里面几个关键公司的收购时间点：

- 1989 年，Rob Mee 创立的咨询公司 Pivotal Labs;
- 2003 年，Rod Johnson 和同伴创建了 Spring；
- 2003 年，EMC 收购了 VMware 公司；
- 2009 年，VMware 收购了 Spring ;
- 2012 年，EMC 又收购了 Pivotal Labs 公司；
- 2013 年，EMC 、 VMware 和收购来的 Pivotal Labs 公司重新组建了新的公司 Pivotal;
- 2015 年，戴尔又并购了 EMC;
- 2018 年，戴尔独立上市。

## 接着说 Pivotal 公司

上面一系列的商业并购搞的眼花缭乱的，但是大家只要知道 Pivotal 公司出身高贵，来自几个都不太差钱的世界 500 强公司联合组建而成，Pivotal 公司的产品非常的高大上，就连我们平时使用的 12306 都使用了他们公司的产品。

Pivotal 公司可谓是大牛云集，公司的开源产品有：Spring 以及 Spring 衍生产品、Web 服务器 Tomcat、缓存中间件 Redis、消息中间件 RabbitMQ、平台即服务的 Cloud Foundry、Greenplum 数据引擎、还有大名鼎鼎的 GemFire（12306 系统解决方案组件之一）。

这些著名开源产品背后的开发者都在 Pivotal 公司，其研发团队汇集了全球的一流开发者，Spring Boot 为什么如此优秀，或许在这里可以找到一些答案。

Pivotal 中国研发中心在中国创建于 2010 年，它的前身是 EMC Greenplum 部门，其团队成员分布在北京和上海两地，目前正致力于以下产品的研发和服务的提供：Pivotal Web Service (PWS), Pivotal Hadoop (PHD), Hawq 和 Greenplum Database (GPDB)。

毕威拓科技（北京）有限公司（Pivotal中国公司）2015年3月1日正式成立并单独运营。

Pivotal 公司成立之后，于 2014 年发布了 Spring Boot，2015 年发布了 Spring Cloud，2018 年 Pivotal 公司在纽约上市。我们可以通过一张图来了解 Pivotal 公司的发展史。

![](http://www.itmind.net/assets/images/2018/springboot/pivotal.jpeg)

Pivotal 的定位是一家下一代云计算和大数据应用相结合的公司，而 VMWare 和原 EMC 的业务方向则依然是软件定义数据中心和信息基础架构。

官网这样介绍他们的产品：Pivotal 提供的工具能够帮助开发人员构建更出色软件，可让您在任意云环境中运行应用的平台，帮助您打造未来。

公司的产品主要分为三大类：部署和运行软件，规划、构建和集成软件，分析和决策

**部署和运行软件**

- Pivotal Cloud Foundry (PCF)，用于快速交付应用、容器和函数的多云平台。
- PCF: Pivotal Application Service，
在具有内置日志记录、监控和自动扩展功能且高度可用的自助服务平台上，运行使用任意语言构建的应用。
- PCF: Pivotal Container Service，基于企业级Kubernetes环境构建应用，该环境采用按需群集、滚动升级和VMware NSX提供的软件定义的网络。
- Pivotal Services Marketplace，
将您的应用与托管、代理或按需服务相结合。产品涵盖数据管理、API管理、消息传递、日志记录等。

**规划、构建和集成软件**

- Spirng Boot，借助领先的Java框架快速构建功能强大的应用和服务。
- Spirng Cloud，
将经过验证的微服务模式融入您的软件。提供配置存储、服务发现、消息传递等功能。
- Steeltoe，受 Spring Cloud 启发，用该框架构建恢复力强、可扩展的.NET应用。
- Pivotal Cloud Cache，采用基于 Pivotal GemFire 的快速且高度可用的缓存，可提供地理复制和后台写入功能。
- Pivotal GemFire，利用可扩展、事件驱动的分布式数据网格执行内存中计算。12306采用的商业方案。
- RabbitMQ，借助这款广受欢迎的消息传递代理，分离服务并扩展处理进程。
- Pivotal Tracker，经过验证的项目管理工具，帮您打造成功的敏捷团队。
- Concourse，利用自动化管道实现 PCF 的持续升级。

**分析和决策**

- Pivotal Greenplum，使用这个功能齐全的多云大规模并行处理(MPP)数据平台，可以对大型数据集进行高级分析。。
- Apache MADlib，通过采用数据并行方式实施多结构数据的数学、统计和机器学习方法来执行数据库内分析。

Pivotal 公司的产品有 Spring Boot 、Spring Cloud 、RabbitMQ 等非常著名的开源软件，也有很多类似 GemFire 等商业解决方案，通过他们公司的产品即可发现，一边通过开源软件打造生态，一方面通过商业解决方案来挣钱。

曾经有一段时间，有人就问我一个问题，说开源的是不是就意味着是免费的，不免费的服务，是不是就意味着不是开源的软件？这种商业模式其实就是对这种观点的一种反驳，开源不等于免费，开源是一种开放分享的精神，不要什么东西来到国内都变味了。

Pivotal 掌握很多最新前沿的开源技术，公司提供的从云端部署到一整套的大数据解决方案，从开发到平台到提供解决方案到提供咨询，可以说真正依赖技术挣钱的典范，我辈之楷模！

最后送大家一个学习 Spring Boot 的开源项目: [spring-boot-examples](https://github.com/ityouknow/spring-boot-examples)

## 参考

[是时候说说Pivotal这个富二代了！](https://www.sohu.com/a/127172641_464027)  
[五年做到60亿美金市值，PaaS第一股Pivotal的崛起之路 | 爱分析调研](https://www.sohu.com/a/238794360_545428)





