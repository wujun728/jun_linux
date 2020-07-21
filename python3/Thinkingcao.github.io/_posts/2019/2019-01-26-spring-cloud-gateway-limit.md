---
layout: post
title: springcloud(十七)：服务网关 Spring Cloud GateWay 熔断、限流、重试
category: springcloud
tags: [springcloud]
keywords: springcloud, GateWay，服务网关
excerpt: Spring Cloud GateWay 熔断、限流、重试使用教程
---

上篇文章介绍了 Gataway 和注册中心的使用，以及 Gataway 中 Filter 的基本使用，这篇文章我们将继续介绍 Filter 的一些常用功能。


## 修改请求路径的过滤器

**StripPrefix Filter**

StripPrefix Filter 是一个请求路径截取的功能，我们可以利用这个功能来做特殊业务的转发。

application.yml 配置如下：

```
spring:
  cloud:
    gateway:
      routes:
      - id: nameRoot
        uri: http://nameservice
        predicates:
        - Path=/name/**
        filters:
        - StripPrefix=2
```

上面这个配置的例子表示，当请求路径匹配到`/name/**`会将包含name和后边的字符串接去掉转发，
`StripPrefix=2`就代表截取路径的个数，这样配置后当请求`/name/bar/foo`后端匹配到的请求路径就会变成`http://nameservice/foo`。

我们还是在 cloud-gateway-eureka 项目中进行测试，修改 application.yml 如下：

```
spring:
  cloud:
     routes:
     - id: nameRoot
       uri: lb://spring-cloud-producer
       predicates:
       - Path=/name/**
       filters:
       - StripPrefix=2
```

配置完后重启 cloud-gateway-eureka 项目，访问地址：`http://localhost:8888/name/foo/hello`页面会交替显示：

```
hello world!
hello world smile!
```

和直接访问地址 `http://localhost:8888/hello`展示的效果一致，说明请求路径中的 `name/foo/` 已经被截取。

**PrefixPath Filter**

PrefixPath Filter 的作用和 StripPrefix 正相反，是在 URL 路径前面添加一部分的前缀

```
spring:
  cloud:
    gateway:
      routes:
      - id: prefixpath_route
        uri: http://example.org
        filters:
        - PrefixPath=/mypath
```

大家可以下来去测试，这里不在演示。


## 限速路由器

限速在高并发场景中比较常用的手段之一，可以有效的保障服务的整体稳定性，Spring Cloud Gateway 提供了基于 Redis 的限流方案。所以我们首先需要添加对应的依赖包`spring-boot-starter-data-redis-reactive`

```
<dependency>
  <groupId>org.springframework.cloud</groupId>
  <artifactId>spring-boot-starter-data-redis-reactive</artifactId>
</dependency>
```

配置文件中需要添加 Redis 地址和限流的相关配置

```
spring:
  application:
    name: cloud-gateway-eureka
  redis:
    host: localhost
    password:
    port: 6379
  cloud:
    gateway:
     discovery:
        locator:
         enabled: true
     routes:
     - id: requestratelimiter_route
       uri: http://example.org
       filters:
       - name: RequestRateLimiter
         args:
           redis-rate-limiter.replenishRate: 10
           redis-rate-limiter.burstCapacity: 20
           key-resolver: "#{@userKeyResolver}"
       predicates:
         - Method=GET
```

- filter 名称必须是 RequestRateLimiter
- redis-rate-limiter.replenishRate：允许用户每秒处理多少个请求
- redis-rate-limiter.burstCapacity：令牌桶的容量，允许在一秒钟内完成的最大请求数
- key-resolver：使用 SpEL 按名称引用 bean

项目中设置限流的策略，创建 Config  类。

```
public class Config {

    @Bean
    KeyResolver userKeyResolver() {
        return exchange -> Mono.just(exchange.getRequest().getQueryParams().getFirst("user"));
    }
}
```

根据请求参数中的 user 字段来限流，也可以设置根据请求 IP 地址来限流，设置如下:

```
@Bean
public KeyResolver ipKeyResolver() {
    return exchange -> Mono.just(exchange.getRequest().getRemoteAddress().getHostName());
}
```

这样网关就可以根据不同策略来对请求进行限流了。

## 熔断路由器

在之前的 Spring Cloud 系列文章中，大家对熔断应该有了一定的了解，如过不了解可以先读这篇文章：[熔断器 Hystrix](http://www.ityouknow.com/springcloud/2017/05/16/springcloud-hystrix.html)

Spring Cloud Gateway 也可以利用 Hystrix 的熔断特性，在流量过大时进行服务降级，同样我们还是首先给项目添加上依赖。

```
<dependency>
  <groupId>org.springframework.cloud</groupId>
  <artifactId>spring-cloud-starter-netflix-hystrix</artifactId>
</dependency>
```

配置示例

```
spring:
  cloud:
    gateway:
      routes:
      - id: hystrix_route
        uri: http://example.org
        filters:
        - Hystrix=myCommandName
```

配置后，gateway 将使用 myCommandName 作为名称生成 HystrixCommand 对象来进行熔断管理。如果想添加熔断后的回调内容，需要在添加一些配置。

```
spring:
  cloud:
    gateway:
      routes:
      - id: hystrix_route
        uri: lb://spring-cloud-producer
        predicates:
        - Path=/consumingserviceendpoint
        filters:
        - name: Hystrix
          args:
            name: fallbackcmd
            fallbackUri: forward:/incaseoffailureusethis
```

`fallbackUri: forward:/incaseoffailureusethis`配置了 fallback 时要会调的路径，当调用 Hystrix 的 fallback 被调用时，请求将转发到`/incaseoffailureuset`这个 URI。

## 重试路由器

RetryGatewayFilter 是 Spring Cloud Gateway 对请求重试提供的一个 GatewayFilter Factory

配置示例：

```
spring:
  cloud:
    gateway:
      routes:
      - id: retry_test
        uri: lb://spring-cloud-producer
        predicates:
        - Path=/retry
        filters:
        - name: Retry
          args:
            retries: 3
            statuses: BAD_GATEWAY
```

Retry GatewayFilter 通过这四个参数来控制重试机制： retries, statuses, methods, 和 series。

- retries：重试次数，默认值是 3 次
- statuses：HTTP 的状态返回码，取值请参考：`org.springframework.http.HttpStatus`
- methods：指定哪些方法的请求需要进行重试逻辑，默认值是 GET 方法，取值参考：`org.springframework.http.HttpMethod`
- series：一些列的状态码配置，取值参考：`org.springframework.http.HttpStatus.Series`。符合的某段状态码才会进行重试逻辑，默认值是 SERVER_ERROR，值是 5，也就是 5XX(5 开头的状态码)，共有5 个值。 

以上便是项目中常用的一些网关操作，更多关于 Spring Cloud GateWay 的使用请参考官网。


**[示例代码-github](https://github.com/ityouknow/spring-cloud-examples)**

**[示例代码-码云](https://gitee.com/ityouknow/spring-cloud-examples)**

## 参考

[Spring Cloud Gateway](http://cloud.spring.io/spring-cloud-gateway/single/spring-cloud-gateway.html)   

[Spring Cloud（十六）：Spring Cloud Gateway（续）](https://windmt.com/2018/05/11/spring-cloud-16-spring-cloud-gateway-others/)