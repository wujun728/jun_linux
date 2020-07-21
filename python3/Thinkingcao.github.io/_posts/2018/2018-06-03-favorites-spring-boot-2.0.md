---
layout: post
title: Spring Boot 2 版的开源项目云收藏来了！
no-post-nav: true
category: springboot
tags: [springboot]
keywords: Spring Boot,Spring Boot 2.0,云收藏,升级
excerpt: 给大家聊一聊云收藏从 Spring Boot 1.0 升级到 2.0 所踩的坑
---

先给大家晒一下云收藏的几个数据，作为一个 Spring Boot 的开源项目（[https://github.com/cloudfavorites/favorites-web](https://github.com/cloudfavorites/favorites-web)）目前在 Github 上面已经有2600多个 Star，如果按照 SpringBoot 标签进行筛选的话也可以排到第五位。

当云收藏1.0开发完成之后，同步将云收藏部署到了服务器上，申请了一个域名[www.favorites.ren](http://favorites.ren/)方便大家使用，到目前为止：网站的注册用户4000多人，共计收藏文章100000多条，在百度上搜索：云收藏，排在第一的就是云收藏的官网。2年多的时间这个数据其实也并不是很耀眼，但是作为一个学习 Spring Boot 的开源软件来讲，已经不错了。

云收藏的部署之路也挺曲折，刚开始的时候部署在我以前公司的服务器上，后来离职的时候在阿里云买了个1核1G的云服务器，因为安装了 Mysql、Redis、还有其它小软件导致服务器非常卡，那段时间访问云收藏的时候需要等待2-3秒才会有响应。

终于有一天自己也不能忍了，花钱把服务器升级到2核2G，访问速度虽有所提升但还是很不理想，那段时间工作很忙也没时间优化。网站的 Bug 也是一片，有时候还会突然中断服务几个小时，流失了一大批用户，甚至有人在 Github 上面留言说：看来微笑哥已经放弃云收藏了，我看了之后只能苦笑。

到了今年 Spring Boot 2.0 发布的时候，我就计划着把云收藏全面升级到2.0，顺便做一些优化让访问速度快一点。但一拖就是2个月，终于在前几个周末抽出了一点时间，将云收藏升级到了 Spring Boot 2.0 同时修复了一批显而易见的 Bug ,使用 Nginx 将静态图片等资源做了代理，当这些工作完全做完的时候，云收藏的访问速度明显得到了提升，大家可以访问[www.favorites.ren](http://favorites.ren/)体验一下。

将云收藏从 Spring Boot 1.0 升级到 2.0 的时候也遇到了一些问题，在修改的过程中记录下来，今天整理一下分享出来，方便后续升级的朋友少踩一些坑。

1、第一个问题：启动类报错

Spring Boot 部署到 Tomcat 中去启动时需要在启动类添加`SpringBootServletInitializer`，2.0 和 1.0 有区别。

``` java
// 1.0
import org.springframework.boot.web.support.SpringBootServletInitializer;
// 2.0
import org.springframework.boot.web.servlet.support.SpringBootServletInitializer;

@SpringBootApplication
public class UserManageApplication extends SpringBootServletInitializer {
    @Override
    protected SpringApplicationBuilder configure(SpringApplicationBuilder application) {
        return application.sources(UserManageApplication.class);
    }

    public static void main(String[] args) throws Exception {
        SpringApplication.run(UserManageApplication.class, args);
    }
}
```

这个问题好解决只需要重新导包就行。

2、日志类报错：Spring Boot 2.0 默认不包含 log4j，建议使用 slf4j 。

```
import org.apache.log4j.Logger;
protected Logger logger = Logger.getLogger(this.getClass());
```

改为：

```
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
protected Logger logger =  LoggerFactory.getLogger(this.getClass());
```

这个也比较好改动，就是需要替换的文件比较多。


3、Spring Boot 2.0 去掉了`findOne()`方法。

以前的`findOne()`方法其实就是根据传入的 Id 来查找对象，所以在 Spring Boot 2.0 的 Repository 中我们可以添加`findById(long id)`来替换使用。

例如：

```
User user=userRepository.findOne(Long id)
```

改为手动在`userRepository`手动添加`findById(long id)`方法，使用时将`findOne()`调用改为`findById(long id)`

```
User user=userRepository.findById(long id)
```

`delete()`方法和`findOne()`类似也被去掉了，可以使用`deleteById(Long id)`来替换，还有一个不同点是`deleteById(Long id)`默认实现返回值为`void`。

```
Long deleteById(Long id);
```

改为

```
//delete 改为 void 类型
void deleteById(Long id);
```

当然我们还有一种方案可以解决上述的两种变化，就是自定义 Sql，但是没有上述方案简单不建议使用。

```
@Query("select t from Tag t where t.tagId = :tagId")
Tag getByTagId(@Param("tagId") long tagId);
```


4、云收藏升级到 2.0 之后，插入数据会报错，错误信息如下：

```
org.springframework.dao.DataIntegrityViolationException: could not execute statement; SQL [n/a]; constraint [PRIMARY]; nested exception is org.hibernate.exception.ConstraintViolationException: could not execute statement
....
Caused by: org.hibernate.exception.ConstraintViolationException: could not execute statement
...
Caused by: com.mysql.jdbc.exceptions.jdbc4.MySQLIntegrityConstraintViolationException: Duplicate entry '299' for key 'PRIMARY'
```

这个问题稍稍花费了一点时间，报错提示的是主键冲突，跟踪数据库的数据发现并没有主键冲突，最后才发现是 Spring Boot 2.0 需要指定主键的自增策略，这个和 Spring Boot 1.0 有所区别，1.0 会使用默认的策略。

```
@Id
@GeneratedValue(strategy= GenerationType.IDENTITY)
private long id;
```

改动也比较简单，需要在所有的主键上面显示的指明自增策略。

5、Thymeleaf 3.0 默认不包含布局模块。

这个问题比较尴尬，当我将 Pom 包升级到 2.0 之后，访问首页的时候一片空白什么都没有，查看后台也没有任何的报错信息，首先尝试着跟踪了 http 请求，对比了一下也没有发现什么异常，在查询 Thymeleaf 3.0 变化时才发现：Spring Boot 2.0 中`spring-boot-starter-thymeleaf` 包默认并不包含布局模块，需要使用的时候单独添加，添加布局模块如下：

```
<dependency>
   <groupId>nz.net.ultraq.thymeleaf</groupId>
   <artifactId>thymeleaf-layout-dialect</artifactId>
</dependency>
```

改完之后再访问首页，一切正常，但是回头查看日志信息发现有一个告警信息：

```
2018-05-10 10:47:00.029  WARN 1536 --- [nio-8080-exec-2] n.n.u.t.decorators.DecoratorProcessor    : The layout:decorator/data-layout-decorator processor has been deprecated and will be removed in the next major version of the layout dialect.  Please use layout:decorate/data-layout-decorate instead to future-proof your code.  See https://github.com/ultraq/thymeleaf-layout-dialect/issues/95 for more information.
2018-05-10 10:47:00.154  WARN 1536 --- [nio-8080-exec-2] n.n.u.t.expressions.ExpressionProcessor  : Fragment expression "layout" is being wrapped as a Thymeleaf 3 fragment expression (~{...}) for backwards compatibility purposes.  This wrapping will be dropped in the next major version of the expression processor, so please rewrite as a Thymeleaf 3 fragment expression to future-proof your code.  See https://github.com/thymeleaf/thymeleaf/issues/451 for more information.
```

跟踪地址看了一下，大概的意思是以前布局的标签已经过期了，推荐使用新的标签来进行页面布局，解决方式也比较简单，修改以前的布局标签 `layout:decorator` 为 `layout:decorate`即可。

6、分页组件`PageRequest`变化。

在 Spring Boot 2.0 中 ，方法`new PageRequest(page, size, sort)` 已经过期不再推荐使用，推荐使用以下方式来构建分页信息：

```
Pageable pageable =PageRequest.of(page, size, Sort.by(Sort.Direction.ASC,"id"));
```

跟踪了一下源码发现`PageRequest.of()`方法，内部还是使用的`new PageRequest(page, size, sort)`，只是最新的写法更简洁一些。

```
public static PageRequest of(int page, int size, Sort sort) {
    return new PageRequest(page, size, sort);
}
```

7、关联查询时候组合返回对象的默认值有变化。

在使用 Spring Boot 1.0 时，使用 Jpa 关联查询时我们会构建一个接口对象来接收结果集，类似如下：

``` java
public interface CollectView{
   Long getId();
   Long getUserId();
   String getProfilePicture();
   String getTitle();
}
```

在使用 Spring Boot 1.0 时，如果没有查询到对应的字段会返回空，在 Spring Boot 2.0 中会直接报空指针异常，对结果集的检查会更加严格一些。

8、其它优化

前段时间在学习 Docker ，给云收藏添加了 Docker 、Docker Compose 支持让部署的时候更简单一些；同时修复了一些 bug，对于明显很消耗资源的功能进行了改进，部分功能添加了容错性；本次部署的时候使用了 Nginx 作为反向代理，因为使用了 WebJars 暂时不能使用 Nginx 代理 Js，所以将除过 Js 以外的其它资源都配置了缓存，；数据库由 Mysql 换成了 Mariadb。

以上就是云收藏从 Spring Boot 1.0 到 2.0 所做的一些小改进，做完这些工作之后惊喜的发现云收藏的访问速度比以前快了很多，虽然还有很大的优化空间，但日常使用基本上不会体验到太大的延迟。Spring Boot 2.0 中 Thymeleaf 默认使用了 3.0 ，数据库连接池默认使用了 Hikari ，这两个组件在性能上有很大的提升，同时也是提升云收藏访问速度的因素之一。

未来云收藏还会持续升级，后续会规划一些面向程序员的新功能，敬请期待！



