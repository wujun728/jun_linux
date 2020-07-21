---
layout: post
title: 从架构演进的角度聊聊Spring Cloud都做了些什么？
category: springcloud
tags: [springcloud]
keywords: 微服务,架构,Spring Cloud
---

Spring Cloud作为一套微服务治理的框架，几乎考虑到了微服务治理的方方面面，之前也写过一些关于Spring Cloud文章，主要偏重各组件的使用，本次分享主要解答这两个问题：Spring Cloud在微服务的架构中都做了哪些事情？Spring Cloud提供的这些功能对微服务的架构提供了怎样的便利？

这也是我写Spring Cloud三部曲的最后一篇文章，前两面篇内容如下：

- [中小型互联网公司微服务实践-经验和教训](http://mp.weixin.qq.com/s/bciSlKearaVFQg1QWOSn_g)

- [Spring Cloud在国内中小型公司能用起来吗？](https://mp.weixin.qq.com/s/vnWXpH5pv-FAzLZfbgTGvg)


我们先来简单回顾一下，我们以往互联网架构的发展情况：

## 传统架构发展史

### 单体架构

单体架构在小微企业比较常见，典型代表就是一个应用、一个数据库、一个web容器就可以跑起来，比如我们开发的开源软件[云收藏](https://github.com/cloudfavorites/favorites-web)，就是标准的单体架构。

在两种情况下可能会选择单体架构：一是在企业发展的初期，为了保证快速上线，采用此种方案较为简单灵活；二是传统企业中垂直度较高，访问压力较小的业务。在这种模式下对技术要求较低，方便各层次开发人员接手，也能满足客户需求。


下面是单体架构的架构图：

![](http://www.itmind.net/assets/images/2017/chat/single_structure.jpg)  

在单体架构中，技术选型非常灵活，优先满足快速上线的要求，也便于快速跟进市场。

### 垂直架构

在单体架构发展一段时间后，公司的业务模式得到了认可，交易量也慢慢的大起来，这时候有些企业为了应对更大的流量，就会对原有的业务进行拆分，比如说：后台系统、前端系统、交易系统等。

在这一阶段往往会将系统分为不同的层级，每个层级有对应的职责，UI层负责和用户进行交互、业务逻辑层负责具体的业务功能、数据库层负责和上层进行数据交换和存储。

下面是垂直架构的架构图：

![](http://www.itmind.net/assets/images/2017/chat/vertical__structure.jpg) 


在这个阶段SSH（struts+spring+hibernate）是项目的关键技术，Struts负责web层逻辑控制、Spring负责业务层管理Bean、Hibernate负责数据库操作进行封装，持久化数据。


### 服务化架构

如果公司进一步的做大，垂直子系统会变的越来越多，系统和系统之间的调用关系呈指数上升的趋势。在这样的背景下，很多公司都会考虑服务的SOA化。SOA代表面向服务的架构，将应用程序根据不同的职责划分为不同的模块，不同的模块直接通过特定的协议和接口进行交互。这样使整个系统切分成很多单个组件服务来完成请求，当流量过大时通过水平扩展相应的组件来支撑，所有的组件通过交互来满足整体的业务需求。

SOA服务化的优点是，它可以根据需求通过网络对松散耦合的粗粒度应用组件进行分布式部署、组合和使用。服务层是SOA的基础，可以直接被应用调用，从而有效控制系统中与软件代理交互的人为依赖性。

服务化架构是一套松耦合的架构，服务的拆分原则是服务内部高内聚，服务之间低耦合。

下面是服务化架构图：

![](http://www.itmind.net/assets/images/2017/chat/soa__structure.jpg)  

在这个阶段可以使用WebService或者dubbo来服务治理。

我们发现从单体架构到服务化架构，应用数量都在不断的增加，慢慢的下沉的就成了基础组建，上浮的就成为业务系统。从上述也可以看出架构的本质就是不断的拆分重构：分的过程是把系统拆分为各个子系统/模块/组件，拆的时候，首先要解决每个组件的定位问题，然后才能划分彼此的边界，实现合理的拆分。合就是根据最终要求，把各个分离的组件有机整合在一起。拆分的结果使开发人员能够做到业务聚焦、技能聚焦，实现开发敏捷，合的结果是系统变得柔性，可以因需而变，实现业务敏捷。

## SOA和微服务架构

### SOA和微服务的区别

其实服务化架构已经可以解决大部分企业的需求了，那么我们为什么要研究微服务呢？先说说它们的区别；

- 微服务架构强调业务系统需要彻底的组件化和服务化，一个组件就是一个产品，可以独立对外提供服务    
- 微服务不再强调传统SOA架构里面比较重的ESB企业服务总线  
- 微服务强调每个微服务都有自己独立的运行空间，包括数据库资源。  
- 微服务架构本身来源于互联网的思路，因此组件对外发布的服务强调了采用HTTP Rest API的方式来进行  
- 微服务的切分粒度会更小   

> 总结:微服务架构是 SOA 架构思想的一种扩展，更加强调服务个体的独立性、拆分粒度更小。


### 为什么考虑Spring Cloud

- Spring Cloud来源于Spring，质量、稳定性、持续性都可以得到保证  
- Spring Cloud天然支持Spring Boot，更加便于业务落地。  
- Spring Cloud发展非常的快，从16年开始接触的时候相关组件版本为1.x，到现在将要发布2.x系列  
- Spring Cloud是Java领域最适合做微服务的框架。  
- 相比于其它框架,Spring Cloud对微服务周边环境的支持力度最大。  
- 对于中小企业来讲，使用门槛较低。  

> Spring Cloud　是微服务架构的最佳落地方案

### 它的特性

以下为Spring Cloud的核心特性：  

- 分布式/版本化配置
- 服务注册和发现
- 路由
- 服务和服务之间的调用
- 负载均衡
- 断路器
- 分布式消息传递

这些特性都是由不同的组件来完成，在架构的演进过程中扮演着重要的角色，接下来我们一起看看。

## 微服务架构

Spring Cloud解决的第一个问题就是：服务与服务之间的解耦。很多公司在业务高速发展的时候，服务组件也会相应的不断增加。服务和服务之间有着复杂的相互调用关系，经常有服务A调用服务B，服务B调用服务C和服务D ...，随着服务化组件的不断增多，服务之间的调用关系成指数级别的增长，极端情况下就如下图所示：

![](http://www.itmind.net/assets/images/2017/architecture/calling_relation.png)  

这样最容易导致的情况就是牵一发而动全身。经常出现由于某个服务更新而没有通知到其它服务，导致上线后惨案频发。这时候就应该进行服务治理，将服务之间的直接依赖转化为服务对服务中心的依赖。Spring Cloud 核心组件Eureka就是解决这类问题。

### Eureka

Eureka是Netflix开源的一款提供服务注册和发现的产品，它提供了完整的Service Registry和Service Discovery实现。也是Spring Cloud体系中最重要最核心的组件之一。

用大白话讲，Eureka就是一个服务中心，将所有的可以提供的服务都注册到它这里来管理，其它各调用者需要的时候去注册中心获取，然后再进行调用，避免了服务之间的直接调用，方便后续的水平扩展、故障转移等。如下图：

![](http://www.itmind.net/assets/images/2017/architecture/eureka.jpg)  

当然服务中心这么重要的组件一但挂掉将会影响全部服务，因此需要搭建Eureka集群来保持高可用性，生产中建议最少两台。随着系统的流量不断增加，需要根据情况来扩展某个服务，Eureka内部已经提供均衡负载的功能，只需要增加相应的服务端实例既可。那么在系统的运行期间某个实例挂了怎么办？Eureka内容有一个心跳检测机制，如果某个实例在规定的时间内没有进行通讯则会自动被剔除掉，避免了某个实例挂掉而影响服务。

因此使用了Eureka就自动具有了注册中心、负载均衡、故障转移的功能。如果想对Eureka进一步了解可以参考这篇文章：[注册中心Eureka](http://www.ityouknow.com/springcloud/2017/05/10/springcloud-eureka.html)

### Hystrix

在微服务架构中通常会有多个服务层调用，基础服务的故障可能会导致级联故障，进而造成整个系统不可用的情况，这种现象被称为服务雪崩效应。服务雪崩效应是一种因“服务提供者”的不可用导致“服务消费者”的不可用,并将不可用逐渐放大的过程。

如下图所示：A作为服务提供者，B为A的服务消费者，C和D是B的服务消费者。A不可用引起了B的不可用，并将不可用像滚雪球一样放大到C和D时，雪崩效应就形成了。

![](http://www.itmind.net/assets/images/2017/springcloud/hystrix-1.png)

在这种情况下就需要整个服务机构具有故障隔离的功能，避免某一个服务挂掉影响全局。在Spring Cloud 中Hystrix组件就扮演这个角色。

Hystrix会在某个服务连续调用N次不响应的情况下，立即通知调用端调用失败，避免调用端持续等待而影响了整体服务。Hystrix间隔时间会再次检查此服务，如果服务恢复将继续提供服务。

继续了解Hystrix可以参考：[熔断器Hystrix](http://www.ityouknow.com/springcloud/2017/05/10/springcloud-eureka.html)

### Hystrix Dashboard和Turbine

当熔断发生的时候需要迅速的响应来解决问题，避免故障进一步扩散，那么对熔断的监控就变得非常重要。熔断的监控现在有两款工具：Hystrix-dashboard和Turbine

Hystrix-dashboard是一款针对Hystrix进行实时监控的工具，通过Hystrix Dashboard我们可以直观地看到各Hystrix Command的请求响应时间, 请求成功率等数据。但是只使用Hystrix Dashboard的话, 你只能看到单个应用内的服务信息, 这明显不够. 我们需要一个工具能让我们汇总系统内多个服务的数据并显示到Hystrix Dashboard上, 这个工具就是Turbine.
监控的效果图如下：

![](http://www.itmind.net/assets/images/2017/springcloud/turbine-02.jpg)

想了解具体都监控了哪些指标，以及如何监控可以参考这篇文章：[熔断监控Hystrix Dashboard和Turbine](http://www.ityouknow.com/springcloud/2017/05/18/hystrix-dashboard-turbine.html)

### 配置中心

随着微服务不断的增多，每个微服务都有自己对应的配置文件。在研发过程中有测试环境、UAT环境、生产环境，因此每个微服务又对应至少三个不同环境的配置文件。这么多的配置文件，如果需要修改某个公共服务的配置信息，如：缓存、数据库等，难免会产生混乱，这个时候就需要引入Spring Cloud另外一个组件：Spring Cloud Config。

#### Spring Cloud Config

Spring Cloud Config是一个解决分布式系统的配置管理方案。它包含了Client和Server两个部分，Server提供配置文件的存储、以接口的形式将配置文件的内容提供出去，Client通过接口获取数据、并依据此数据初始化自己的应用。

其实就是Server端将所有的配置文件服务化，需要配置文件的服务实例去Config Server获取对应的数据。将所有的配置文件统一整理，避免了配置文件碎片化。配置中心git实例参考：[配置中心git示例](http://www.ityouknow.com/springcloud/2017/05/22/springcloud-config-git.html)；

如果服务运行期间改变配置文件，服务是不会得到最新的配置信息，需要解决这个问题就需要引入Refresh。可以在服务的运行期间重新加载配置文件，具体可以参考这篇文章：[配置中心svn示例和refresh](http://www.ityouknow.com/springcloud/2017/05/23/springcloud-config-svn-refresh.html)

当所有的配置文件都存储在配置中心的时候，配置中心就成为了一个非常重要的组件。如果配置中心出现问题将会导致灾难性的后果，因此在生产中建议对配置中心做集群，来支持配置中心高可用性。具体参考：[配置中心服务化和高可用](http://www.ityouknow.com/springcloud/2017/05/25/springcloud-config-eureka.html)

#### Spring Cloud Bus

上面的Refresh方案虽然可以解决单个微服务运行期间重载配置信息的问题，但是在真正的实践生产中，可能会有N多的服务需要更新配置，如果每次依靠手动Refresh将是一个巨大的工作量，这时候Spring Cloud提出了另外一个解决方案：Spring Cloud Bus

Spring Cloud Bus通过轻量消息代理连接各个分布的节点。这会用在广播状态的变化（例如配置变化）或者其它的消息指令中。Spring Cloud Bus的一个核心思想是通过分布式的启动器对Spring Boot应用进行扩展，也可以用来建立一个或多个应用之间的通信频道。目前唯一实现的方式是用AMQP消息代理作为通道。

Spring Cloud Bus是轻量级的通讯组件，也可以用在其它类似的场景中。有了Spring Cloud Bus之后，当我们改变配置文件提交到版本库中时，会自动的触发对应实例的Refresh，具体的工作流程如下：

![](http://www.itmind.net/assets/images/2017/springcloud/configbus2.jpg)

也可以参考这篇文章来了解：[配置中心和消息总线](http://www.ityouknow.com/springcloud/2017/05/26/springcloud-config-eureka-bus.html)

### 服务网关

在微服务架构模式下，后端服务的实例数一般是动态的，对于客户端而言很难发现动态改变的服务实例的访问地址信息。因此在基于微服务的项目中为了简化前端的调用逻辑，通常会引入API Gateway作为轻量级网关，同时API Gateway中也会实现相关的认证逻辑从而简化内部服务之间相互调用的复杂度。

![](http://www.itmind.net/assets/images/2017/springcloud/api_gateway.png)

Spring Cloud体系中支持API Gateway落地的技术就是Zuul。Spring Cloud Zuul路由是微服务架构中不可或缺的一部分，提供动态路由，监控，弹性，安全等的边缘服务。Zuul是Netflix出品的一个基于JVM路由和服务端的负载均衡器。

它的具体作用就是服务转发，接收并转发所有内外部的客户端调用。使用Zuul可以作为资源的统一访问入口，同时也可以在网关做一些权限校验等类似的功能。

具体使用参考这篇文章：[服务网关zuul](http://www.ityouknow.com/springcloud/2017/06/01/gateway-service-zuul.html)

### 链路跟踪

随着服务的越来越多，对调用链的分析会越来越复杂，如服务之间的调用关系、某个请求对应的调用链、调用之间消费的时间等，对这些信息进行监控就成为一个问题。在实际的使用中我们需要监控服务和服务之间通讯的各项指标，这些数据将是我们改进系统架构的主要依据。因此分布式的链路跟踪就变的非常重要，Spring Cloud也给出了具体的解决方案：Spring Cloud Sleuth和Zipkin

![](http://www.itmind.net/assets/images/2017/architecture/dyl.png)

Spring Cloud Sleuth为服务之间调用提供链路追踪。通过Sleuth可以很清楚的了解到一个服务请求经过了哪些服务，每个服务处理花费了多长时间。从而让我们可以很方便的理清各微服务间的调用关系。

Zipkin是Twitter的一个开源项目，允许开发者收集 Twitter 各个服务上的监控数据，并提供查询接口

分布式链路跟踪需要Sleuth+Zipkin结合来实现，具体操作参考这篇文章：[分布式链路跟踪(Sleuth)](http://www.jianshu.com/p/c3d191663279)


### 总结

我们从整体上来看一下Spring Cloud各个组件如何来配套使用：

![](http://www.itmind.net/assets/images/2017/chat/spring_cloud_structure.png)

从上图可以看出Spring Cloud各个组件相互配合，合作支持了一套完整的微服务架构。

- 其中Eureka负责服务的注册与发现，很好将各服务连接起来
- Hystrix 负责监控服务之间的调用情况，连续多次失败进行熔断保护。
- Hystrix dashboard,Turbine 负责监控 Hystrix的熔断情况，并给予图形化的展示  
- Spring Cloud Config 提供了统一的配置中心服务  
- 当配置文件发生变化的时候，Spring Cloud Bus 负责通知各服务去获取最新的配置信息  
- 所有对外的请求和服务，我们都通过Zuul来进行转发，起到API网关的作用  
- 最后我们使用Sleuth+Zipkin将所有的请求数据记录下来，方便我们进行后续分析  


Spring Cloud从设计之初就考虑了绝大多数互联网公司架构演化所需的功能，如服务发现注册、配置中心、消息总线、负载均衡、断路器、数据监控等。这些功能都是以插拔的形式提供出来，方便我们系统架构演进的过程中，可以合理的选择需要的组件进行集成，从而在架构演进的过程中会更加平滑、顺利。

微服务架构是一种趋势，Spring Cloud提供了标准化的、全站式的技术方案，意义可能会堪比当前Servlet规范的诞生，有效推进服务端软件系统技术水平的进步。


**这是我在GitChat的分享[从架构演进的角度聊聊 Spring Cloud 都做了些什么？](http://gitbook.cn/gitchat/author/5949f1f19bc6b9498d120a0d)**
