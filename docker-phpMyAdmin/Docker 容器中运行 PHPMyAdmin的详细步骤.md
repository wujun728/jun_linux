# Docker 容器中运行 PHPMyAdmin的详细步骤



Docker是一个开源的应用容器引擎，它能够实现应用部署的自动化。此外，容器是完全使用沙箱机制，容器之间的环境相互独立，不会相互干扰，接下来通过本文给大家介绍在 Docker 容器中运行 PHPMyAdmin的详细步骤，感兴趣的朋友一起看看吧



**+**

##### 目录

![在这里插入图片描述](https://img.jbzj.com/file_images/article/202201/2022012510210112.png)

PHPMyAdmin是 MySQL 和 MariaDB 数据库的流行管理界面。它允许您使用 Web 浏览器与您的模式、表和数据进行交互。phpMyAdmin能够为你的MySQL提供直观、方便的Web管理界面，非常好用。

该项目有一个官方的 Docker 镜像，它简化了在容器化环境中的部署。以下是如何使用图像快速运行新的 PHPMyAdmin 实例。



## 基本用法

最简单的安装让 PHPMyAdmin 容器连接到任何可访问的数据库服务器：

```
docker run -d --name phpmyadmin -e PMA_ARBITRARY=1 -p 8080:80 phpmyadmin
```

此命令在端口 8080 上启动 PHPMyAdmin。localhost:8080在浏览器中访问以查看登录屏幕。环境变量的存在会PMA_ARBITRARY导致显示服务器连接表单。指定要登录的 MySQL 或 MariaDB 数据库的主机和用户凭据。

![在这里插入图片描述](https://img.jbzj.com/file_images/article/202201/2022012510210113.png)

当您使用此方法时，您通常会看到一个 PHPMyAdmin 警告“某些扩展功能已被停用”。当您连接的服务器没有名为phpmyadmin. PHPMyAdmin 使用这个模式来存储它自己的配置数据。

![在这里插入图片描述](https://img.jbzj.com/file_images/article/202201/2022012510210114.png)

按照警告链接“创建数据库”完成安装。您的用户帐户将需要在服务器上创建新数据库的权限。



## 预设服务器

作为允许任意访问的替代方法，您可以使用预配置的服务器连接启动 PHPMyAdmin 容器。提供PMA_HOSTandPMA_PORT环境变量而不是PMA_ARBITRARY：

```
docker run -d --name phpmyadmin -e PMA_HOST=mysql.example.com -e PMA_PORT=33060 -p 8080:80 phpmyadmin
```

PMA_PORT是可选的。当没有提供值时，它将使用 MySQL 默认值 3306。

使用这些变量启动容器将限制 PHPMyAdmin 使用mysql.example.com服务器。系统会在登录屏幕上提示您输入用户名和密码，但您不需要提供主机名。

PHPMyAdmin 也可以配置为呈现多个服务器选项。提供PMA_HOSTS并PMA_PORTS以逗号分隔的连接列表来启用此功能。



## 使用 MySQL Docker 容器

另一个常见用例是连接到在单独的 Docker 容器中运行的 MySQL 或 MariaDB 服务器。您可以在端口上公开数据库服务器，也可以将两个容器连接到共享的 Docker 网络。在任何一种情况下，使用PMA_HOST和PMA_PORT环境变量将指示 PHPMyAdmin 如何连接到服务器。

还支持旧版 Docker 链接：

```
docker run -d --name phpmyadmin --link my_mysql_container:``db` `-p 8080:80 phpmyadmin
```

此命令允许您将 PHPMyAdmin 连接到my_mysql_container容器，而无需手动设置网络链接。这个功能在 Docker 中被弃用了，所以切换到网络命令是更可取的：

```
docker network create phpmyadmin``docker network connect phpmyadmin mysql_container_name --ip 172.17.0.1``docker network connect phpmyadmin phpmyadmin_container_name
```

作为替代方案，您可以使用 Docker 的–network标志通过预配置的网络连接启动 PHPMyAdmin ：

```
docker run -d --name phpmyadmin --network phpmyadmin -p 8080:80 phpmyadmin
```

现在 PHPMyAdmin 将能够通过共享网络访问 MySQL 容器。将PMA_HOST环境变量设置为172.17.0.1启动容器时。



## 使用 Docker Compose 简化部署

编写Docker Compose 文件可以简化重要的部署。您可以使用该docker-compose up -d命令以可重复的方式启动一个新的 PHPMyAdmin 容器。

这是docker-compose.yml任意连接模式下的 PHPMyAdmin：

```
version: "3"` `services:`` ``phpmyadmin:``  ``image: phpmyadmin:latest``  ``ports:``    ``- 8080:80``  ``environment:``    ``- PMA_ARBITRARY=1``  ``restart: unless-stopped
```

Docker Compose 还可以帮助您使用全新的 MySQL 数据库安装和 PHPMyAdmin 容器创建堆栈：

```
version: "3"` `service:`` ``mysql:``  ``image: mysql:latest``  ``expose:``   ``- 3306``  ``environment:``   ``- MYSQL_ROOT_PASSWORD``  ``volumes:``   ``- mysql:/var/lib/mysql``  ``restart: unless-stopped`` ``phpmyadmin:``  ``image: phpmyadmin:latest``  ``ports:``   ``- 8080:80``  ``environment:``   ``- PMA_HOST: mysql``   ``- PMA_PASSWORD: ${MYSQL_ROOT_PASSWORD}``  ``restart: unless-stopped` `volumes:`` ``- mysql
```

运行docker-compose up -d以使用完全联网的 PHPMyAdmin 容器启动 MySQL。PHPMyAdmin 的PMA_HOST变量设置为mysql，引用 MySQL 服务名称。Docker Compose 自动设置主机名以匹配服务名称，允许 PHPMyAdmin 使用共享网络连接到 MySQL。



## 配置安装

PHPMyAdmin Docker 映像支持用户提供的配置文件，您可以通过Docker 卷注入该配置文件。路径是/etc/phpmyadmin/config.user.inc.php：

```
docker run -d \``  ``--name phpmyadmin \``  ``-e PMA_ARBITRARY=1 \``  ``-p 8080:80 \``  ``-``v` `my-config-``file``.php:``/etc/phpmyadmin/config``.user.inc.php``  ``phpmyadmin
```

您可以添加PHPMyAdmin 支持的任何配置变量。

该图像还支持许多常见设置的环境变量。这些措施包括MEMORY_LIMIT，UPLOAD_LIMIT并且MAX_EXECUTION_TIME，每个对应于可能需要如果你使用长时间运行或复杂的查询进行调整，PHP INI值。

敏感值，例如PMA_HOST，PMA_PASSWORD，和MYSQL_ROOT_PASSWORD，可以使用注射多克尔秘密而非纯的环境变量。附加_FILE到变量的名称，然后将值设置为容器内提供实际值的路径。

```
docker run -d --name phpmyadmin -e PMA_HOST_FILE=``/run/secrets/pma_host` `-p 8080:80 phpmyadmin
```



## 概括

PHPMyAdmin 是最流行和最著名的 MySQL 管理实用程序之一。裸机安装为您的系统添加了多个依赖项，将 Apache 和 PHP 与应用程序的源代码捆绑在一起。

在 Docker 中安装 PHPMyAdmin 为您提供了一个隔离环境，可以使用少数 Docker CLI 命令创建、替换和删除该环境。官方镜像可以连接到可以从您的主机访问的任何 MySQL 服务器，包括在其他 Docker 容器中运行的数据库。



可以在官方文档中找到有关运行和使用 PHPMyAdmin 的更详细指南。查看安全指南尤其重要，这样您就不会无意中让您的数据库面临外部攻击的风险。在暴露给外界的容器中部署 PHPMyAdmin 时，您还应该考虑Docker 安全最佳实践。