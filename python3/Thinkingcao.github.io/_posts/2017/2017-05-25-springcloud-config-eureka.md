---
layout: post
title: springcloud(八)：配置中心服务化和高可用
category: springcloud
tags: [springcloud]
---


在前两篇的介绍中，客户端都是直接调用配置中心的server端来获取配置文件信息。这样就存在了一个问题，客户端和服务端的耦合性太高，如果server端要做集群，客户端只能通过原始的方式来路由，server端改变IP地址的时候，客户端也需要修改配置，不符合springcloud服务治理的理念。springcloud提供了这样的解决方案，我们只需要将server端当做一个服务注册到eureka中，client端去eureka中去获取配置中心server端的服务既可。

这篇文章我们基于配置中心git版本的内容来改造


## server端改造

### 1、添加依赖

``` xml
<dependencies>
	<dependency>
		<groupId>org.springframework.cloud</groupId>
		<artifactId>spring-cloud-config-server</artifactId>
	</dependency>
	<dependency>
		<groupId>org.springframework.cloud</groupId>
		<artifactId>spring-cloud-starter-eureka</artifactId>
	</dependency>
</dependencies>
```

需要多引入```spring-cloud-starter-eureka```包，来添加对eureka的支持。

### 2、配置文件

``` properties
server:
server:
  port: 8001
spring:
  application:
    name: spring-cloud-config-server
  cloud:
    config:
      server:
        git:
          uri: https://github.com/ityouknow/spring-cloud-starter/     # 配置git仓库的地址
          search-paths: config-repo                             # git仓库地址下的相对地址，可以配置多个，用,分割。
          username: username                                        # git仓库的账号
          password: password                                    # git仓库的密码
eureka:
  client:
    serviceUrl:
      defaultZone: http://localhost:8000/eureka/   ## 注册中心eurka地址
```

增加了eureka注册中心的配置

### 3、启动类

启动类添加```@EnableDiscoveryClient```激活对配置中心的支持

``` java
@EnableDiscoveryClient
@EnableConfigServer
@SpringBootApplication
public class ConfigServerApplication {

	public static void main(String[] args) {
		SpringApplication.run(ConfigServerApplication.class, args);
	}
}
```

这样server端的改造就完成了。先启动eureka注册中心，在启动server端，在浏览器中访问：```http://localhost:8000/``` 就会看到server端已经注册了到注册中心了。

 
![](http://www.itmind.net/assets/images/2017/springcloud/eureka-config01.jpg)


按照上篇的测试步骤对server端进行测试服务正常。


## 客户端改造


### 1、添加依赖

``` xml
<dependencies>
	<dependency>
		<groupId>org.springframework.cloud</groupId>
		<artifactId>spring-cloud-starter-config</artifactId>
	</dependency>
	<dependency>
		<groupId>org.springframework.boot</groupId>
		<artifactId>spring-boot-starter-web</artifactId>
	</dependency>
	<dependency>
		<groupId>org.springframework.cloud</groupId>
		<artifactId>spring-cloud-starter-eureka</artifactId>
	</dependency>
	<dependency>
		<groupId>org.springframework.boot</groupId>
		<artifactId>spring-boot-starter-test</artifactId>
		<scope>test</scope>
	</dependency>
</dependencies>
```

需要多引入```spring-cloud-starter-eureka```包，来添加对eureka的支持。

### 2、配置文件

``` properties
spring.application.name=spring-cloud-config-client
server.port=8002

spring.cloud.config.name=neo-config
spring.cloud.config.profile=dev
spring.cloud.config.label=master
spring.cloud.config.discovery.enabled=true
spring.cloud.config.discovery.serviceId=spring-cloud-config-server

eureka.client.serviceUrl.defaultZone=http://localhost:8000/eureka/
```

主要是去掉了```spring.cloud.config.uri```直接指向server端地址的配置，增加了最后的三个配置：

- ```spring.cloud.config.discovery.enabled``` ：开启Config服务发现支持
- ```spring.cloud.config.discovery.serviceId``` ：指定server端的name,也就是server端```spring.application.name```的值
- ```eureka.client.serviceUrl.defaultZone``` ：指向配置中心的地址

这三个配置文件都需要放到```bootstrap.properties```的配置中

### 3、启动类

启动类添加```@EnableDiscoveryClient```激活对配置中心的支持

``` java
@EnableDiscoveryClient
@SpringBootApplication
public class ConfigClientApplication {

	public static void main(String[] args) {
		SpringApplication.run(ConfigClientApplication.class, args);
	}
}
```

启动client端，在浏览器中访问：```http://localhost:8000/``` 就会看到server端和client端都已经注册了到注册中心了。

 
![](http://www.itmind.net/assets/images/2017/springcloud/eureka-config02.jpg)


## 高可用

为了模拟生产集群环境，我们改动server端的端口为8003，再启动一个server端来做服务的负载，提供高可用的server端支持。

 
![](http://www.itmind.net/assets/images/2017/springcloud/eureka-config03.jpg)

如上图就可发现会有两个server端同时提供配置中心的服务，防止某一台down掉之后影响整个系统的使用。

我们先单独测试服务端，分别访问：```http://localhost:8001/neo-config/dev```、```http://localhost:8003/neo-config/dev```返回信息：

```
{
    "name": "neo-config", 
    "profiles": [
        "dev"
    ], 
    "label": null, 
    "version": null, 
    "state": null, 
    "propertySources": [
        {
            "name": "https://github.com/ityouknow/spring-cloud-starter/config-repo/neo-config-dev.properties", 
            "source": {
                "neo.hello": "hello im dev"
            }
        }
    ]
}
```

说明两个server端都正常读取到了配置信息。

再次访问：```http://localhost:8002/hello```，返回：```hello im dev update```。说明客户端已经读取到了server端的内容，我们随机停掉一台server端的服务，再次访问```http://localhost:8002/hello```，返回：```hello im dev update```，说明达到了高可用的目的。


**[示例代码-github](https://github.com/ityouknow/spring-cloud-examples)**

**[示例代码-码云](https://gitee.com/ityouknow/spring-cloud-examples)**

-------------
**作者：纯洁的微笑**  
**出处：[http://www.ityouknow.com/](http://www.ityouknow.com/springcloud/2017/05/25/springcloud-config-eureka.html)**      
**版权归作者所有，转载请注明出处** 
