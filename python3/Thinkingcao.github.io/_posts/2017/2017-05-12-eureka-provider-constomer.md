---
layout: post
title: springcloud(三)：服务提供与调用
category: springcloud
tags: [springcloud]
---

上一篇文章我们介绍了eureka服务注册中心的搭建，这篇文章介绍一下如何使用eureka服务注册中心，搭建一个简单的服务端注册服务，客户端去调用服务使用的案例。

案例中有三个角色：服务注册中心、服务提供者、服务消费者，其中服务注册中心就是我们上一篇的eureka单机版启动既可，流程是首先启动注册中心，服务提供者生产服务并注册到服务中心中，消费者从服务中心中获取服务并执行。

## 服务提供

我们假设服务提供者有一个hello方法，可以根据传入的参数，提供输出“hello  xxx，this is first messge”的服务

### 1、pom包配置

创建一个springboot项目，pom.xml中添加如下配置：

``` xml
<dependencies>
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

### 2、配置文件

application.properties配置如下：

``` properties
spring.application.name=spring-cloud-producer
server.port=9000
eureka.client.serviceUrl.defaultZone=http://localhost:8000/eureka/
```

参数在上一篇都已经解释过，这里不多说。

### 3、启动类

启动类中添加```@EnableDiscoveryClient```注解

``` java
@SpringBootApplication
@EnableDiscoveryClient
public class ProducerApplication {

	public static void main(String[] args) {
		SpringApplication.run(ProducerApplication.class, args);
	}
}
```

### 4、controller

提供hello服务

``` java
@RestController
public class HelloController {
	
    @RequestMapping("/hello")
    public String index(@RequestParam String name) {
        return "hello "+name+"，this is first messge";
    }
}
```

添加```@EnableDiscoveryClient```注解后，项目就具有了服务注册的功能。启动工程后，就可以在注册中心的页面看到SPRING-CLOUD-PRODUCER服务。

 
![](http://www.itmind.net/assets/images/2017/springcloud/eureka_server.png)

到此服务提供者配置就完成了。

## 服务调用

### 1、pom包配置

和服务提供者一致

``` xml
<dependencies>
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

### 2、配置文件

application.properties配置如下：

``` properties
spring.application.name=spring-cloud-consumer
server.port=9001
eureka.client.serviceUrl.defaultZone=http://localhost:8000/eureka/
```

### 3、启动类

启动类添加```@EnableDiscoveryClient```和```@EnableFeignClients```注解。

``` java
@SpringBootApplication
@EnableDiscoveryClient
@EnableFeignClients
public class ConsumerApplication {

	public static void main(String[] args) {
		SpringApplication.run(ConsumerApplication.class, args);
	}

}
```

- ```@EnableDiscoveryClient``` :启用服务注册与发现
- ```@EnableFeignClients```：启用feign进行远程调用

>Feign是一个声明式Web Service客户端。使用Feign能让编写Web Service客户端更加简单, 它的使用方法是定义一个接口，然后在上面添加注解，同时也支持JAX-RS标准的注解。Feign也支持可拔插式的编码器和解码器。Spring Cloud对Feign进行了封装，使其支持了Spring MVC标准注解和HttpMessageConverters。Feign可以与Eureka和Ribbon组合使用以支持负载均衡。

### 4、feign调用实现

``` java
@FeignClient(name= "spring-cloud-producer")
public interface HelloRemote {
    @RequestMapping(value = "/hello")
    public String hello(@RequestParam(value = "name") String name);
}
```

- name:远程服务名，及spring.application.name配置的名称

此类中的方法和远程服务中contoller中的方法名和参数需保持一致。


### 5、web层调用远程服务

将HelloRemote注入到controller层，像普通方法一样去调用即可。

``` java
@RestController
public class ConsumerController {

    @Autowired
    HelloRemote HelloRemote;
	
    @RequestMapping("/hello/{name}")
    public String index(@PathVariable("name") String name) {
        return HelloRemote.hello(name);
    }

}
```

到此，最简单的一个服务注册与调用的例子就完成了。


## 测试

### 简单调用
依次启动spring-cloud-eureka、spring-cloud-producer、spring-cloud-consumer三个项目

先输入：```http://localhost:9000/hello?name=neo``` 检查spring-cloud-producer服务是否正常

返回：```hello neo，this is first messge```

说明spring-cloud-producer正常启动，提供的服务也正常。

浏览器中输入：```http://localhost:9001/hello/neo```  

返回：```hello neo，this is first messge``` 

说明客户端已经成功的通过feign调用了远程服务hello，并且将结果返回到了浏览器。

### 负载均衡

以上面spring-cloud-producer为例子修改，将其中的controller改动如下：

``` java
@RestController
public class HelloController {
	
    @RequestMapping("/hello")
    public String index(@RequestParam String name) {
        return "hello "+name+"，this is producer 2  send first messge";
    }
}
```

在配置文件中改动端口：

``` properties
spring.application.name=spring-cloud-producer
server.port=9003
eureka.client.serviceUrl.defaultZone=http://localhost:8000/eureka/
```

打包启动后，在eureka就会发现两个服务提供者，如下图：

 
![](http://www.itmind.net/assets/images/2017/springcloud/eureka_server2.png)

然后在浏览器再次输入：```http://localhost:9001/hello/neo```  进行测试：

第一次返回结果：```hello neo，this is first messge```

第二次返回结果：```hello neo，this is producer 2  send first messge```

不断的进行测试下去会发现两种结果交替出现，说明两个服务中心自动提供了服务均衡负载的功能。如果我们将服务提供者的数量在提高为N个，测试结果一样，请求会自动轮询到每个服务端来处理。

**[示例代码-github](https://github.com/ityouknow/spring-cloud-examples)**

**[示例代码-码云](https://gitee.com/ityouknow/spring-cloud-examples)**

-------------

**作者：纯洁的微笑**  
**出处：[http://www.ityouknow.com/](http://www.ityouknow.com/springcloud/2017/05/12/eureka-provider-constomer.html)**      
**版权归作者所有，转载请注明出处** 



