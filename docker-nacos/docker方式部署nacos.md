# docker方式部署nacos



Nacos 提供了一组简单易用的特性集，帮助您快速实现动态服务发现、服务配置、服务元数据及流量管理，下面通过本文docker方式部署nacos的过程



##### 目录



## docker方式部署nacos



### 1 拉取nacos镜像并启动

```
docker pull nacos``/nacos-server
```

![img](https://img.jbzj.com/file_images/article/202205/2022051911082451.png)



### 2 启动nacos命令

```
docker run -d --name nacos -p 8848:8848 -e PREFER_HOST_MODE=``hostname` `-e MODE=standalone nacos``/nacos-server
```

至此，我们已经可以使用nacos服务，UI地址:http://:8848/nacos 账号:nacos 密码:nacos

![img](https://img.jbzj.com/file_images/article/202205/2022051911082452.png)

上述方式是最简便的方式启动，但这样的话有一点小瑕疵，nacos所有元数据都会保存在容器内部。倘若容器迁移则nacos源数据则不复存在，所以通常我们通常会将nacos元数据保存在mysql中。下面附上配置方式：



### 3 修改配置文件

```
#1 查看docker容器，nacos启动成功``docker ``ps``CONTAINER ID    IMAGE        COMMAND         CREATED       STATUS       PORTS          NAMES``8149bca96437    nacos``/nacos-server`  `"bin/docker-startup.…"`  `4 minutes ago    Up About a minute  0.0.0.0:8848->8848``/tcp`  `nacos``#2 进入容器``docker ``exec` `-it 8149bca96437 ``/bin/bash``#3 修改 conf/application.properties 内容如下：``vi` `conf``/application``.properties
```

数据库脚本

[nacos-db.sql](https://github.com/alibaba/nacos/blob/master/config/src/main/resources/META-INF/nacos-db.sql)

application.properties 内容替换为

```
# spring``server.contextPath=``/nacos``server.servlet.contextPath=``/nacos``server.port=8848``management.metrics.``export``.elastic.enabled=``false``management.metrics.``export``.influx.enabled=``false``server.tomcat.accesslog.enabled=``true``server.tomcat.accesslog.pattern=%h %l %u %t ``"%r"` `%s %b %D %{User-Agent}i``server.tomcat.basedir=``nacos.security.ignore.urls=/,/**/*.css,/**/*.js,/**/*.html,/**/*.map,/**/*.svg,/**/*.png,/**/*.ico,``/console-fe/public/``**,``/v1/auth/login``,``/v1/console/health/``**,``/v1/cs/``**,``/v1/ns/``**,``/v1/cmdb/``**,``/actuator/``**,``/v1/console/server/``**``spring.datasource.platform=mysql``db``.num=1``db``.url.0=jdbc:mysql:``//``:``/nacos``?characterEncoding=utf8&connectTimeout=1000&socketTimeout=3000&autoReconnect=``true``db``.user=root``db``.password=password
```



### 4 退出容器

```
exit
```



### 5 重启容器

```
docker restart 8149bca96437
```