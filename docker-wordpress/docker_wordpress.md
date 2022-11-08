# Docker搭建WordPress博客



WordPress是一个非常著名的PHP编写的博客平台，发展到目前为止已经形成了一个庞大的网站平台系统。在WP上有规模庞大的插件和主题，可以帮助我们快速建立一个博客甚至网站。

在Windows上可以非常方便的安装WordPress，因为IIS上集成了WordPress的一键安装包。而在Linux上安装WordPress就比较复杂了，我们需要配置PHP环境、Apache或者Nginx服务器、MySQL数据库以及各种权限和访问问题。所以在Linux上最好的办法就是使用Docker来安装WordPress。

安装Docker
如果是Windows平台，可以参考在Windows平台上搭建Docker开发环境。如果在Linux环境中，按照所使用的Linux的包管理器来安装Docker即可。顺便还可以安装Kitematic，这是一个非常好用的Docker图形界面工具。

安装完成之后需要启用Docker后台服务。如果是国内用户的话可能还需要设置Docker加速，可以参考Docker 镜像加速器-博客-云栖社区-阿里云。

**安装WordPress**
有了Docker，安装WordPress就很简单了，直接一条命令搞定。

docker pull wordpress:5.8
1
**安装MySQL**
WordPress需要使用MySQL数据库，这里也有两种方式，第一种是安装本地MySQL，第二种就是在Docker中安装MySQL镜像。如果要在Docker中安装MySQL也非常简单，同样一条命令搞定。

docker pull mysql:5.7
1
如果从Docker中安装MySQL，还需要额外的配置来启动MySQL，具体文档参考这里。启动MySQL使用下面的命令。

docker run --name some-mysql -e MYSQL_ROOT_PASSWORD=my-secret-pw -d mysql:tag
1
name参数指定要启动的实例名称，MYSQL_ROOT_PASSWORD指定ROOT密码。tag参数是MySQL的版本号，可以是5.7、5.6、8.0。

**配置WordPress**
安装好数据库之后，就可以启动WordPress了。详细的文档参考这里。如果使用Docker中安装的MySQL实例，使用下面的命令。

docker run --name some-wordpress --link some-mysql:mysql -p 8080:80 -d wordpress

docker run --name wordpress5.8 --link mysql:mysql  -v   /home/wordpress/wp-content:/var/www/html/wp-content  -p 8000:80 -d wordpress



docker run --name wordpress5.8 --link mysql:mysql  -v   /home/wordpress/wp-content:/var/www/html/wp-content    -e WORDPRESS_DB_HOST=119.45.221.36:3306      -e WORDPRESS_DB_USER=root  -e WORDPRESS_DB_PASSWORD=mysqladmin     -p 8000:80 -d wordpress



​	



name参数指定要启动的WordPress实例名称，link参数指定要使用的Docker MySQL实例名称，p参数将Docker内部的80端口映射到本地的8080端口上。

如果使用外部的MySQL数据库，则输入下面的命令。

docker run --name some-wordpress -e WORDPRESS_DB_HOST=10.1.2.3:3306 \
    -e WORDPRESS_DB_USER=... -e WORDPRESS_DB_PASSWORD=... -d wordpress
1
2
WORDPRESS_DB_HOST参数是MySQL的数据库端口号，WORDPRESS_DB_USER是要数据库用户名，WORDPRESS_DB_PASSWORD是数据库密码。这里的WORDPRESS_DB_HOST参数不能填写localhost，因为这样会重定向到WordPress镜像内部的localhost，而这个镜像中实际上没有安装MySQL。所以这里需要填写本机IP地址，才能正确访问到Docker外部的本机的数据库。

因此需要注意，如果使用外部数据库的话，数据库的用户需要具有外部IP的权限，因为这次不是通过本机回环地址访问。默认情况下MySQL安装时候的ROOT用户只允许本地登录，所以可能需要配置允许用户远程登录。

然后打开浏览器，输入localhost:8080（端口号是命令中设置的），然后就可以看到WordPress了。按照提示输入用户名等信息，然后安装WordPress。等到它提示安装完成，那么WordPress的安装就算大功告成了。

最后稍加配置，再添加诸如内网映射等功能之后，站点就可以对外访问了。
————————————————
版权声明：本文为CSDN博主「过了即是客」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/u011054333/article/details/70136099







docker run  --name apache -p 8000:80 -v $PWD/htdocs/:/usr/local/apache2/htdocs/ -v $PWD/conf/httpd.conf:/usr/local/apache2/conf/httpd.conf -v $PWD/logs/:/usr/local/apache2/logs/ -d centos/httpd





https://www.runoob.com/docker/docker-image-usage.html





https://www.runoob.com/docker/docker-install-apache.html