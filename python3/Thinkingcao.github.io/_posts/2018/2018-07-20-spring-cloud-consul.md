---
layout: post
title: springcloud(十三)：注册中心 Consul 使用详解
category: springcloud
tags: [springcloud]
keywords: springcloud, Consul，注册中心，消费者，提供者
excerpt: Spring Cloud Consul 使用详解
---

在上个月我们知道 Eureka 2.X 遇到困难停止开发了，但其实对国内的用户影响甚小，一方面国内大都使用的是 Eureka 1.X 系列，另一方面 Spring Cloud 支持很多服务发现的软件，Eureka 只是其中之一，下面是 Spring Cloud 支持的服务发现软件以及特性对比：

| Feature |  euerka | Consul | zookeeper | etcd |
| --- | --- | --- | --- | --- |
| 服务健康检查 | 可配支持 | 服务状态，内存，硬盘等 | (弱)长连接，keepalive | 连接心跳 | 
| 多数据中心 | — | 支持 | — | — |
| kv 存储服务 |  — |支持 | 支持 | 支持 |
| 一致性 | — |raft | paxos | raft | 
| cap | ap | ca | cp | cp | 
| 使用接口(多语言能力) | http（sidecar） | 支持 http 和 dns | 客户端 | http/grpc | 
| watch 支持 | 支持 long polling/大部分增量 | 全量/支持long polling | 支持 | 支持 long polling | 
| 自身监控 | metrics | metrics | — | metrics |
| 安全 |  — | acl /https | acl | https 支持（弱） |
| spring cloud 集成 | 已支持 | 已支持 | 已支持 | 已支持 |

在以上服务发现的软件中，Euerka 和 Consul 使用最为广泛。如果大家对注册中心的概念和 Euerka 不太了解的话， 可以参考我前期的文章：[springcloud(二)：注册中心Eureka
](http://www.ityouknow.com/springcloud/2017/05/10/springcloud-eureka.html)，本篇文章主要给大家介绍 Spring Cloud Consul 的使用。


## Consul 介绍

Consul 是 HashiCorp 公司推出的开源工具，用于实现分布式系统的服务发现与配置。与其它分布式服务注册与发现的方案，Consul 的方案更“一站式”，内置了服务注册与发现框 架、分布一致性协议实现、健康检查、Key/Value 存储、多数据中心方案，不再需要依赖其它工具（比如 ZooKeeper 等）。使用起来也较 为简单。Consul 使用 Go 语言编写，因此具有天然可移植性(支持Linux、windows和Mac OS X)；安装包仅包含一个可执行文件，方便部署，与 Docker 等轻量级容器可无缝配合。


**Consul 的优势：**

- 使用 Raft 算法来保证一致性, 比复杂的 Paxos 算法更直接. 相比较而言, zookeeper 采用的是 Paxos, 而 etcd 使用的则是 Raft。
- 支持多数据中心，内外网的服务采用不同的端口进行监听。 多数据中心集群可以避免单数据中心的单点故障,而其部署则需要考虑网络延迟, 分片等情况等。 zookeeper 和 etcd 均不提供多数据中心功能的支持。
- 支持健康检查。 etcd 不提供此功能。
- 支持 http 和 dns 协议接口。 zookeeper 的集成较为复杂, etcd 只支持 http 协议。
- 官方提供 web 管理界面, etcd 无此功能。
- 综合比较, Consul 作为服务注册和配置管理的新星, 比较值得关注和研究。


**特性：**

- 服务发现
- 健康检查
- Key/Value 存储
- 多数据中心


**Consul 角色**

- client: 客户端, 无状态, 将 HTTP 和 DNS 接口请求转发给局域网内的服务端集群。 
- server: 服务端, 保存配置信息, 高可用集群, 在局域网内与本地客户端通讯, 通过广域网与其它数据中心通讯。 每个数据中心的 server 数量推荐为 3 个或是 5 个。

Consul 客户端、服务端还支持夸中心的使用，更加提高了它的高可用性。

![](http://www.itmind.net/assets/images/2018/springcloud/consul-server-client.png)

**Consul 工作原理：**

![](http://www.itmind.net/assets/images/2018/springcloud/consol_service.png)

- 1、当 Producer 启动的时候，会向 Consul 发送一个 post 请求，告诉 Consul 自己的 IP 和 Port
- 2、Consul 接收到 Producer 的注册后，每隔10s（默认）会向 Producer 发送一个健康检查的请求，检验Producer是否健康
- 3、当 Consumer 发送 GET 方式请求 /api/address 到 Producer 时，会先从 Consul 中拿到一个存储服务 IP 和 Port 的临时表，从表中拿到 Producer 的 IP 和 Port 后再发送 GET 方式请求 /api/address
- 4、该临时表每隔10s会更新，只包含有通过了健康检查的 Producer

Spring Cloud Consul 项目是针对 Consul 的服务治理实现。Consul 是一个分布式高可用的系统，它包含多个组件，但是作为一个整体，在微服务架构中为我们的基础设施提供服务发现和服务配置的工具。

## Consul VS Eureka

Eureka 是一个服务发现工具。该体系结构主要是客户端/服务器，每个数据中心有一组 Eureka 服务器，通常每个可用区域一个。通常 Eureka 的客户使用嵌入式 SDK 来注册和发现服务。对于非本地集成的客户，官方提供的 Eureka 一些 REST 操作 API，其它语言可以使用这些 API 来实现对 Eureka Server 的操作从而实现一个非 jvm 语言的 Eureka Client。

Eureka 提供了一个弱一致的服务视图，尽可能的提供服务可用性。当客户端向服务器注册时，该服务器将尝试复制到其它服务器，但不提供保证复制完成。服务注册的生存时间（TTL）较短，要求客户端对服务器心跳检测。不健康的服务或节点停止心跳，导致它们超时并从注册表中删除。服务发现可以路由到注册的任何服务，由于心跳检测机制有时间间隔，可能会导致部分服务不可用。这个简化的模型允许简单的群集管理和高可扩展性。

Consul 提供了一些列特性，包括更丰富的健康检查，键值对存储以及多数据中心。Consul 需要每个数据中心都有一套服务，以及每个客户端的 agent，类似于使用像 Ribbon 这样的服务。Consul agent 允许大多数应用程序成为 Consul 不知情者，通过配置文件执行服务注册并通过 DNS 或负载平衡器 sidecars 发现。

Consul 提供强大的一致性保证，因为服务器使用 Raft 协议复制状态 。Consul 支持丰富的健康检查，包括 TCP，HTTP，Nagios / Sensu 兼容脚本或基于 Eureka 的 TTL。客户端节点参与基于 Gossip 协议的健康检查，该检查分发健康检查工作，而不像集中式心跳检测那样成为可扩展性挑战。发现请求被路由到选举出来的 leader，这使他们默认情况下强一致性。允许客户端过时读取取使任何服务器处理他们的请求，从而实现像 Eureka 这样的线性可伸缩性。

Consul 强烈的一致性意味着它可以作为领导选举和集群协调的锁定服务。Eureka 不提供类似的保证，并且通常需要为需要执行协调或具有更强一致性需求的服务运行 ZooKeeper。

Consul 提供了支持面向服务的体系结构所需的一系列功能。这包括服务发现，还包括丰富的运行状况检查，锁定，密钥/值，多数据中心联合，事件系统和 ACL。Consul 和 consul-template 和 envconsul 等工具生态系统都试图尽量减少集成所需的应用程序更改，以避免需要通过 SDK 进行本地集成。Eureka 是一个更大的 Netflix OSS 套件的一部分，该套件预计应用程序相对均匀且紧密集成。因此 Eureka 只解决了一小部分问题，可以和 ZooKeeper 等其它工具可以一起使用。

Consul 强一致性(C)带来的是：

服务注册相比 Eureka 会稍慢一些。因为 Consul 的 raft 协议要求必须过半数的节点都写入成功才认为注册成功 
Leader 挂掉时，重新选举期间整个 Consul 不可用。保证了强一致性但牺牲了可用性。

Eureka 保证高可用(A)和最终一致性：

服务注册相对要快，因为不需要等注册信息 replicate 到其它节点，也不保证注册信息是否 replicate 成功
当数据出现不一致时，虽然 A, B 上的注册信息不完全相同，但每个 Eureka 节点依然能够正常对外提供服务，这会出现查询服务信息时如果请求 A 查不到，但请求 B 就能查到。如此保证了可用性但牺牲了一致性。

其它方面，eureka 就是个 servlet 程序，跑在 servlet 容器中; Consul 则是 go 编写而成。


## Consul 安装

Consul 不同于 Eureka 需要单独安装，访问[Consul 官网](https://www.consul.io/downloads.html)下载 Consul 的最新版本，我这里是 consul_1.2.1。

根据不同的系统类型选择不同的安装包，从下图也可以看出 Consul 支持所有主流系统。

![](http://www.itmind.net/assets/images/2018/springcloud/consul_insall.png)


我这里以 Windows 为例，下载下来是一个 consul_1.2.1_windows_amd64.zip 的压缩包，解压是是一个 consul.exe 的执行文件。

![](http://www.itmind.net/assets/images/2018/springcloud/consul_win.png)

cd 到对应的目录下，使用 cmd 启动 Consul

```
cd D:\Common Files\consul
#cmd启动：
consul agent -dev        # -dev表示开发模式运行，另外还有-server表示服务模式运行
```

为了方便期间，可以在同级目录下创建一个 run.bat 脚本来启动，脚本内容如下：

```
consul agent -dev
pause
```

启动结果如下：

![](http://www.itmind.net/assets/images/2018/springcloud/consol_cmd.png)

启动成功之后访问：`http://localhost:8500`，可以看到 Consul 的管理界面

![](http://www.itmind.net/assets/images/2018/springcloud/consol_manage.png)

这样就意味着我们的 Consul 服务启动成功了。

## Consul 服务端

接下来我们开发 Consul 的服务端，我们创建一个 spring-cloud-consul-producer 项目

### 添加依赖包

依赖包如下：

```
<dependencies>
	<dependency>
		<groupId>org.springframework.boot</groupId>
		<artifactId>spring-boot-starter-actuator</artifactId>
	</dependency>
	<dependency>
		<groupId>org.springframework.cloud</groupId>
		<artifactId>spring-cloud-starter-consul-discovery</artifactId>
	</dependency>
	<dependency>
		<groupId>org.springframework.boot</groupId>
		<artifactId>spring-boot-starter-web</artifactId>
	</dependency>
	<dependency>
		<groupId>org.springframework.boot</groupId>
		<artifactId>spring-boot-starter-test</artifactId>
		<scope>test</scope>
	</dependency>
</dependencies>
```

- `spring-boot-starter-actuator` 健康检查依赖于此包。
- `spring-cloud-starter-consul-discovery` Spring Cloud Consul 的支持。


Spring Boot 版本使用的是 2.0.3.RELEASE，Spring Cloud 最新版本是 Finchley.RELEASE 依赖于 Spring Boot 2.x.

```
<parent>
	<groupId>org.springframework.boot</groupId>
	<artifactId>spring-boot-starter-parent</artifactId>
	<version>2.0.3.RELEASE</version>
	<relativePath/> <!-- lookup parent from repository -->
</parent>

<dependencyManagement>
	<dependencies>
		<dependency>
			<groupId>org.springframework.cloud</groupId>
			<artifactId>spring-cloud-dependencies</artifactId>
			<version>${spring-cloud.version}</version>
			<type>pom</type>
			<scope>import</scope>
		</dependency>
	</dependencies>
</dependencyManagement>
```

完整的 pom.xml 文件大家可以参考示例源码。

### 配置文件

配置文件内容如下

```
spring.application.name=spring-cloud-consul-producer
server.port=8501
spring.cloud.consul.host=localhost
spring.cloud.consul.port=8500
#注册到consul的服务名称
spring.cloud.consul.discovery.serviceName=service-producer
```

Consul 的地址和端口号默认是 localhost:8500 ，如果不是这个地址可以自行配置。
`spring.cloud.consul.discovery.serviceName` 是指注册到 Consul 的服务名称，后期客户端会根据这个名称来进行服务调用。


### 启动类

``` java
@SpringBootApplication
@EnableDiscoveryClient
public class ConsulProducerApplication {

	public static void main(String[] args) {
		SpringApplication.run(ConsulProducerApplication.class, args);
	}
}
```

添加了 `@EnableDiscoveryClient` 注解表示支持服务发现。


### 提供服务

我们在创建一个 Controller，推文提供 hello 的服务。

``` java
@RestController
public class HelloController {

    @RequestMapping("/hello")
    public String hello() {
        return "helle consul";
    }
}
```

为了模拟注册均衡负载复制一份上面的项目重命名为 spring-cloud-consul-producer-2 ,修改对应的端口为 8502，修改 hello 方法的返回值为："helle consul two"，修改完成后依次启动两个项目。

这时候我们再次在浏览器访问地址：http://localhost:8500，显示如下：

![](http://www.itmind.net/assets/images/2018/springcloud/consol_producer.png)

我们发现页面多了 service-producer 服务，点击进去后页面显示有两个服务提供者：

![](http://www.itmind.net/assets/images/2018/springcloud/consol_producer-2.png)

这样服务提供者就准备好了。

## Consul 消费端

我们创建一个 spring-cloud-consul-consumer 项目，pom 文件和上面示例保持一致。


### 配置文件

配置文件内容如下

```
spring.application.name=spring-cloud-consul-consumer
server.port=8503
spring.cloud.consul.host=127.0.0.1
spring.cloud.consul.port=8500
#设置不需要注册到 consul 中
spring.cloud.consul.discovery.register=false
```

客户端可以设置注册到 Consul 中，也可以不注册到 Consul 注册中心中，根据我们的业务来选择，只需要在使用服务时通过 Consul 对外提供的接口获取服务信息即可。


### 启动类

``` java
@SpringBootApplication
public class ConsulConsumerApplication {

	public static void main(String[] args) {
		SpringApplication.run(ConsulConsumerApplication.class, args);
	}
}
```

### 进行测试

我们先来创建一个 ServiceController ,试试如果去获取 Consul 中的服务。

``` java
@RestController
public class ServiceController {

    @Autowired
    private LoadBalancerClient loadBalancer;
    @Autowired
    private DiscoveryClient discoveryClient;

   /**
     * 获取所有服务
     */
    @RequestMapping("/services")
    public Object services() {
        return discoveryClient.getInstances("service-producer");
    }

    /**
     * 从所有服务中选择一个服务（轮询）
     */
    @RequestMapping("/discover")
    public Object discover() {
        return loadBalancer.choose("service-producer").getUri().toString();
    }
}
```

Controller 中有俩个方法，一个是获取所有服务名为`service-producer`的服务信息并返回到页面，一个是随机从服务名为`service-producer`的服务中获取一个并返回到页面。

添加完 ServiceController 之后我们启动项目，访问地址：`http://localhost:8503/services`，返回：


```
[{"serviceId":"service-producer","host":"windows10.microdone.cn","port":8501,"secure":false,"metadata":{"secure":"false"},"uri":"http://windows10.microdone.cn:8501","scheme":null},{"serviceId":"service-producer","host":"windows10.microdone.cn","port":8502,"secure":false,"metadata":{"secure":"false"},"uri":"http://windows10.microdone.cn:8502","scheme":null}]
```

发现我们刚才创建的端口为 8501 和 8502 的两个服务端都存在。

多次访问地址：`http://localhost:8503/discover`，页面会交替返回下面信息：

```
http://windows10.microdone.cn:8501
http://windows10.microdone.cn:8502
...
```

说明 8501 和 8501 的两个服务会交替出现，从而实现了获取服务端地址的均衡负载。

大多数情况下我们希望使用均衡负载的形式去获取服务端提供的服务，因此使用第二种方法来模拟调用服务端提供的 hello 方法。

创建  CallHelloController ：

``` java
@RestController
public class CallHelloController {

    @Autowired
    private LoadBalancerClient loadBalancer;

    @RequestMapping("/call")
    public String call() {
        ServiceInstance serviceInstance = loadBalancer.choose("service-producer");
        System.out.println("服务地址：" + serviceInstance.getUri());
        System.out.println("服务名称：" + serviceInstance.getServiceId());

        String callServiceResult = new RestTemplate().getForObject(serviceInstance.getUri().toString() + "/hello", String.class);
        System.out.println(callServiceResult);
        return callServiceResult;
    }

}
```

使用 RestTemplate 进行远程调用。添加完之后重启 spring-cloud-consul-consumer 项目。在浏览器中访问地址：`http://localhost:8503/call`，依次返回结果如下：

```
helle consul
helle consul two
...
```

说明我们已经成功的调用了 Consul 服务端提供的服务，并且实现了服务端的均衡负载功能。通过今天的实践我们发现 Consul 提供的服务发现易用、强大。


**[示例代码-github](https://github.com/ityouknow/spring-cloud-examples)**

**[示例代码-码云](https://gitee.com/ityouknow/spring-cloud-examples)**