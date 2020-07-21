---
layout: post
title: Spring Boot 2 (五)：Docker Compose + Spring Boot + Nginx + Mysql 实践
category: springboot
tags: [springboot]
keywords: Spring Boot,Docker,Compose,Nginx,Mysql,docker
excerpt: 感受 Docker 魅力，排解决多应用部署之疼，Docker Compose + Spring Boot + Nginx + Mysql 实践
---

我知道大家这段时间看了我写关于 docker 相关的几篇文章，不疼不痒的，仍然没有感受 docker 的便利，是的，我也是这样认为的，I know your felling 。

前期了解概念什么的确实比较无聊，请不要着急精彩马上开始，当大家对 docker 相关概念有所了解之后，后面我会结合 Spring Boot 给大家来一系列的小例子，会让大家感受到使用 Docker 就是这么爽！

今天给大家演出的导演是 Docker 家族的 docker-compare ，主演是 Spring Boot、Nginx、Mysql 三位又红又紫的大碗，名导名演在一起的时候往往是准备搞事情，接下来又一场经典大片值得大家期待。

![](http://www.itmind.net/assets/images/2018/springboot/qifen.gif)

Spring Boot + Nginx + Mysql 是实际工作中最常用的一个组合，最前端使用 Nginx 代理请求转发到后端 Spring Boot 内嵌的 Tomcat 服务，Mysql 负责业务中数据相关的交互，那么在没有 docker 之前，我们是如何来搞定这些环境的呢？

- 1、安装 Nginx，配置 Nginx 相关信息，重启。
- 2、安装 Mysql ，配置字符集时区等信息，重启，最后初始化脚本。
- 3、启动 Spring Boot 项目，整体进行联调测试。

大家看我只写了三行，但其实搭建这些环境的时候还挺费事的，但这还不是结局，在用了一段时间时候需要迁移到另外一个环境，怎么办又需要重新搞一次？正常情况下，测试环境、SIT 环境、UAT 环境、生产环境！我们需要重复搭建四次。有人说不就是搭建四次吗？也没什么大不了的，那么我想告诉你，Too yong ,Too Simple 。

![](http://www.itmind.net/assets/images/2018/springboot/tooyang.jpg)

让我们看看以下几个因素：

第一，这只是一个最简单的案例，如果项目涉及到 MongoDB、Redis、ES ... 一些列的环境呢？
第二，如果你经常搭建环境或者调试程序，你就会知道什么是环境问题？有的时候明明是一模一样的配置，但是到了另外一个环境就是跑不起来。于是你花费很多时间来查找，最后才发现是少了一个参数或者逗号的问题，或者是系统内核版本不一致、或者你最后也没搞懂是为什么！只能再换另外一台服务器，那么使用 Docker 呢就可以完美的避开这些坑。

好了，废话不多说我们就开始吧！

## Spring Boot 案例

首先我们先准备一个 Spring Boot 使用 Mysql 的小场景，我们做这样一个示例，使用 Spring Boot 做一个 Web 应用，提供一个按照 IP 地址统计访问次数的方法，每次请求时将统计数据存入 Mysql 并展示到页面中。

### 配置信息

**依赖包**

``` xml
<dependencies>
     <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
	<dependency>
		<groupId>org.springframework.boot</groupId>
		<artifactId>spring-boot-starter-data-jpa</artifactId>
	</dependency>
	<dependency>
		<groupId>mysql</groupId>
		<artifactId>mysql-connector-java</artifactId>
	</dependency>
	<dependency>
		<groupId>org.springframework.boot</groupId>
		<artifactId>spring-boot-starter-test</artifactId>
		<scope>test</scope>
	</dependency>
</dependencies>
```

主要添加了 Spring Boot Web 支持，使用 Jpa 操作数据库、添加 Myql 驱动包等。

**配置文件**

``` xml
spring.datasource.url=jdbc:mysql://localhost:3306/test
spring.datasource.username=root
spring.datasource.password=root
spring.datasource.driver-class-name=com.mysql.jdbc.Driver

spring.jpa.properties.hibernate.hbm2ddl.auto=update
spring.jpa.properties.hibernate.dialect=org.hibernate.dialect.MySQL5InnoDBDialect
spring.jpa.show-sql=true
```

配置了数据库的链接信息，以及 Jpa 更新表模式、方言和是否显示Sql


### 核心代码

核心代码很简单，每过来一个请求，判断是否已经统计过，如果没有统计新增数据，如果有统计数据更新数据。

``` java
@RestController
public class VisitorController {

    @Autowired
    private VisitorRepository repository;
	
    @RequestMapping("/")
    public String index(HttpServletRequest request) {
        String ip=request.getRemoteAddr();
        Visitor visitor=repository.findByIp(ip);
        if(visitor==null){
            visitor=new Visitor();
            visitor.setIp(ip);
            visitor.setTimes(1);
        }else {
            visitor.setTimes(visitor.getTimes()+1);
        }
        repository.save(visitor);
        return "I have been seen ip "+visitor.getIp()+" "+visitor.getTimes()+" times.";
    }
}
```

实体类和 Repository 层代码比较简单，这里就不贴出来了，大家感兴趣可以下载源码查看。

以上内容都完成后，启动项目，访问：`http://localhost:8080/` 我们就可以看到这样的返回结果：

``` text
I have been seen ip 0:0:0:0:0:0:0:1 1 times.
```

再访问一次会变成

``` text
I have been seen ip 0:0:0:0:0:0:0:1 2 times.
```

多次访问一直叠加，说明演示项目开发完成。


## Docker 化改造

首先我们将目录改造成这样一个结构

![](http://www.itmind.net/assets/images/2018/springboot/mulu.png)

我们先从最外层说起：

- `docker-compose.yaml`：docker-compose 的核心文件，描述如何构建整个服务
- `nginx`：有关 nginx 的配置
- `app`：Spring Boot 项目地址

如果我们需要对 Mysql 有特殊的定制，也可以在最外层创建 mysql 文件夹，在此目录下进行配置。

### `docker-compose.yaml` 文件详解

``` xml
version: '3'
services:
  nginx:
   container_name: v-nginx
   image: nginx:1.13
   restart: always
   ports:
   - 80:80
   - 443:443
   volumes:
   - ./nginx/conf.d:/etc/nginx/conf.d
    
  mysql:
   container_name: v-mysql
   image: mysql/mysql-server:5.7
   environment:
    MYSQL_DATABASE: test
    MYSQL_ROOT_PASSWORD: root
    MYSQL_ROOT_HOST: '%'
   ports:
   - "3306:3306"
   restart: always
    
  app:
    restart: always
    build: ./app
    working_dir: /app
    volumes:
      - ./app:/app
      - ~/.m2:/root/.m2
    expose:
      - "8080"
    depends_on:
      - nginx
      - mysql
    command: mvn clean spring-boot:run -Dspring-boot.run.profiles=docker
```

- `version: '3'`： 表示使用第三代语法来构建 docker-compose.yaml 文件。
- `services`: 用来表示 compose 需要启动的服务，我们可以看出此文件中有三个服务分别为：nginx、mysql、app。
- `container_name`:  容器名称
- `environment`: 此节点下的信息会当作环境变量传入容器，此示例中 mysql 服务配置了数据库、密码和权限信息。
- `ports`: 表示对外开放的端口
- `restart: always` 表示如果服务启动不成功会一直尝试。
- `volumes`: 加载本地目录下的配置文件到容器目标地址下
- `depends_on`：可以配置依赖服务，表示需要先启动 `depends_on` 下面的服务后，再启动本服务。
- `command: mvn clean spring-boot:run -Dspring-boot.run.profiles=docker`: 表示以这个命令来启动项目，`-Dspring-boot.run.profiles=docker`表示使用 `application-docker.properties`文件配置信息进行启动。

### Nginx 文件解读

nginx 在目录下有一个文件 app.conf，主要配置了服务转发信息

``` xml
server {
    listen 80;
    charset utf-8;
    access_log off;

    location / {
        proxy_pass http://app:8080;
        proxy_set_header Host $host:$server_port;
        proxy_set_header X-Forwarded-Host $server_name;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static {
        access_log   off;
        expires      30d;

        alias /app/static;
    }
}
```

这块内容比较简单，配置请求转发，将80端口的请求转发到服务 app 的8080端口。其中`proxy_pass http://app:8080`这块的配置信息需要解释一下，这里使用是`app`而不是`localhost`，是因为他们没有在一个容器中，在一组 compose 的服务通讯需要使用 services 的名称进行访问。  

### Spring Boot 项目改造

在`app`目录下也就是和`pom.xm`文件同级添加`Dockerfile`文件，文件内容如下：

``` xml
FROM maven:3.5-jdk-8
```

只有一句，依赖于基础镜像`maven3.5`和`jdk 1.8`。因为在`docker-compose.yaml`文件设置了项目启动命令，这里不需要再添加启动命令。

在项目的`resources`目录下创建`application-dev.properties`和`application-docker.properties`文件

- `application-dev.properties` 中的配置信息和上面一致
- `application-docker.properties` 中的配置信息做稍微的改造，将数据库的连接信息由`jdbc:mysql://localhost:3306/test`改为`jdbc:mysql://mysql:3306/test` 。


这样我们所有的配置都已经完成。

## 部署

我们将项目拷贝到服务器中进行测试，服务器需要先安装 Docker 和 Docker Compos 环境，如果不了解的朋友可以查看我前面的两篇文章：

- [Docker(一)：Docker入门教程](http://www.ityouknow.com/docker/2018/03/07/docker-introduction.html)
- [Docker(四)：Docker 三剑客之 Docker Compose](http://www.ityouknow.com/docker/2018/03/22/docker-compose.html)

将项目拷贝到服务器中，进入目录`cd  dockercompose-springboot-mysql-nginx`

**启动服务：`docker-compose up`**

``` xml
[root@VM_73_217_centos dockercompose-springboot-mysql-nginx]# docker-compose up
Creating network "dockercomposespringbootmysqlnginx_default" with the default driver
Creating v-nginx ... done
Creating v-mysql ... done
Creating dockercomposespringbootmysqlnginx_app_1 ... done
Attaching to v-nginx, v-mysql, dockercomposespringbootmysqlnginx_app_1
v-mysql  | [Entrypoint] MySQL Docker Image 5.7.21-1.1.4
v-mysql  | [Entrypoint] Initializing database
app_1    | [INFO] Scanning for projects...
... 
app_1    | 2018-03-26 02:54:55.658  INFO 1 --- [           main] o.s.b.w.embedded.tomcat.TomcatWebServer  : Tomcat started on port(s): 8080 (http) with context path ''
app_1    | 2018-03-26 02:54:55.660  INFO 1 --- [           main] com.neo.ComposeApplication               : Started ComposeApplication in 14.869 seconds (JVM running for 30.202)
```

看到信息`Tomcat started on port(s): 8080`表示服务启动成功。也可以使用`docker-compose up -d`后台启动

访问服务器地址；`http://58.87.69.230/`，返回：`I have been seen ip 172.19.0.2 1 times.` 表示整体服务启动成功


**使用`docker-compose ps`查看项目中目前的所有容器**

``` text
[root@VM_73_217_centos dockercompose-springboot-mysql-nginx]# docker-compose ps
                 Name                                Command                  State                        Ports                  
----------------------------------------------------------------------------------------------------------------------------------
dockercomposespringbootmysqlnginx_app_1   /usr/local/bin/mvn-entrypo ...   Up             8080/tcp                                
v-mysql                                   /entrypoint.sh mysqld            Up (healthy)   0.0.0.0:3306->3306/tcp, 33060/tcp       
v-nginx                                   nginx -g daemon off;             Up             0.0.0.0:443->443/tcp, 0.0.0.0:80->80/tcp
```

可以看到项目中服务的状态、命令、端口等信息。

**关闭服务`docker-compose down`**

``` text
[root@VM_73_217_centos dockercompose-springboot-mysql-nginx]# docker-compose down
Stopping dockercomposespringbootmysqlnginx_app_1 ... done
Stopping visitor-nginx                           ... done
Stopping visitor-mysql                           ... done
Removing dockercomposespringbootmysqlnginx_app_1 ... done
Removing visitor-nginx                           ... done
Removing visitor-mysql                           ... done
```

### docker-compose 顺序

在使用 docker-compose 启动的时候经常会出现项目报 Mysql 连接异常，跟踪了一天终于发现了问题。 docker-compose 虽然可以通过`depends_on` 来定义服务启动的顺序，但是无法确定服务是否启动完成，因此会出现这样一个现象，Mysql 服务启动比较慢，当 Spring Boot 项目已经启动起来，但是 Mysql 还没有初始化好，这样当项目连接 Mysql 数据库的时候，就会出现连接数据库的异常。

针对这样的问题，有两种解决方案:

1、足够的容错和重试机制，比如连接数据库，在初次连接不上的时候，服务消费者可以不断重试，直到连接上服务。也就是在服务中定义： `restart: always`

2、同步等待，使用`wait-for-it.sh`或者其他`shell`脚本将当前服务启动阻塞，直到被依赖的服务加载完毕。这种方案后期可以尝试使用。


## 总结

没有对比就没有伤害，在没有使用 Docker 之前，我们需要搭建这样一个环境的话，需要安装 Nginx、Mysql ，再进行一系列的配置调试，还要担心各种环境问题；使用 Docker 之后简单两个命令就完成服务的上线、下线。

``` sh
docker-compose up
docker-compose down
```

其实容器技术对部署运维的优化还有很多，这只是刚刚开始，后面使用了 Swarm 才会真正感受到它的便利和强大。


**[示例代码-github](https://github.com/ityouknow/spring-boot-examples)**

**[示例代码-码云](https://gitee.com/ityouknow/spring-boot-examples)**


## 参考

[Docker Compose with Spring Boot, MySQL and NGINX](https://hellokoding.com/docker-compose-with-spring-boot-mysql-nginx/)  

