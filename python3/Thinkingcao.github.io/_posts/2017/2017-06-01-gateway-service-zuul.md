---
layout: post
title: springcloud(十)：服务网关zuul初级篇
category: springcloud
tags: [springcloud]
---

前面的文章我们介绍了，Eureka用于服务的注册于发现，Feign支持服务的调用以及均衡负载，Hystrix处理服务的熔断防止故障扩散，Spring Cloud Config服务集群配置中心，似乎一个微服务框架已经完成了。

我们还是少考虑了一个问题，外部的应用如何来访问内部各种各样的微服务呢？在微服务架构中，后端服务往往不直接开放给调用端，而是通过一个API网关根据请求的url，路由到相应的服务。当添加API网关后，在第三方调用端和服务提供方之间就创建了一面墙，这面墙直接与调用方通信进行权限控制，后将请求均衡分发给后台服务端。


## 为什么需要API Gateway


1、简化客户端调用复杂度
 

在微服务架构模式下后端服务的实例数一般是动态的，对于客户端而言很难发现动态改变的服务实例的访问地址信息。因此在基于微服务的项目中为了简化前端的调用逻辑，通常会引入API Gateway作为轻量级网关，同时API Gateway中也会实现相关的认证逻辑从而简化内部服务之间相互调用的复杂度。

 
![](http://www.itmind.net/assets/images/2017/springcloud/api_gateway.png)


2、数据裁剪以及聚合
 
通常而言不同的客户端对于显示时对于数据的需求是不一致的，比如手机端或者Web端又或者在低延迟的网络环境或者高延迟的网络环境。

因此为了优化客户端的使用体验，API Gateway可以对通用性的响应数据进行裁剪以适应不同客户端的使用需求。同时还可以将多个API调用逻辑进行聚合，从而减少客户端的请求数，优化客户端用户体验


3、多渠道支持
 
当然我们还可以针对不同的渠道和客户端提供不同的API Gateway,对于该模式的使用由另外一个大家熟知的方式叫Backend for front-end, 在Backend for front-end模式当中，我们可以针对不同的客户端分别创建其BFF，进一步了解BFF可以参考这篇文章：[Pattern: Backends For Frontends](http://samnewman.io/patterns/architectural/bff/)

 
![](http://www.itmind.net/assets/images/2017/springcloud/bff.png)


4、遗留系统的微服务化改造

对于系统而言进行微服务改造通常是由于原有的系统存在或多或少的问题，比如技术债务，代码质量，可维护性，可扩展性等等。API Gateway的模式同样适用于这一类遗留系统的改造，通过微服务化的改造逐步实现对原有系统中的问题的修复，从而提升对于原有业务响应力的提升。通过引入抽象层，逐步使用新的实现替换旧的实现。

 
![](http://www.itmind.net/assets/images/2017/springcloud/bff-process.png)

> 在Spring Cloud体系中， Spring Cloud Zuul就是提供负载均衡、反向代理、权限认证的一个API gateway。

## Spring Cloud Zuul

Spring Cloud Zuul路由是微服务架构的不可或缺的一部分，提供动态路由，监控，弹性，安全等的边缘服务。Zuul是Netflix出品的一个基于JVM路由和服务端的负载均衡器。


下面我们通过代码来了解Zuul是如何工作的

### 简单使用

1、添加依赖

``` xml
<dependency>
	<groupId>org.springframework.cloud</groupId>
	<artifactId>spring-cloud-starter-zuul</artifactId>
</dependency>
```

引入```spring-cloud-starter-zuul```包

2、配置文件

``` properties
spring.application.name=gateway-service-zuul
server.port=8888

#这里的配置表示，访问/it/** 直接重定向到http://www.ityouknow.com/**
zuul.routes.baidu.path=/it/**
zuul.routes.baidu.url=http://www.ityouknow.com/
```

3、启动类

``` java
@SpringBootApplication
@EnableZuulProxy
public class GatewayServiceZuulApplication {

	public static void main(String[] args) {
		SpringApplication.run(GatewayServiceZuulApplication.class, args);
	}
}
```

启动类添加```@EnableZuulProxy```，支持网关路由。

史上最简单的zuul案例就配置完了


4、测试

启动```gateway-service-zuul-simple```项目，在浏览器中访问：```http://localhost:8888/it/spring-cloud```，看到页面返回了：```http://www.ityouknow.com/spring-cloud ``` 页面的信息，如下：

 
![](http://www.itmind.net/assets/images/2017/springcloud/zuul-01.jpg)


我们以前面文章的示例代码```spring-cloud-producer```为例来测试请求的重定向，在配置文件中添加：

``` properties
zuul.routes.hello.path=/hello/**
zuul.routes.hello.url=http://localhost:9000/
```

启动```spring-cloud-producer```，重新启动```gateway-service-zuul-simple```，访问：```http://localhost:8888/hello/hello?name=%E5%B0%8F%E6%98%8E```，返回：```hello 小明，this is first messge```

说明访问```gateway-service-zuul-simple```的请求自动转发到了```spring-cloud-producer```，并且将结果返回。


### 服务化

通过url映射的方式来实现zull的转发有局限性，比如每增加一个服务就需要配置一条内容，另外后端的服务如果是动态来提供，就不能采用这种方案来配置了。实际上在实现微服务架构时，服务名与服务实例地址的关系在eureka server中已经存在了，所以只需要将Zuul注册到eureka server上去发现其他服务，就可以实现对serviceId的映射。

我们结合示例来说明，在上面示例项目```gateway-service-zuul-simple```的基础上来改造。


1、添加依赖

``` xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-eureka</artifactId>
</dependency>
```

增加```spring-cloud-starter-eureka```包，添加对eureka的支持。

2、配置文件

配置修改为：

``` properties
spring.application.name=gateway-service-zuul
server.port=8888

zuul.routes.api-a.path=/producer/**
zuul.routes.api-a.serviceId=spring-cloud-producer

eureka.client.serviceUrl.defaultZone=http://localhost:8000/eureka/
```

3、测试

依次启动 ```spring-cloud-eureka```、 ```spring-cloud-producer```、```gateway-service-zuul-eureka```，访问：```http://localhost:8888/producer/hello?name=%E5%B0%8F%E6%98%8E```，返回：```hello 小明，this is first messge```

说明访问```gateway-service-zuul-eureka```的请求自动转发到了```spring-cloud-producer```，并且将结果返回。


为了更好的模拟服务集群，我们复制```spring-cloud-producer```项目改为```spring-cloud-producer-2```，修改```spring-cloud-producer-2```项目端口为9001，controller代码修改如下：

``` java
@RestController
public class HelloController {
	
    @RequestMapping("/hello")
    public String index(@RequestParam String name) {
        return "hello "+name+"，this is two messge";
    }
}
```

修改完成后启动```spring-cloud-producer-2```，重启```gateway-service-zuul-eureka```。测试多次访问```http://localhost:8888/producer/hello?name=%E5%B0%8F%E6%98%8E```，依次返回：

``` 
hello 小明，this is first messge
hello 小明，this is two messge
hello 小明，this is first messge
hello 小明，this is two messge
...
```

说明通过zuul成功调用了producer服务并且做了均衡负载。


**网关的默认路由规则**

但是如果后端服务多达十几个的时候，每一个都这样配置也挺麻烦的，spring cloud zuul已经帮我们做了默认配置。默认情况下，Zuul会代理所有注册到Eureka Server的微服务，并且Zuul的路由规则如下：```http://ZUUL_HOST:ZUUL_PORT/微服务在Eureka上的serviceId/**```会被转发到serviceId对应的微服务。


我们注销掉```gateway-service-zuul-eureka```项目中关于路由的配置：

``` properties
#zuul.routes.api-a.path=/producer/**
#zuul.routes.api-a.serviceId=spring-cloud-producer
```

重新启动后，访问```http://localhost:8888/spring-cloud-producer/hello?name=%E5%B0%8F%E6%98%8E```，测试返回结果和上述示例相同，说明Spring cloud zuul默认已经提供了转发功能。

到此zuul的基本使用我们就介绍完了。关于zuul更高级使用，我们下篇再来介绍。

参考：

[API网关那些儿](http://yunlzheng.github.io/2017/03/14/the-things-about-api-gateway/)

**[示例代码-github](https://github.com/ityouknow/spring-cloud-examples)**

**[示例代码-码云](https://gitee.com/ityouknow/spring-cloud-examples)**

-------------
**作者：纯洁的微笑**  
**出处：[http://www.ityouknow.com/](http://www.ityouknow.com/springcloud/2017/06/01/gateway-service-zuul.html)**      
**版权归作者所有，转载请注明出处** 
