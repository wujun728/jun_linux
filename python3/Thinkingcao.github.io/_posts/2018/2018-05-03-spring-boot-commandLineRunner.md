---
layout: post
title: Spring Boot 2 (七)：Spring Boot 如何解决项目启动时初始化资源
category: springboot
tags: [springboot]
keywords: Spring Boot,commandLineRunner
---

在我们实际工作中，总会遇到这样需求，在项目启动的时候需要做一些初始化的操作，比如初始化线程池，提前加载好加密证书等。今天就给大家介绍一个 Spring Boot 神器，专门帮助大家解决项目启动初始化资源操作。

这个神器就是 `CommandLineRunner`，`CommandLineRunner` 接口的 `Component` 会在所有 `Spring Beans `都初始化之后，`SpringApplication.run() `之前执行，非常适合在应用程序启动之初进行一些数据初始化的工作。

接下来我们就运用案例测试它如何使用，在测试之前在启动类加两行打印提示，方便我们识别 `CommandLineRunner` 的执行时机。

``` java
@SpringBootApplication
public class CommandLineRunnerApplication {
	public static void main(String[] args) {
		System.out.println("The service to start.");
		SpringApplication.run(CommandLineRunnerApplication.class, args);
		System.out.println("The service has started.");
	}
}
```

接下来我们直接创建一个类继承 `CommandLineRunner` ，并实现它的 `run()` 方法。

``` java
@Component
public class Runner implements CommandLineRunner {
    @Override
    public void run(String... args) throws Exception {
        System.out.println("The Runner start to initialize ...");
    }
}
```

我们在 `run()` 方法中打印了一些参数来看出它的执行时机。完成之后启动项目进行测试：


```
...
The service to start.

  .   ____          _            __ _ _
 /\\ / ___'_ __ _ _(_)_ __  __ _ \ \ \ \
( ( )\___ | '_ | '_| | '_ \/ _` | \ \ \ \
 \\/  ___)| |_)| | | | | || (_| |  ) ) ) )
  '  |____| .__|_| |_|_| |_\__, | / / / /
 =========|_|==============|___/=/_/_/_/
 :: Spring Boot ::        (v2.0.0.RELEASE)
...
2018-04-21 22:21:34.706  INFO 27016 --- [           main] o.s.b.w.embedded.tomcat.TomcatWebServer  : Tomcat started on port(s): 8080 (http) with context path ''
2018-04-21 22:21:34.710  INFO 27016 --- [           main] com.neo.CommandLineRunnerApplication     : Started CommandLineRunnerApplication in 3.796 seconds (JVM running for 5.128)
The Runner start to initialize ...
The service has started.
```

根据控制台的打印信息我们可以看出 `CommandLineRunner` 中的方法会在 Spring Boot 容器加载之后执行，执行完成后项目启动完成。


如果我们在启动容器的时候需要初始化很多资源，并且初始化资源相互之间有序，那如何保证不同的 `CommandLineRunner` 的执行顺序呢？Spring Boot 也给出了解决方案。那就是使用 `@Order` 注解。

我们创建两个 `CommandLineRunner` 的实现类来进行测试：

第一个实现类：

``` java
@Component
@Order(1)
public class OrderRunner1 implements CommandLineRunner {
    @Override
    public void run(String... args) throws Exception {
        System.out.println("The OrderRunner1 start to initialize ...");
    }
}
```

第二个实现类：

``` java
@Component
@Order(2)
public class OrderRunner2 implements CommandLineRunner {
    @Override
    public void run(String... args) throws Exception {
        System.out.println("The OrderRunner2 start to initialize ...");
    }
}
```

添加完成之后重新启动，观察执行顺序：

```
...
The service to start.

  .   ____          _            __ _ _
 /\\ / ___'_ __ _ _(_)_ __  __ _ \ \ \ \
( ( )\___ | '_ | '_| | '_ \/ _` | \ \ \ \
 \\/  ___)| |_)| | | | | || (_| |  ) ) ) )
  '  |____| .__|_| |_|_| |_\__, | / / / /
 =========|_|==============|___/=/_/_/_/
 :: Spring Boot ::        (v2.0.0.RELEASE)
...
2018-04-21 22:21:34.706  INFO 27016 --- [           main] o.s.b.w.embedded.tomcat.TomcatWebServer  : Tomcat started on port(s): 8080 (http) with context path ''
2018-04-21 22:21:34.710  INFO 27016 --- [           main] com.neo.CommandLineRunnerApplication     : Started CommandLineRunnerApplication in 3.796 seconds (JVM running for 5.128)
The OrderRunner1 start to initialize ...
The OrderRunner2 start to initialize ...
The Runner start to initialize ...
The service has started.
```

通过控制台的输出我们发现，添加 `@Order` 注解的实现类最先执行，并且`@Order()`里面的值越小启动越早。

在实践中，使用`ApplicationRunner`也可以达到相同的目的，两着差别不大。看来使用 Spring Boot 解决初始化资源的问题非常简单。


**[示例代码-github](https://github.com/ityouknow/spring-boot-examples)**

**[示例代码-码云](https://gitee.com/ityouknow/spring-boot-examples)**