# SpringCloudAlibaba微服务docker容器打包和部署示例实战



# 概述

我们使用前面《SpringCloudAlibaba注册中心与配置中心之利器[Nacos](https://so.csdn.net/so/search?q=Nacos&spm=1001.2101.3001.7020)实战与源码分析（中）》的两个微服务示例，分别是库存微服务和订单微服务，基于Nacos注册中心和配置中心的使用，前面Nacos我们已基于dock-compose方式部署，我们增加配置数据，这里我们暂时也不把数据打包进去，各位可以直接将容器以dokcer export方式导入为镜像，微服务使用订单、库存MySQL数据库暂时也不单独做成镜像，各位可以做成SQL脚本执行导入方式。

# 整体工程结构

- docker目录docker compose编排脚本目录
  - bin目录：包含初始化脚本、启动脚本、停止脚本、更新脚本
  - env目录：存在为微服务环境变量
  - yaml目录：存在全局环境脚本变量、微服务docker-compose脚本
- 库存微服务
  - bin目录：存在微服务启动脚本
  - conf目录：存在启动配置文件和日志配置文件
  - Dockerfile文件
- 订单微服务
  - bin目录：存在微服务启动脚本
  - conf目录：存在启动配置文件和日志配置文件
  - Dockerfile文件

![image-20220419112440637](https://img-blog.csdnimg.cn/img_convert/5c7da98ba8a1b9374d8d73451aea2408.png)

# 库存[微服务](https://so.csdn.net/so/search?q=微服务&spm=1001.2101.3001.7020)

## 编写配置文件

bootstrap.yml

```ruby
spring:



  application:



    name: ecom-storage-service



  profiles:



    active: ${SPRING_PROFILES_ACTIVE:"dev"}



  main:



    allow-circular-references: true



  cloud:



    nacos:



      # 注册中心信息放在配置中心上，每个程序一般只配置配置中心的信息



      server-addr: ${NACOS_CONFIG_SERVER:"192.168.50.95:8848"}



      config:



        server-addr: ${spring.cloud.nacos.server-addr}



        file-extension: yaml



        namespace: ${NACOS_CONFIG_NAMESPACE:"a2b1a5b7-d0bc-48e8-ab65-04695e61db01"}



        group: ${NACOS_CONFIG_GROUP:"storage-group"}



        extension-configs:



          - dataId: extension-priority-dev.yaml



            group: extension-group



            refresh: true



          - dataId: commons-dev.yaml



            group: commons-group



            refresh: true



        shared-configs:



          - dataId: shared-priority-dev.yaml



            group: shared-group



            refresh: true



        username: itsx



        password: itxs123



        enabled: true # 默认为true，设置false 来完全关闭 Spring Cloud Nacos Config



        refresh-enabled: true # 默认为true，当变更配置时，应用程序中能够获取到最新的值，设置false来关闭动态刷新，我们使用注册中心场景大部分就是动态感知，因此基本使用默认的



 
```

logback.xml

```xml
<?xml version="1.0" encoding="UTF-8" ?>



<configuration debug="false">



    <!--定义日志文件的存储地址 勿在 LogBack 的配置中使用相对路径-->



    <springProperty scope="context" name="APP_HOME" source="spring.application.name"/>



    <property name="LOG_HOME" value="${LOG_PATH:-.}" />



    <!-- 控制台输出设置 -->



    <!-- 彩色日志格式，magenta：洋红，boldMagenta：粗红，yan：青色，·⊱══> -->



    <property name="CONSOLE_LOG_PATTERN" value="%boldMagenta([%d{yyyy-MM-dd HH:mm:ss.SSS}]) %cyan([%X{requestId}]) %boldMagenta(%-5level) %blue(%logger{15}) %red([%thread]) %magenta(·⊱══>) %cyan(%msg%n)"/>



    <appender name="CONSOLE" class="ch.qos.logback.core.ConsoleAppender">



        <encoder>



            <pattern>${CONSOLE_LOG_PATTERN}</pattern>



            <charset>utf8</charset>



        </encoder>



    </appender>



    <!-- 按天输出日志设置 -->



    <appender name="DAY_FILE" class="ch.qos.logback.core.rolling.RollingFileAppender">



        <rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy">



            <!-- 日志文件输出的文件名 -->



            <FileNamePattern>${LOG_HOME}/%d{yyyy-MM-dd}_${APP_HOME}.%i.log</FileNamePattern>



            <!-- 日志文件保留天数 -->



            <MaxHistory>7</MaxHistory>



            <timeBasedFileNamingAndTriggeringPolicy class="ch.qos.logback.core.rolling.SizeAndTimeBasedFNATP">



                <maxFileSize>50MB</maxFileSize>



            </timeBasedFileNamingAndTriggeringPolicy>



        </rollingPolicy>



        <filter class="ch.qos.logback.classic.filter.LevelFilter">



            <level>INFO</level>             <!-- 设置拦截的对象为INFO级别日志 -->



            <onMatch>ACCEPT</onMatch>       <!-- 当遇到了INFO级别时，启用改段配置 -->



            <onMismatch>DENY</onMismatch>   <!-- 没有遇到INFO级别日志时，屏蔽改段配置 -->



        </filter>



        <encoder class="ch.qos.logback.classic.encoder.PatternLayoutEncoder">



            <!-- 格式化输出：%d表示日期，%thread表示线程名，%-5level：级别从左显示5个字符宽度%msg：日志消息，%n是换行符 -->



            <pattern>%d{yyyy-MM-dd HH:mm:ss.SSS} [%thread] %-5level %logger{50} - %msg%n</pattern>



        </encoder>



    </appender>



    <!-- 按天输出WARN级别日志设置 -->



    <appender name="DAY_WARN_FILE" class="ch.qos.logback.core.rolling.RollingFileAppender">



        <rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy">



            <!-- 日志文件输出的文件名 -->



            <FileNamePattern>${LOG_HOME}/%d{yyyy-MM-dd}_${APP_HOME}_warn.%i.log</FileNamePattern>



            <!-- 日志文件保留天数 -->



            <MaxHistory>7</MaxHistory>



            <timeBasedFileNamingAndTriggeringPolicy class="ch.qos.logback.core.rolling.SizeAndTimeBasedFNATP">



                <maxFileSize>50MB</maxFileSize>



            </timeBasedFileNamingAndTriggeringPolicy>



        </rollingPolicy>



        <filter class="ch.qos.logback.classic.filter.LevelFilter">



            <level>WARN</level>             <!-- 设置拦截的对象为INFO级别日志 -->



            <onMatch>ACCEPT</onMatch>       <!-- 当遇到了INFO级别时，启用改段配置 -->



            <onMismatch>DENY</onMismatch>   <!-- 没有遇到INFO级别日志时，屏蔽改段配置 -->



        </filter>



        <encoder class="ch.qos.logback.classic.encoder.PatternLayoutEncoder">



            <!-- 格式化输出：%d表示日期，%thread表示线程名，%-5level：级别从左显示5个字符宽度%msg：日志消息，%n是换行符 -->



            <pattern>%d{yyyy-MM-dd HH:mm:ss.SSS} [%thread] %-5level %logger{50} - %msg%n</pattern>



        </encoder>



    </appender>



    <!-- 按天输出ERROR级别日志设置 -->



    <appender name="DAY_ERROR_FILE" class="ch.qos.logback.core.rolling.RollingFileAppender">



        <rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy">



            <!-- 日志文件输出的文件名 -->



            <FileNamePattern>${LOG_HOME}/%d{yyyy-MM-dd}_${APP_HOME}_error.%i.log</FileNamePattern>



            <!-- 日志文件保留天数 -->



            <MaxHistory>7</MaxHistory>



            <timeBasedFileNamingAndTriggeringPolicy class="ch.qos.logback.core.rolling.SizeAndTimeBasedFNATP">



                <maxFileSize>50MB</maxFileSize>



            </timeBasedFileNamingAndTriggeringPolicy>



        </rollingPolicy>



        <filter class="ch.qos.logback.classic.filter.LevelFilter">



            <level>ERROR</level>            <!-- 设置拦截的对象为ERROR级别日志 -->



            <onMatch>ACCEPT</onMatch>       <!-- 当遇到了ERROR级别时，启用改段配置 -->



            <onMismatch>DENY</onMismatch>   <!-- 没有遇到ERROR级别日志时，屏蔽改段配置 -->



        </filter>



        <encoder class="ch.qos.logback.classic.encoder.PatternLayoutEncoder">



            <!-- 格式化输出：%d表示日期，%thread表示线程名，%-5level：级别从左显示5个字符宽度%msg：日志消息，%n是换行符 -->



            <pattern>%d{yyyy-MM-dd HH:mm:ss.SSS} [%thread] %-5level %logger{50} - %msg%n</pattern>



        </encoder>



    </appender>



 



    <!-- 日志输出级别，OFF level > FATAL > ERROR > WARN > INFO > DEBUG > ALL level -->



    <logger name="com.sand" level="INFO"/>



    <logger name="com.apache.ibatis" level="INFO"/>



    <logger name="java.sql.Statement" level="INFO"/>



    <logger name="java.sql.Connection" level="INFO"/>



    <logger name="java.sql.PreparedStatement" level="INFO"/>



    <logger name="org.springframework" level="WARN"/>



    <logger name="com.baomidou.mybatisplus" level="WARN"/>



 



    <!-- 开发环境：打印控制台和输出到文件 -->



    <springProfile name="dev">



        <root level="INFO">



            <appender-ref ref="CONSOLE"/>



            <appender-ref ref="DAY_FILE"/>



            <appender-ref ref="DAY_WARN_FILE"/>



            <appender-ref ref="DAY_ERROR_FILE"/>



        </root>



    </springProfile>



 



    <!-- 生产环境：打印控制台和输出到文件 -->



    <springProfile name="pro">



        <root level="INFO">



            <appender-ref ref="CONSOLE"/>



            <appender-ref ref="DAY_FILE"/>



            <appender-ref ref="DAY_WARN_FILE"/>



            <appender-ref ref="DAY_ERROR_FILE"/>



        </root>



    </springProfile>



</configuration>
```

## 制作[Docker](https://so.csdn.net/so/search?q=Docker&spm=1001.2101.3001.7020)启动脚本

docker-startup.sh

```bash
#!/bin/bash



set -x



export CUSTOM_SEARCH_NAMES="application,custom"



export CUSTOM_SEARCH_LOCATIONS=${BASE_DIR}/init.d/,file:${BASE_DIR}/conf/



 



JAVA_OPT="${JAVA_OPT} -Dsimple_ecommerce.home=${BASE_DIR}"



JAVA_OPT="${JAVA_OPT} -jar ${BASE_DIR}/target/ecom-storage-service.jar"



JAVA_OPT="${JAVA_OPT} ${JAVA_OPT_EXT}"



JAVA_OPT="${JAVA_OPT} --spring.config.additional-location=${CUSTOM_SEARCH_LOCATIONS}"



JAVA_OPT="${JAVA_OPT} --spring.config.name=${CUSTOM_SEARCH_NAMES}"



JAVA_OPT="${JAVA_OPT} --logging.config=${BASE_DIR}/conf/logback.xml"



JAVA_OPT="${JAVA_OPT} --logging.file.path=${BASE_DIR}/logs/"



JAVA_OPT="${JAVA_OPT} --spring.config.location=${BASE_DIR}/conf/bootstrap.yml"



JAVA_OPT="${JAVA_OPT} --server.max-http-header-size=524288"



 



echo "ecom-storage-service is starting, you can docker logs your container"



exec $JAVA ${JAVA_OPT}
```

## 制作Dockerfile文件

Dockerfile文件

```bash
FROM java:8



MAINTAINER itxs "107734588@qq.com"



 



ARG ECOM_STORAGE_SERVICE_VERSION=1.0



ARG ECOM_STORAGE_SERVICE_DIR="ecom-storage-service"



ARG ECOM_STORAGE_SERVICE_PACKAGE="ecom-storage-service-$ECOM_STORAGE_SERVICE_VERSION.jar"



ARG ECOM_STORAGE_SERVICE_PROGRAM="ecom-storage-service.jar"



 



# set environment



ENV BASE_DIR="/home/simple_ecommerce/${ECOM_STORAGE_SERVICE_DIR}" \



    CLASSPATH=".:/home/simple_ecommerce/${ECOM_STORAGE_SERVICE_DIR}/conf:$CLASSPATH" \



    JAVA_HOME="/usr/lib/jvm/java-8-openjdk-amd64" \



    JAVA="/usr/lib/jvm/java-8-openjdk-amd64/bin/java" \



    JAVA_OPT_EXT="${JAVA_OPT_EXT}" \



    TIME_ZONE="Asia/Shanghai"



 



WORKDIR $BASE_DIR



 



ADD ./target/$ECOM_STORAGE_SERVICE_PACKAGE target/$ECOM_STORAGE_SERVICE_PROGRAM



RUN ln -snf /usr/share/zoneinfo/$TIME_ZONE /etc/localtime && echo $TIME_ZONE > /etc/timezone



 



ADD bin/docker-startup.sh bin/docker-startup.sh



ADD conf/bootstrap.yml conf/bootstrap.yml



ADD conf/logback.xml conf/logback.xml



RUN mkdir -p init.d



 



# set startup log dir



RUN mkdir -p logs \



        && cd logs \



        && touch start.out \



        && ln -sf /dev/stdout start.out \



        && ln -sf /dev/stderr start.out



RUN chmod +x bin/docker-startup.sh



 



EXPOSE 4080



ENTRYPOINT ["bin/docker-startup.sh"]
```

## 打包配置

库存微服务pom文件添加docker-maven-plugin

```xml
<?xml version="1.0" encoding="UTF-8"?>



<project xmlns="http://maven.apache.org/POM/4.0.0"



         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"



         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">



    <parent>



        <artifactId>simple-ecommerce</artifactId>



        <groupId>cn.itxs</groupId>



        <version>1.0</version>



    </parent>



    <modelVersion>4.0.0</modelVersion>



 



    <artifactId>ecom-storage-service</artifactId>



    <packaging>jar</packaging>



    <version>1.0</version>



    <name>ecom-storage-service</name>



    <description>a simple electronic commerce platform demo tutorial for storage service</description>



 



    <dependencies>



        <dependency>



            <groupId>cn.itxs</groupId>



            <artifactId>ecom-commons</artifactId>



        </dependency>



        <dependency>



            <groupId>org.projectlombok</groupId>



            <artifactId>lombok</artifactId>



            <scope>provided</scope>



        </dependency>



    </dependencies>



 



    <build>



        <plugins>



            <plugin>



                <groupId>org.springframework.boot</groupId>



                <artifactId>spring-boot-maven-plugin</artifactId>



                <configuration>



                    <!-- 指定该Main Class为全局的唯一入口 -->



                    <mainClass>cn.itxs.ecom.storage.StorageServiceApplication</mainClass>



                    <layout>ZIP</layout>



                </configuration>



                <executions>



                    <execution>



                        <goals>



                            <goal>repackage</goal><!--可以把依赖的包都打包到生成的Jar包中-->



                        </goals>



                    </execution>



                </executions>



            </plugin>



 



            <plugin>



                <groupId>io.fabric8</groupId>



                <artifactId>docker-maven-plugin</artifactId>



                <version>0.39.1</version>



                <configuration>



                    <authConfig>



                        <!-- registry服务的认证-->



                        <username>admin</username>



                        <password>admin12345</password>



                    </authConfig>



                    <images>



                        <image>



                            <!-- 指定image的名字（包含registry地址）-->



                            <name>simple_ecommerce/${project.name}:${project.version}</name>



                            <!--registry地址,用于推送,拉取镜像-->



                            <registry>registry.itxs.cn</registry>



                            <!-- 别名为master，不关键-->



                            <alias>master</alias>



                            <build>



                                <!-- 指定dockerfile文件的位置-->



                                <dockerFile>${project.basedir}/Dockerfile</dockerFile>



                                <buildOptions>



                                    <!-- 网络的配置，与宿主主机共端口号-->



                                    <network>host</network>



                                </buildOptions>



                            </build>



                        </image>



                    </images>



                </configuration>



 



                <executions>



                    <execution>



                        <id>docker-exec</id>



                        <!-- 绑定mvn install阶段，当执行mvn install时 就会执行docker build 和docker push-->



                        <phase>install</phase>



                        <goals>



                            <goal>build</goal>



                            <goal>push</goal>



                        </goals>



                    </execution>



                </executions>



            </plugin>



        </plugins>



    </build>



 



</project>
```

可以看到库存微服务pom文件添加docker-maven-plugin，mvn install阶段，当执行mvn install时 就会执行docker build 和docker push，我们前面也介绍Docker Harbor私有仓库的部署，可以通过插件直接推送内网的Harbor私有仓库里。

# 订单微服务

## 编写配置文件

bootstrap.yml

```ruby
spring:



  application:



    name: ecom-order-service



  profiles:



    active: dev



  main:



    allow-circular-references: true



  cloud:



    # 负载均衡器缓存



    loadbalancer:



      cache:



        enabled: true



        caffeine:



          spec: initialCapacity=500,expireAfterWrite=5s



    nacos:



      # 注册中心信息放在配置中心上，每个程序一般只配置配置中心的信息



      server-addr: ${NACOS_CONFIG_SERVER:"192.168.50.95:8848"}



      config:



        server-addr: ${spring.cloud.nacos.server-addr}



        file-extension: yaml



        namespace: ${NACOS_CONFIG_NAMESPACE:"a2b1a5b7-d0bc-48e8-ab65-04695e61db01"}



        group: ${NACOS_CONFIG_GROUP:"order-group"}



        username: itsx



        password: itxs123



        extension-configs:



          - dataId: commons-dev.yaml



            group: commons-group



            refresh: true



        enabled: true # 默认为true，设置false 来完全关闭 Spring Cloud Nacos Config



        refresh-enabled: true # 默认为true，当变更配置时，应用程序中能够获取到最新的值，设置false来关闭动态刷新，我们使用注册中心场景大部分就是动态感知，因此基本使用默认的
```

## 制作Docker启动脚本

docker-startup.sh

```bash
#!/bin/bash



set -x



export CUSTOM_SEARCH_NAMES="application,custom"



export CUSTOM_SEARCH_LOCATIONS=${BASE_DIR}/init.d/,file:${BASE_DIR}/conf/



 



JAVA_OPT="${JAVA_OPT} -Dsimple_ecommerce.home=${BASE_DIR}"



JAVA_OPT="${JAVA_OPT} -jar ${BASE_DIR}/target/ecom-order-service.jar"



JAVA_OPT="${JAVA_OPT} ${JAVA_OPT_EXT}"



JAVA_OPT="${JAVA_OPT} --spring.config.additional-location=${CUSTOM_SEARCH_LOCATIONS}"



JAVA_OPT="${JAVA_OPT} --spring.config.name=${CUSTOM_SEARCH_NAMES}"



JAVA_OPT="${JAVA_OPT} --logging.config=${BASE_DIR}/conf/logback.xml"



JAVA_OPT="${JAVA_OPT} --logging.file.path=${BASE_DIR}/logs/"



JAVA_OPT="${JAVA_OPT} --spring.config.location=${BASE_DIR}/conf/bootstrap.yml"



JAVA_OPT="${JAVA_OPT} --server.max-http-header-size=524288"



 



echo "ecom-order-service is starting, you can docker logs your container"



exec $JAVA ${JAVA_OPT}
```

## 制作Dockerfile文件

Dockerfile文件

```bash
FROM java:8



MAINTAINER itxs "107734588@qq.com"



 



ARG ECOM_ORDER_SERVICE_VERSION=1.0



ARG ECOM_ORDER_SERVICE_DIR="ecom-order-service"



ARG ECOM_ORDER_SERVICE_PACKAGE="ecom-order-service-$ECOM_ORDER_SERVICE_VERSION.jar"



ARG ECOM_ORDER_SERVICE_PROGRAM="ecom-order-service.jar"



 



# set environment



ENV BASE_DIR="/home/simple_ecommerce/${ECOM_ORDER_SERVICE_DIR}" \



    CLASSPATH=".:/home/simple_ecommerce/${ECOM_ORDER_SERVICE_DIR}/conf:$CLASSPATH" \



    JAVA_HOME="/usr/lib/jvm/java-8-openjdk-amd64" \



    JAVA="/usr/lib/jvm/java-8-openjdk-amd64/bin/java" \



    JAVA_OPT_EXT="${JAVA_OPT_EXT}" \



    TIME_ZONE="Asia/Shanghai"



 



WORKDIR $BASE_DIR



 



ADD ./target/$ECOM_ORDER_SERVICE_PACKAGE target/$ECOM_ORDER_SERVICE_PROGRAM



RUN ln -snf /usr/share/zoneinfo/$TIME_ZONE /etc/localtime && echo $TIME_ZONE > /etc/timezone



 



ADD bin/docker-startup.sh bin/docker-startup.sh



ADD conf/bootstrap.yml conf/bootstrap.yml



ADD conf/logback.xml conf/logback.xml



RUN mkdir -p init.d



 



# set startup log dir



RUN mkdir -p logs \



        && cd logs \



        && touch start.out \



        && ln -sf /dev/stdout start.out \



        && ln -sf /dev/stderr start.out



RUN chmod +x bin/docker-startup.sh



 



EXPOSE 4070



ENTRYPOINT ["bin/docker-startup.sh"]
```

## 打包配置

订单微服务pom文件添加docker-maven-plugin

```xml
<?xml version="1.0" encoding="UTF-8"?>



<project xmlns="http://maven.apache.org/POM/4.0.0"



         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"



         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">



    <parent>



        <artifactId>simple-ecommerce</artifactId>



        <groupId>cn.itxs</groupId>



        <version>1.0</version>



    </parent>



    <modelVersion>4.0.0</modelVersion>



 



    <artifactId>ecom-order-service</artifactId>



    <packaging>jar</packaging>



    <version>1.0</version>



    <name>ecom-order-service</name>



    <description>a simple electronic commerce platform demo tutorial for order service</description>



 



    <dependencies>



        <dependency>



            <groupId>cn.itxs</groupId>



            <artifactId>ecom-commons</artifactId>



        </dependency>



        <dependency>



            <groupId>org.projectlombok</groupId>



            <artifactId>lombok</artifactId>



            <scope>provided</scope>



        </dependency>



        <dependency>



            <groupId>com.github.ben-manes.caffeine</groupId>



            <artifactId>caffeine</artifactId>



            <version>3.0.6</version>



        </dependency>



    </dependencies>



 



    <build>



        <plugins>



            <plugin>



                <groupId>org.springframework.boot</groupId>



                <artifactId>spring-boot-maven-plugin</artifactId>



                <configuration>



                    <!-- 指定该Main Class为全局的唯一入口 -->



                    <mainClass>cn.itxs.ecom.order.OrderServiceApplication</mainClass>



                    <layout>ZIP</layout>



                </configuration>



                <executions>



                    <execution>



                        <goals>



                            <goal>repackage</goal><!--可以把依赖的包都打包到生成的Jar包中-->



                        </goals>



                    </execution>



                </executions>



            </plugin>



 



            <plugin>



                <groupId>io.fabric8</groupId>



                <artifactId>docker-maven-plugin</artifactId>



                <version>0.39.1</version>



                <configuration>



                    <authConfig>



                        <!-- registry服务的认证-->



                        <username>admin</username>



                        <password>admin12345</password>



                    </authConfig>



                    <images>



                        <image>



                            <!-- 指定image的名字（包含registry地址）-->



                            <name>simple_ecommerce/${project.name}:${project.version}</name>



                            <!--registry地址,用于推送,拉取镜像-->



                            <registry>registry.itxs.cn</registry>



                            <!-- 别名为master，不关键-->



                            <alias>master</alias>



                            <build>



                                <!-- 指定dockerfile文件的位置-->



                                <dockerFile>${project.basedir}/Dockerfile</dockerFile>



                                <buildOptions>



                                    <!-- 网络的配置，与宿主主机共端口号-->



                                    <network>host</network>



                                </buildOptions>



                            </build>



                        </image>



                    </images>



                </configuration>



 



                <executions>



                    <execution>



                        <id>docker-exec</id>



                        <!-- 绑定mvn install阶段，当执行mvn install时 就会执行docker build 和docker push-->



                        <phase>install</phase>



                        <goals>



                            <goal>build</goal>



                            <goal>push</goal>



                        </goals>



                    </execution>



                </executions>



            </plugin>



        </plugins>



    </build>



 



</project>
```

上面订单微服务pom文件添加docker-maven-plugin，mvn install阶段，当执行mvn install时 就会执行docker build 和docker push，我们前面也介绍Docker Harbor私有仓库的部署，可以通过插件直接推送内网的Harbor私有仓库里。

# 打包

```crystal
# 由于需要进行docker build 和docker push，打包机器需要安装docker，直接执行mvn clean install 即可，如果需要单独mvn clean install# 如果是单独针对库存微服务只进行docker build，可以进入库存微服务目录mvn clean package docker:bulid
```

docker build两个微服务的镜像文件如下，这个是我单独docker build没有push.如果install的话上传内网Harbor仓库本地先生成镜像，然后再上传最后删除本地的镜像。

![image-20220419152731637](https://img-blog.csdnimg.cn/img_convert/028fc3e6f801d765df6bb9f62000f4cd.png)

# 部署

## env目录

订单微服务环境变量ecom-order-service.env，这里NACOS_CONFIG_SERVER简单先用地址，如果是在单个宿主机或者K8s环境下，并且在同个容器网络内可以直接使用容器名，可不需要Nacos地址配置，这里我们就先用暴露宿主机端口，先重点放在两个微服务容器上。

```sql
SPRING_PROFILES_ACTIVE=dev



NACOS_CONFIG_SERVER=192.168.50.95:8848



NACOS_CONFIG_NAMESPACE=a2b1a5b7-d0bc-48e8-ab65-04695e61db01



NACOS_CONFIG_GROUP=order-group



JAVA_OPT_EXT="-XX:+PrintGCDetails -XX:+PrintGCDateStamps -Xms1024m -Xmx1024m -Xmn1024m -XX:-UseAdaptiveSizePolicy -XX:SurvivorRatio=4 -XX:+UseParNewGC -XX:+UseConcMarkSweepGC -XX:-CMSConcurrentMTEnabled -XX:CMSInitiatingOccupancyFraction=70 -XX:+CMSParallelRemarkEnabled -XX:MetaspaceSize=256m -XX:MaxMetaspaceSize=256m"
```

库存微服务环境变量ecom-storage-service.env

```sql
SPRING_PROFILES_ACTIVE=dev



NACOS_CONFIG_SERVER=192.168.50.95:8848



NACOS_CONFIG_NAMESPACE=a2b1a5b7-d0bc-48e8-ab65-04695e61db01



NACOS_CONFIG_GROUP=storage-group



JAVA_OPT_EXT="-XX:+PrintGCDetails -XX:+PrintGCDateStamps -Xms1024m -Xmx1024m -Xmn1024m -XX:-UseAdaptiveSizePolicy -XX:SurvivorRatio=4 -XX:+UseParNewGC -XX:+UseConcMarkSweepGC -XX:-CMSConcurrentMTEnabled -XX:CMSInitiatingOccupancyFraction=70 -XX:+CMSParallelRemarkEnabled -XX:MetaspaceSize=256m -XX:MaxMetaspaceSize=256m"
```

## 制作Docker-Compose编排文件

我这里做法没有将多个微服务编排的一个Docker-Compose文件里，而已单独做一个Docker-Compose，通过shell脚本串联起来执行，各位也可以直接编写一个Docker-Compose

全局环境变量.env存放全局参数信息，例如各微服务的版本信息

```undefined
ECOM_STORAGE_VERSION=1.0ECOM_ORDER_VERSION=1.0
```

库存微服务Docker-Compose文件ecom-storage-service.yml,如果是本地build则image去掉registry.itxs.cn/

```ruby
version: "3"



services:



  ecom-storage-service:



    image: registry.itxs.cn/simple_ecommerce/ecom-storage-service:${ECOM_STORAGE_VERSION}



    container_name: ecom-storage-service



    env_file:



      - ../env/ecom-storage-service.env



    volumes:



      - ../logs/ecom-storage-service/:/home/simple_ecommerce/ecom-storage-service/logs



    ports:



      - "4080:4080"



    networks:



      - simple_ecommerce



    restart: always



networks:



  simple_ecommerce:



    external: true
```

订单微服务Docker-Compose文件ecom-order-service.yml

```ruby
version: "3"



services:



  ecom-order-service:



    image: registry.itxs.cn/simple_ecommerce/ecom-order-service:${ECOM_ORDER_VERSION}



    container_name: ecom-order-service



    env_file:



      - ../env/ecom-order-service.env



    volumes:



      - ../logs/ecom-order-service/:/home/simple_ecommerce/ecom-order-service/logs



    ports:



      - "4070:4070"



    networks:



      - simple_ecommerce



    restart: always



networks:



  simple_ecommerce:



    external: true
```

## 部署脚本

bin目录下我们创建操作脚本，init.sh初始化检查环境、安装docker和docker-compose、

```bash
#!/usr/bin/env bash



 



echo "############当前操作系统版本##############"



if ! type yum >/dev/null 2>&1; then



        echo "【ERROR】目前脚本仅支持CentOS7.X系统"



        exit 8



else



        osVersion=$(echo `cat /etc/redhat-release | sed -r 's/.* ([0-9]+)\..*/\1/'`)



        if [[ "$osVersion" != "7" ]]; then



             echo "【ERROR】目前脚本仅支持CentOS7.X系统"



             exit 8



        else



             echo '版本校验成功' 



        fi



fi



 



echo "############判断是否安装了docker##############"



if ! type docker >/dev/null 2>&1; then



    echo 'docker 未安装';



	  echo '开始安装Docker....';



    yum install -y yum-utils



    yum-config-manager \



          --add-repo \



          https://download.docker.com/linux/centos/docker-ce.repo



 



    #安装docker核心引擎、命令行客户端、容器



    yum install docker-ce docker-ce-cli containerd.io



    echo 'docker 安装完毕';



    #启动docker



	  echo '配置Docker开启启动';



	  systemctl enable docker



	  systemctl start docker



 



cat >> /etc/docker/daemon.json << EOF



{



  "registry-mirrors": ["https://b9pmyelo.mirror.aliyuncs.com"]



}



EOF



	  systemctl restart docker



else



    echo 'docker 安装完毕';



fi



 



echo "############判断是否安装了wget##############"



if ! type wget >/dev/null 2>&1; then



    echo 'wget 未安装';



	  echo '开始安装wget....';



	  yum -y install wget



else



    echo 'wget 已安装';



fi



 



echo "############判断是否安装了dos2unix##############"



if ! type dos2unix >/dev/null 2>&1; then



    echo 'dos2unix 未安装';



	  echo '开始安装dos2unix....';



	  yum -y install dos2unix*



else



    echo 'dos2unix 已安装';



fi



 



echo "############判断是否安装了docker-compose##############"



if ! type docker-compose >/dev/null 2>&1; then



    echo 'docker-compose 未安装';



	  echo '开始安装docker-compose....';



	  wget http://www.itxiaoshen.com:3001/assets/docker-compose



	  chmod +x docker-compose



	  mv docker-compose /usr/local/bin/



	  docker-compose -v



	  echo 'docker-compose安装完毕....';



else



    echo 'docker-compose 已安装';



fi



 



echo '创建simple_ecommerce网络';



docker network create simple_ecommerce



 



# 添加执行权限



chmod +x ../bin/startup-all.sh



chmod +x ../bin/shutdown-all.sh



chmod +x ../bin/update.sh



chmod +x ../bin/wait-for-it.sh



 



# 修改编码



echo "修改编码...."



dos2unix startup-all.sh



dos2unix shutdown-all.sh



dos2unix update.sh



dos2unix wait-for-it.sh



 



sh startup-all.sh
```

wait-for-it.sh等待请求脚本

```bash
#!/usr/bin/env bash



# Use this script to test if a given TCP host/port are available



 



WAITFORIT_cmdname=${0##*/}



 



echoerr() { if [[ $WAITFORIT_QUIET -ne 1 ]]; then echo "$@" 1>&2; fi }



 



usage()



{



    cat << USAGE >&2



Usage:



    $WAITFORIT_cmdname host:port [-s] [-t timeout] [-- command args]



    -h HOST | --host=HOST       Host or IP under test



    -p PORT | --port=PORT       TCP port under test



                                Alternatively, you specify the host and port as host:port



    -s | --strict               Only execute subcommand if the test succeeds



    -q | --quiet                Don't output any status messages



    -t TIMEOUT | --timeout=TIMEOUT



                                Timeout in seconds, zero for no timeout



    -- COMMAND ARGS             Execute command with args after the test finishes



USAGE



    exit 1



}



 



wait_for()



{



    if [[ $WAITFORIT_TIMEOUT -gt 0 ]]; then



        echoerr "$WAITFORIT_cmdname: waiting $WAITFORIT_TIMEOUT seconds for $WAITFORIT_HOST:$WAITFORIT_PORT"



    else



        echoerr "$WAITFORIT_cmdname: waiting for $WAITFORIT_HOST:$WAITFORIT_PORT without a timeout"



    fi



    WAITFORIT_start_ts=$(date +%s)



    while :



    do



        if [[ $WAITFORIT_ISBUSY -eq 1 ]]; then



            nc -z $WAITFORIT_HOST $WAITFORIT_PORT



            WAITFORIT_result=$?



        else



            (echo -n > /dev/tcp/$WAITFORIT_HOST/$WAITFORIT_PORT) >/dev/null 2>&1



            WAITFORIT_result=$?



        fi



        if [[ $WAITFORIT_result -eq 0 ]]; then



            WAITFORIT_end_ts=$(date +%s)



            echoerr "$WAITFORIT_cmdname: $WAITFORIT_HOST:$WAITFORIT_PORT is available after $((WAITFORIT_end_ts - WAITFORIT_start_ts)) seconds"



            break



        fi



        sleep 1



    done



    return $WAITFORIT_result



}



 



wait_for_wrapper()



{



    # In order to support SIGINT during timeout: http://unix.stackexchange.com/a/57692



    if [[ $WAITFORIT_QUIET -eq 1 ]]; then



        timeout $WAITFORIT_BUSYTIMEFLAG $WAITFORIT_TIMEOUT $0 --quiet --child --host=$WAITFORIT_HOST --port=$WAITFORIT_PORT --timeout=$WAITFORIT_TIMEOUT &



    else



        timeout $WAITFORIT_BUSYTIMEFLAG $WAITFORIT_TIMEOUT $0 --child --host=$WAITFORIT_HOST --port=$WAITFORIT_PORT --timeout=$WAITFORIT_TIMEOUT &



    fi



    WAITFORIT_PID=$!



    trap "kill -INT -$WAITFORIT_PID" INT



    wait $WAITFORIT_PID



    WAITFORIT_RESULT=$?



    if [[ $WAITFORIT_RESULT -ne 0 ]]; then



        echoerr "$WAITFORIT_cmdname: timeout occurred after waiting $WAITFORIT_TIMEOUT seconds for $WAITFORIT_HOST:$WAITFORIT_PORT"



    fi



    return $WAITFORIT_RESULT



}



 



# process arguments



while [[ $# -gt 0 ]]



do



    case "$1" in



        *:* )



        WAITFORIT_hostport=(${1//:/ })



        WAITFORIT_HOST=${WAITFORIT_hostport[0]}



        WAITFORIT_PORT=${WAITFORIT_hostport[1]}



        shift 1



        ;;



        --child)



        WAITFORIT_CHILD=1



        shift 1



        ;;



        -q | --quiet)



        WAITFORIT_QUIET=1



        shift 1



        ;;



        -s | --strict)



        WAITFORIT_STRICT=1



        shift 1



        ;;



        -h)



        WAITFORIT_HOST="$2"



        if [[ $WAITFORIT_HOST == "" ]]; then break; fi



        shift 2



        ;;



        --host=*)



        WAITFORIT_HOST="${1#*=}"



        shift 1



        ;;



        -p)



        WAITFORIT_PORT="$2"



        if [[ $WAITFORIT_PORT == "" ]]; then break; fi



        shift 2



        ;;



        --port=*)



        WAITFORIT_PORT="${1#*=}"



        shift 1



        ;;



        -t)



        WAITFORIT_TIMEOUT="$2"



        if [[ $WAITFORIT_TIMEOUT == "" ]]; then break; fi



        shift 2



        ;;



        --timeout=*)



        WAITFORIT_TIMEOUT="${1#*=}"



        shift 1



        ;;



        --)



        shift



        WAITFORIT_CLI=("$@")



        break



        ;;



        --help)



        usage



        ;;



        *)



        echoerr "Unknown argument: $1"



        usage



        ;;



    esac



done



 



if [[ "$WAITFORIT_HOST" == "" || "$WAITFORIT_PORT" == "" ]]; then



    echoerr "Error: you need to provide a host and port to test."



    usage



fi



 



WAITFORIT_TIMEOUT=${WAITFORIT_TIMEOUT:-15}



WAITFORIT_STRICT=${WAITFORIT_STRICT:-0}



WAITFORIT_CHILD=${WAITFORIT_CHILD:-0}



WAITFORIT_QUIET=${WAITFORIT_QUIET:-0}



 



# Check to see if timeout is from busybox?



WAITFORIT_TIMEOUT_PATH=$(type -p timeout)



WAITFORIT_TIMEOUT_PATH=$(realpath $WAITFORIT_TIMEOUT_PATH 2>/dev/null || readlink -f $WAITFORIT_TIMEOUT_PATH)



 



WAITFORIT_BUSYTIMEFLAG=""



if [[ $WAITFORIT_TIMEOUT_PATH =~ "busybox" ]]; then



    WAITFORIT_ISBUSY=1



    # Check if busybox timeout uses -t flag



    # (recent Alpine versions don't support -t anymore)



    if timeout &>/dev/stdout | grep -q -e '-t '; then



        WAITFORIT_BUSYTIMEFLAG="-t"



    fi



else



    WAITFORIT_ISBUSY=0



fi



 



if [[ $WAITFORIT_CHILD -gt 0 ]]; then



    wait_for



    WAITFORIT_RESULT=$?



    exit $WAITFORIT_RESULT



else



    if [[ $WAITFORIT_TIMEOUT -gt 0 ]]; then



        wait_for_wrapper



        WAITFORIT_RESULT=$?



    else



        wait_for



        WAITFORIT_RESULT=$?



    fi



fi



 



if [[ $WAITFORIT_CLI != "" ]]; then



    if [[ $WAITFORIT_RESULT -ne 0 && $WAITFORIT_STRICT -eq 1 ]]; then



        echoerr "$WAITFORIT_cmdname: strict mode, refusing to execute subprocess"



        exit $WAITFORIT_RESULT



    fi



    exec "${WAITFORIT_CLI[@]}"



else



    exit $WAITFORIT_RESULT



fi
```

容器启动脚本startup-all.sh，其他只是示例流程，可以一步步完善补充

```bash
#!/usr/bin/env bash



 



echo '=====开始安装simple_ecommerce系统环境====='



 



#echo '=====开始运行mysql====='



#docker-compose -f ../yaml/mysql.yml up -d



 



#echo '=====开始运行nacos====='



#docker-compose -f ../yaml/nacos.yml up -d



#echo '=====nacos正在进行初始化,请等待...====='



#./wait-for-it.sh http://localhost:8848 --timeout=60  -- echo "=====nacos已经准备就绪====="



 



#echo '=====开始运行rocketmq====='



#docker-compose -f ../yaml/rocketmq.yml up -d



 



#echo '=====开始运行redis====='



#docker-compose -f ../yaml/redis.yml up -d



 



#echo '=====开始运行TinyID分布式系统全局ID服务====='



#docker-compose -f ../yaml/tinyid.yml up -d



 



#echo '=====开始运行ELK====='



#docker-compose -f ../yaml/elk.yml up -d



 



echo '======================'



echo '=====开始运行后台====='



echo '======================'



 



#echo '=====开始运行ecom-gateway====='



#docker-compose -f ../yaml/ecom-gateway.yml up -d



 



echo '=====开始运行ecom-storage-service====='



docker-compose -f ../yaml/ecom-storage-service.yml up -d



 



echo '=====开始运行ecom-order-service====='



docker-compose -f ../yaml/ecom-order-service.yml up -d



 



echo '执行完成 日志目录: ./log'



 



echo '======================'



echo '=====开始运行前台====='



echo '======================'



 



#echo '=====开始运行ecom_vue_web====='



#docker-compose -f ../yaml/ecom_vue_web.yml up -d



 



echo '======================================================'



echo '=====所有服务已经启动【请检查是否存在错误启动的】====='



echo '======================================================'
```

容器关闭脚本shutdown-all.sh

```bash
#!/usr/bin/env bash



 



echo '=====开始结束运行simple_ecommerce系统服务====='



 



#echo '=====结束运行mysql====='



#docker-compose -f ../yaml/mysql.yml down



 



#echo '=====结束运行nacos====='



#docker-compose -f ../yaml/nacos.yml down



 



#echo '=====结束运行rocketmq====='



#docker-compose -f ../yaml/rocketmq.yml down



 



#echo '=====结束运行redis====='



#docker-compose -f ../yaml/redis.yml down



 



#echo '=====结束运行TinyID分布式系统全局ID服务====='



#docker-compose -f ../yaml/tinyid.yml down



 



#echo '=====结束运行ELK====='



#docker-compose -f ../yaml/elk.yml down



 



echo '=========================='



echo '=====结束后台服务运行====='



echo '=========================='



 



#echo '=====结束运行ecom-gateway====='



#docker-compose -f ../yaml/ecom-gateway.yml down



 



echo '=====结束运行ecom-storage-service====='



docker-compose -f ../yaml/ecom-storage-service.yml down



 



echo '=====结束运行ecom-order-service====='



docker-compose -f ../yaml/ecom-order-service.yml down



 



echo '=========================='



echo '=====结束前台服务运行====='



echo '=========================='



 



#echo '=====结束运行ecom_vue_web====='



#docker-compose -f ../yaml/ecom_vue_web.yml down



 



echo '=============================='



echo '=====所有服务已经结束运行====='



echo '=============================='
```

更新镜像脚本update.sh，包含关闭容器、下载新的镜像、启动容器

```bash
#!/usr/bin/env bash



 



echo '=====开始更新simple_ecommerce系统镜像====='



 



echo '=====开始关闭运行的容器====='



sh shutdown-all.sh



 



#echo '=====开始更新ecom-gateway====='



#docker pull registry.itxs.cn/simple_ecommerce/ecom-gateway



 



echo '=====开始更新ecom-storage-service====='



docker pull registry.itxs.cn/simple_ecommerce/ecom-storage-service



 



echo '=====开始更新ecom-order-service====='



docker pull registry.itxs.cn/simple_ecommerce/ecom-order-service



 



#echo '=====开始更新cu_vue_web====='



#docker pull registry.itxs.cn/simple_ecommerce/ecom_vue_web



 



echo '=====删除docker标签为none的镜像====='



docker images | grep none | awk '{print $3}' | xargs docker rmi



 



echo '=====开始运行的一键部署脚本====='



sh startup-all.sh
```

## 执行测试

```bash
# 进入到bin目录下，由于我这里本地有镜像，少了pull流程



sh ./init.sh
```

![image-20220419155812868](https://img-blog.csdnimg.cn/img_convert/339d5a417885ec6acbfb8d9975fad7b7.png)

查看容器运行情况，容器正常运行

![image-20220419160027572](https://img-blog.csdnimg.cn/img_convert/288c14795006be3350762ba31faa08c0.png)

查看nacos服务的注册信息

![image-20220419160237729](https://img-blog.csdnimg.cn/img_convert/952582a722c393e787e583a1f1fb8505.png)

访问订单接口http://192.168.50.95:4070/create/1001/1001/3 ，返回成功结果

![image-20220419160329098](https://img-blog.csdnimg.cn/img_convert/173e6d0235e7e25a054522288952c70f.png)

查看订单表和库存表的数据都已更新，至此部署完毕

![image-20220419160543506](https://img-blog.csdnimg.cn/img_convert/126dae84b5d802d516d457df339a1627.png)

因为内容实在是太多了