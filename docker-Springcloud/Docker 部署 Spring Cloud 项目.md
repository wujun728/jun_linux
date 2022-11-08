# [ Docker 部署 Spring Cloud 项目](https://www.cnblogs.com/d102601560/p/12883271.html)

**准备工作**

JDK1.8、Docker1.12.1、CentOS7.0

**1.CentOS7.0下JDK1.8的安装**

（1）到Oracle官网下载好 jdk-8u181-linux-x64.tar.gz 备用
（2）卸载系统自带的java

java -**version**      
rpm -**qa**|**grep** java
yum -**y** remove [上面查出来的东西，多个用空格分隔]

（3）安装jdk

cd /usr *#**进入到要安装**jdk**的目录*
mkdir java *#**创建**java**目录，将**jdk-8u181-linux-x64.tar.gz**上传到此目录*
tar -zxvf jdk-8u181-linux-x64.tar.gz *#**将**jdk**压缩包解压安装*

（4）配置环境变量

**vim** /etc/**profile**

找到：export PATH USER LOGNAME MAIL HOSTNAME HISTSIZE HISTCONTROL 这一行，并在其下面一行添加如下内容：

export JAVA_HOME=/usr/java/jdk1.8.0_181
export PATH=$JAVA_HOME/bin:$PATH
export CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar

使环境变量生效

**source** /etc/**profile**

测试安装

java -**version**

 

**2.Docker的安装**

 

（1） 查看内核版本(Docker需要64位版本，同时内核版本在3.10以上，如果版本低于3.10，需要升级内核)

uname -r

（2） 更新yum包：

yum **update**

（3） 添加yum仓库：

sudo tee /etc/yum.repos.d/docker.repo <<-'EOF'
[dockerrepo]
name=Docker Repository
baseurl=https://yum.dockerproject.org/repo/main/centos/7/
enabled=1
gpgcheck=1
gpgkey=https://yum.dockerproject.org/gpg
EOF

（4） 安装Docker

yum **install** docker-**engine**

（5） 启动Docker

service docker **start**

（6）配置docker远程访问

执行命令编辑文件

**vim** /usr/lib/systemd/system/docker.service

找到这一行

ExecStart=/usr/bin/dockerd

改为 

ExecStart=/usr/bin/dockerd -H tcp:
 unix:

修改完成后保存并重启Docker

service docker restart

测试访问 http://125.35.86.214:2375/version 如果有返回数据则配置成功。

（7）使用Docker国内镜像（为Docker镜像下载提速，非必须）

curl -sSL https://get.daocloud.io/daotools/set_mirror.**sh** | **sh** -s
http://fe8a7d6e.**m**.daocloud.io

 

**3. Docker Compose的安装**

（1）下载docker-compose ，并放到/usr/local/bin/

https://github.com/docker/compose/releases/download/1.8.0/docker-compose-`uname
-s`-`uname -m` > /usr/local/bin/docker-compose

（2）为Docker Compose脚本添加执行权限

chmod +x /usr/local/bin/docker-compose

（3）安装完成，测试

docker-compose *--version*

结果显示：

**docker-compose** **version** 1.8.0, **build** **f3628c7**

说明Docker Compose已经安装完成了。

**4. Docker使用Maven插件构建并上传镜像**

（1）新建Dockerfile文件
在项目的/src/main下新增文件夹docker，并在文件夹下创建Dockerfile文件，文件内容如下

*#* *基于哪个镜像*
FROM java:8
*#* *将本地文件夹挂载到当前容器*
VOLUME /tmp
*#* *拷贝文件到容器，**handcuffs-reg-0.0.1-SNAPSHOT.jar**这里是**maven**打包后的名字*
ADD handcuffs-reg-0.0.1-SNAPSHOT.jar app.jar
RUN bash -c 'touch /app.jar'
*#* *配置容器启动后执行的命令*
ENTRYPOINT ["java","-Djava.security.egd=file:/dev/./urandom","-jar","/app.jar"]

（2）修改pom.xml文件增加如下plugin
imageName：镜像名称
dockerDirectory：Dockerfile文件所在目录
dockerHost：docker所在宿主机ip 2375为docker开启的远程访问端口
其他配置采取默认即可

<plugin>
  <groupId>com.spotifygroupId>
  <artifactId>docker-maven-pluginartifactId>
  <version>0.4.14version>
  <configuration>
    <imageName>reg-serviceimageName>
    <dockerDirectory>src/main/dockerdockerDirectory>
     <dockerHost>http://125.35.86.214:2375dockerHost>
      <resources>
        <resource>
          <targetPath>/targetPath>
          <directory>${project.build.directory}directory>
          <include>${project.build.finalName}.jarinclude>
        resource>
      resources>
  configuration>
plugin>

每一个微服务项目都要进行配置。

（3）构建镜像并上传至docker
使用maven运行如下命令

clean **package** docker:build -DskipTests

上传成功后，在服务器输入

docker images

可以看到所有的docker镜像啦。

**5. 使用Docker Compose进行服务编排**

（1）在服务器任意目录，新建文件docker-compose.yml

version: '2'
services:
 eureka-server1:
  restart: on-failure
  image: reg-service
  ports:
   \- "8761:8761"      
  networks:
   \- eureka-net
  environment:
   SERVER_PORT: "8761"   

 config:
  image: config-service
  networks:
   \- eureka-net
  ports:
   \- "8091:8091"      
  environment:
   REGISTER_URL: "http://114.115.185.152:8761/eureka/" 
   SERVER_PORT: "8091"
   SERVER_GIT_URL: "https://gitee.com/deanTheOne/handcuffs-config.git"
   SERVER_GIT_USERNAME: "test"
   SERVER_GIT_PASSWORD: "test"
   RABBITMQ_HOST: "39.105.152.144"
   RABBITMQ_PORT: "5672"
   RABBITMQ_USERNAME: "mqTest"
   RABBITMQ_PASSWORD: "mqTest"


 zuul:
  restart: on-failure
  image: gateway-service
  ports:
   \- "8000:8000"
  environment:
   REGISTER_URL: "http://114.115.185.152:8761/eureka/"
   SERVER_PORT: "8000"
   SERVER_ADDR: "114.115.185.152"
  networks:
   \- eureka-net
networks:
 eureka-net:

  driver: bridge

文件编写完毕保存，切换到当前文件所在目录，输入命令启动Docker Compose

docker-compose -**f** docker-compose.yml **up** -d

停止Docker Compose命令

**docker-compose** **-f** **docker-compose**.yml **down**