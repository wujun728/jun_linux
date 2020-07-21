---
layout: post
title: Spring Boot 2 (四)：使用 Docker 部署 Spring Boot
category: springboot
tags: [springboot]
keywords: Spring Boot,Docker,部署,docker
---

Docker 技术发展为微服务落地提供了更加便利的环境，使用 Docker 部署 Spring Boot 其实非常简单，这篇文章我们就来简单学习下。

首先构建一个简单的 Spring Boot 项目，然后给项目添加 Docker 支持，最后对项目进行部署。

## 一个简单 Spring Boot 项目

在 `pom.xml` 中 ，使用 Spring Boot 2.0 相关依赖

``` xml
<parent>
	<groupId>org.springframework.boot</groupId>
	<artifactId>spring-boot-starter-parent</artifactId>
	<version>2.0.0.RELEASE</version>
</parent>
```

添加 web 和测试依赖

``` xml
<dependencies>
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

创建一个 DockerController，在其中有一个`index()`方法，访问时返回：`Hello Docker!`


``` java
@RestController
public class DockerController {
	
    @RequestMapping("/")
    public String index() {
        return "Hello Docker!";
    }
}
```

启动类

``` java
@SpringBootApplication
public class DockerApplication {

	public static void main(String[] args) {
		SpringApplication.run(DockerApplication.class, args);
	}
}
```

添加完毕后启动项目，启动成功后浏览器放问：`http://localhost:8080/`，页面返回：`Hello Docker!`，说明 Spring Boot 项目配置正常。


## Spring Boot 项目添加 Docker 支持


在 `pom.xml-properties `中添加 Docker 镜像名称

``` xml
<properties>
	<docker.image.prefix>springboot</docker.image.prefix>
</properties>
```

plugins 中添加 Docker 构建插件：

``` xml
<build>
	<plugins>
		<plugin>
			<groupId>org.springframework.boot</groupId>
			<artifactId>spring-boot-maven-plugin</artifactId>
		</plugin>
		<!-- Docker maven plugin -->
		<plugin>
			<groupId>com.spotify</groupId>
			<artifactId>docker-maven-plugin</artifactId>
			<version>1.0.0</version>
			<configuration>
				<imageName>${docker.image.prefix}/${project.artifactId}</imageName>
				<dockerDirectory>src/main/docker</dockerDirectory>
				<resources>
					<resource>
						<targetPath>/</targetPath>
						<directory>${project.build.directory}</directory>
						<include>${project.build.finalName}.jar</include>
					</resource>
				</resources>
			</configuration>
		</plugin>
		<!-- Docker maven plugin -->
	</plugins>
</build>
```

在目录`src/main/docker`下创建 Dockerfile 文件，Dockerfile 文件用来说明如何来构建镜像。

``` text
FROM openjdk:8-jdk-alpine
VOLUME /tmp
ADD spring-boot-docker-1.0.jar app.jar
ENTRYPOINT ["java","-Djava.security.egd=file:/dev/./urandom","-jar","/app.jar"]
```

这个 Dockerfile 文件很简单，构建 Jdk 基础环境，添加 Spring Boot Jar 到镜像中，简单解释一下:

- FROM ，表示使用 Jdk8 环境 为基础镜像，如果镜像不是本地的会从 DockerHub 进行下载
- VOLUME ，VOLUME 指向了一个`/tmp`的目录，由于 Spring Boot 使用内置的Tomcat容器，Tomcat 默认使用`/tmp`作为工作目录。这个命令的效果是：在宿主机的`/var/lib/docker`目录下创建一个临时文件并把它链接到容器中的`/tmp`目录
- ADD ，拷贝文件并且重命名
- ENTRYPOINT ，为了缩短 Tomcat 的启动时间，添加`java.security.egd`的系统属性指向`/dev/urandom`作为 ENTRYPOINT

> 这样 Spring Boot 项目添加 Docker 依赖就完成了。


## 构建打包环境

我们需要有一个 Docker 环境来打包 Spring Boot 项目，在 Windows 搭建 Docker 环境很麻烦，因此我这里以 Centos 7 为例。

### 安装 Docker 环境
 
安装

``` sh
yum install docker
```

安装完成后，使用下面的命令来启动 docker 服务，并将其设置为开机启动：

``` sh
service docker start
chkconfig docker on

#LCTT 译注：此处采用了旧式的 sysv 语法，如采用CentOS 7中支持的新式 systemd 语法，如下：
systemctl  start docker.service
systemctl  enable docker.service
```

使用Docker 中国加速器

``` sh
vi  /etc/docker/daemon.json

#添加后：
{
    "registry-mirrors": ["https://registry.docker-cn.com"],
    "live-restore": true
}
```

重新启动docker

``` sh
systemctl restart docker
```

输入`docker version` 返回版本信息则安装正常。


###  安装JDK

``` sh
yum -y install java-1.8.0-openjdk*
```

配置环境变量
打开 `vim /etc/profile`
添加一下内容

``` sh
export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.161-0.b14.el7_4.x86_64 
export PATH=$PATH:$JAVA_HOME/bin 
```

修改完成之后，使其生效

``` sh
source /etc/profile
```

输入`java -version` 返回版本信息则安装正常。

###  安装MAVEN

下载：`http://mirrors.shu.edu.cn/apache/maven/maven-3/3.5.2/binaries/apache-maven-3.5.2-bin.tar.gz`

``` sh
## 解压
tar vxf apache-maven-3.5.2-bin.tar.gz
## 移动
mv apache-maven-3.5.2 /usr/local/maven3
```

修改环境变量， 在`/etc/profile`中添加以下几行

``` sh
MAVEN_HOME=/usr/local/maven3
export MAVEN_HOME
export PATH=${PATH}:${MAVEN_HOME}/bin
```

记得执行`source /etc/profile`使环境变量生效。

输入`mvn -version` 返回版本信息则安装正常。

> 这样整个构建环境就配置完成了。


## 使用 Docker 部署 Spring Boot 项目

将项目 `spring-boot-docker` 拷贝服务器中，进入项目路径下进行打包测试。

``` sh
#打包
mvn package
#启动
java -jar target/spring-boot-docker-1.0.jar
```

看到 Spring Boot 的启动日志后表明环境配置没有问题，接下来我们使用 DockerFile 构建镜像。

``` sh
mvn package docker:build
```

第一次构建可能有点慢，当看到以下内容的时候表明构建成功：

``` sh
...
Step 1 : FROM openjdk:8-jdk-alpine
 ---> 224765a6bdbe
Step 2 : VOLUME /tmp
 ---> Using cache
 ---> b4e86cc8654e
Step 3 : ADD spring-boot-docker-1.0.jar app.jar
 ---> a20fe75963ab
Removing intermediate container 593ee5e1ea51
Step 4 : ENTRYPOINT java -Djava.security.egd=file:/dev/./urandom -jar /app.jar
 ---> Running in 85d558a10cd4
 ---> 7102f08b5e95
Removing intermediate container 85d558a10cd4
Successfully built 7102f08b5e95
[INFO] Built springboot/spring-boot-docker
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
[INFO] Total time: 54.346 s
[INFO] Finished at: 2018-03-13T16:20:15+08:00
[INFO] Final Memory: 42M/182M
[INFO] ------------------------------------------------------------------------
```

使用`docker images`命令查看构建好的镜像：

``` sh
docker images
REPOSITORY                      TAG                 IMAGE ID            CREATED             SIZE
springboot/spring-boot-docker   latest              99ce9468da74        6 seconds ago       117.5 MB
```

`springboot/spring-boot-docker` 就是我们构建好的镜像，下一步就是运行该镜像

``` sh
docker run -p 8080:8080 -t springboot/spring-boot-docker
```

启动完成之后我们使用`docker ps`查看正在运行的镜像：

``` sh
docker ps
CONTAINER ID        IMAGE                           COMMAND                  CREATED             STATUS              PORTS                    NAMES
049570da86a9        springboot/spring-boot-docker   "java -Djava.security"   30 seconds ago      Up 27 seconds       0.0.0.0:8080->8080/tcp   determined_mahavira
```

可以看到我们构建的容器正在在运行，访问浏览器：`http://192.168.0.x:8080/`,返回

``` sh
Hello Docker!
```

说明使用 Docker 部署 Spring Boot 项目成功！


**[示例代码-github](https://github.com/ityouknow/spring-boot-examples)**

**[示例代码-码云](https://gitee.com/ityouknow/spring-boot-examples)**


## 参考

[Spring Boot with Docker](https://spring.io/guides/gs/spring-boot-docker/)  
[Docker：Spring Boot 应用发布到 Docker](https://lw900925.github.io/docker/docker-springboot.html)  


