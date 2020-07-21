---
layout: post
title: Spring Boot 2 (八)：Spring Boot 集成 Memcached
category: springboot
no-post-nav: true
tags: [springboot]
keywords: Spring Boot,Memcached
excerpt: Spring Boot 和 Memcached 的解决方案
---

## Memcached 介绍

Memcached 是一个高性能的分布式内存对象缓存系统，用于动态Web应用以减轻数据库负载。它通过在内存中缓存数据和对象来减少读取数据库的次数，从而提高动态、数据库驱动网站的速度。Memcached基于一个存储键/值对的hashmap。其守护进程（daemon ）是用C写的，但是客户端可以用任何语言来编写，并通过memcached协议与守护进程通信。

因为 Spring Boot 没有针对 Memcached 提供对应的组建包，因此需要我们自己来集成。官方推出的 Java 客户端 Spymemcached 是一个比较好的选择之一。

**Spymemcached 介绍**

Spymemcached 最早由 Dustin Sallings 开发，Dustin 后来和别人一起创办了 Couchbase (原NorthScale)，职位为首席架构师。2014 加入 Google。

Spymemcached 是一个采用 Java 开发的异步、单线程的 Memcached 客户端， 使用 NIO 实现。Spymemcached 是 Memcached 的一个流行的 Java client 库，性能表现出色，广泛应用于 Java + Memcached 项目中。


## 依赖配置

**添加依赖**

pomx 包中添加 spymemcached 的引用

``` xml
<dependency>
  <groupId>net.spy</groupId>
  <artifactId>spymemcached</artifactId>
  <version>2.12.2</version>
</dependency>
```

**添加配置**

```
memcache.ip=192.168.0.161
memcache.port=11211
```

分别配置 memcache 的 Ip 地址和 端口。


**设置配置对象**

创建 `MemcacheSource` 接收配置信息

``` java
@Component
@ConfigurationProperties(prefix = "memcache")
public class MemcacheSource {

    private String ip;

    private int port;

    public String getIp() {
        return ip;
    }

    public void setIp(String ip) {
        this.ip = ip;
    }

    public int getPort() {
        return port;
    }

    public void setPort(int port) {
        this.port = port;
    }
}
```

`@ConfigurationProperties(prefix = "memcache")` 的意思会以 `memcache.*` 为开通将对应的配置文件加载到属性中。


## 启动初始化 MemcachedClient

我们使用上一节的内容[Spring Boot 2 (七)：Spring Boot 如何解决项目启动时初始化资源](http://www.ityouknow.com/springboot/2018/05/03/spring-boot-commandLineRunner.html),利用 CommandLineRunner 在项目启动的时候配置好 MemcachedClient 。

``` java
@Component
public class MemcachedRunner implements CommandLineRunner {
    protected Logger logger =  LoggerFactory.getLogger(this.getClass());

    @Resource
    private  MemcacheSource memcacheSource;

    private MemcachedClient client = null;

    @Override
    public void run(String... args) throws Exception {
        try {
            client = new MemcachedClient(new InetSocketAddress(memcacheSource.getIp(),memcacheSource.getPort()));
        } catch (IOException e) {
            logger.error("inint MemcachedClient failed ",e);
        }
    }

    public MemcachedClient getClient() {
        return client;
    }

}
```

## 测试使用

``` java
@RunWith(SpringRunner.class)
@SpringBootTest
public class RepositoryTests {

  @Resource
    private MemcachedRunner memcachedRunner;

  @Test
  public void testSetGet()  {
    MemcachedClient memcachedClient = memcachedRunner.getClient();
    memcachedClient.set("testkey",1000,"666666");
    System.out.println("***********  "+memcachedClient.get("testkey").toString());
  }

}
```

使用中先测试插入一个 key 为 testkey ，1000 为过期时间单位为 毫秒，最后的 "666666" 为 key 对应的值。


执行测试用例 testSetGet ，控制台输出内容：

```
***********  666666
```

表明测试成功。


**[示例代码-github](https://github.com/ityouknow/spring-boot-examples)**

**[示例代码-码云](https://gitee.com/ityouknow/spring-boot-examples)**