---
layout: post
title: gradle-使用总结
category: other
tags: [other]
---

spring 项目建议使用Gradle进行构建项目，相比maven来讲Gradle更简洁，而且gradle更时候大型复杂项目的构建。gradle吸收了maven和ant的特点而来，不过目前maven仍然是Java界的主流


### 命令
1、gradle build  编译


#### Execution failed for task ':compileJava'.
> 无效的源发行版: 1.8

报错不匹配的Java编译版本

使用```gradle -version``` 查看gradle支持的jdk版本号，如果不是1.8,修改本地的Java_home环境变量为1.8，在次执行OK。


### * What went wrong:
Execution failed for task ':findMainClass'.
> Unable to find a single main class from the following candidates [**]

报错没有找到主入口

build.gradle 添加

``` properties
springBoot {
  mainClass = "com.favorites.Application"
}
```

