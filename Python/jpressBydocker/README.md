
#### 安装 docker and docker-compose 
```
// docker Version: 18.06.1-ce
// docker-compose Version 1.23.1
wget -c https://github.com/itsccn/jpressBydocker/releases/download/jpressBydocker1.0/docker-compose -O /opt/docker-compose
wget -c https://github.com/itsccn/jpressBydocker/releases/download/jpressBydocker1.0/docker.rpm -O /opt/docker.rpm
yum install -y /opt/docker.rpm
chmod +x /opt/docker-compose
mv /opt/docker-compose /usr/local/bin/
```
#### 下载 jpressBydocker
```
wget -c https://github.com/itsccn/jpressBydocker/archive/jpressBydocker1.0.tar.gz -O /opt/jpressBydocker.tar.gz
mkdir jpressBydocker && tar -zxvf /opt/jpressBydocker.tar.gz -C jpressBydocker --strip-components 1

```
#### 构建jpress environment (jpress初始化表结构在 /opt/jpressBydocker/mysql/db.sql build完成后会自动执行)
```
//修改 docker-compose.yml文件中初始化的数据库名称、root用户密码 为jpress创建的用户名密码和下文的war包内的jboot.properties对应
     environment:
           MYSQL_ROOT_PASSWORD: 'AScsaw@ddcc'
           MYSQL_DATABASE: 'jpress'
           MYSQL_USER: 'jpress'
           MYSQL_PASSWORD: 'jpress_db_password'

systemctl start docker
cd /opt/jpressBydocker/ && docker-compose build
```
#### 下载jpress war包 替换 ```/opt/jpressBydocker/tomcat/jpress``` 下的war,执行 ```cd /opt/jpressBydocker/ && docker-compose up -d```
#### 完成后 停止所有的服务 ```cd /opt/jpressBydocker/ && docker-compose stop```
#### 修改 ```/opt/jpressBydocker/tomcat/jpress/ROOT/WEB-INF/classes/jboot.properties``` 文件
```
// 只需要修改用户名密码即可 
jboot.datasource.type=mysql
jboot.datasource.url=jdbc:mysql://db:3306/jpress?useUnicode=true&characterEncoding=UTF-8 // 最好加上编码
jboot.datasource.user=jpress
jboot.datasource.password=jpress_db_password
```
#### 一切就绪后再重启所有的容器保证所有配置都生效
```
cd /opt/jpressBydocker/ && docker-compose restart
```

#### 挂载的目录说明
``` /opt/jpressBydocker/tomcat/jpress/ROOT ``` jpress 源码目录 修改直接生效

``` /opt/jpressBydocker/nginx/nginx.conf ``` nginx 配置文件 （配置https 把证书放置在/opt/jpressBydocker/nginx/cert 文件夹 ``` ssl_certificate		./cert/server.crt; ``` 即可）

```/opt/jpressBydocker/tomcat/jpress/ROOT/static:/etc/nginx/statics/static ```和 ```/opt/jpressBydocker/tomcat/jpress/ROOT/templates:/etc/nginx/statics/templates ``` 挂载到nginx容器下 方便让nginx处理静态资源

``` /opt/jpressBydocker/mysql/data ``` mysql 数据文件

#### 服务器启停

``` cd /opt/jpressBydocker/ && docker-compose restart ``` 重启所有服务

``` cd /opt/jpressBydocker/ && docker-compose start ``` 启动所有容器

``` cd /opt/jpressBydocker/ && docker-compose stop ``` 停止所有容器

#### 1.点击[下载 docker](https://github.com/itsccn/jpressBydocker/releases/download/jpressBydocker1.0/docker.rpm)
#### 2.点击[下载 docker-compose](https://github.com/itsccn/jpressBydocker/releases/download/jpressBydocker1.0/docker-compose)
#### 3.点击[下载 jpressBydocker1.0](https://github.com/itsccn/jpressBydocker/archive/jpressBydocker1.0.zip)
#### 4.点击[下载 jpress.war](https://gitee.com/fuhai/jpress/attach_files/download?i=181664&u=http%3A%2F%2Ffiles.git.oschina.net%2Fgroup1%2FM00%2F05%2F79%2FPaAvDFvii9mAfAqcAwxJMHkhSEs352.war%3Ftoken%3Da298841bc64b283701e4a7c4b1f20ee4%26ts%3D1541815552%26attname%3Dstarter-tomcat-1.0.war)

