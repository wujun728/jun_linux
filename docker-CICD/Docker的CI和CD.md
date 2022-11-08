Docker的CI和CD

 
一 CI-持续集成.
在程序员编写完一个功能要提交到GitLab仓库后，GitLab Runner将最新提交上去的代码，package，在通过Docker部署到GitLab Runner所在的服务器中。

安装GitLab Runner：

docker-compose.yml文件
version: ‘3.1’
services:
gitlab-runner:
build: environment
restart: always
container_name: gitlab-runner
privileged: true
volumes:
- ./config:/etc/gitlab-runner
- /var/run/docker.sock:/var/run/docker.sock

加载Dockerfile，启动自定义镜像。

FROM baseservice.qfjava.cn:60001/gitlab-runner:bleeding

修改软件源
RUN echo ‘deb http://mirrors.aliyun.com/ubuntu/ xenial main restricted universe multiverse’ > /etc/apt/sources.list &&
echo ‘deb http://mirrors.aliyun.com/ubuntu/ xenial-security main restricted universe multiverse’ >> /etc/apt/sources.list &&
echo ‘deb http://mirrors.aliyun.com/ubuntu/ xenial-updates main restricted universe multiverse’ >> /etc/apt/sources.list &&
echo ‘deb http://mirrors.aliyun.com/ubuntu/ xenial-backports main restricted universe multiverse’ >> /etc/apt/sources.list &&
#下面的地址需要根据实际情况变化
wget https://http.kali.org/kali/pool/main/k/kali-archive-keyring/kali-archive-keyring_2018.2_all.deb --no-check-certificate &&
apt install -y ./kali-archive-keyring_2018.2_all.deb &&
apt-get update -y &&
apt install -y gnupg &&
apt-get clean

安装 Docker
RUN curl -fsSL http://mirrors.aliyun.com/docker-ce/linux/ubuntu/gpg | apt-key add - &&
apt-get install -y python-software-properties software-properties-common &&
echo ‘deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable’ >> /etc/apt/sources.list.d/docker.list &&
apt-get update -y &&
apt-get install -y docker-ce
COPY daemon.json /etc/docker/daemon.json

安装 Docker Compose,因为下载不下来，所以我们本地上传一份docker-compose到environment目录
WORKDIR /usr/local/bin
#RUN wget https://raw.githubusercontent.com/topsale/resources/master/docker/docker-compose
COPY docker-compose docker-compose
RUN chmod +x docker-compose

安装 Java
RUN mkdir -p /usr/local/java
WORKDIR /usr/local/java
COPY jdk-8u231-linux-x64.tar.gz /usr/local/java
RUN tar -zxvf jdk-8u231-linux-x64.tar.gz &&
rm -fr jdk-8u231-linux-x64.tar.gz

安装 Maven
RUN mkdir -p /usr/local/maven
WORKDIR /usr/local/maven
RUN wget https://raw.githubusercontent.com/topsale/resources/master/maven/apache-maven-3.6.3-bin.tar.gz
COPY apache-maven-3.6.3-bin.tar.gz /usr/local/maven
RUN tar -zxvf apache-maven-3.6.3-bin.tar.gz &&
rm -fr apache-maven-3.6.3-bin.tar.gz
#需要配置maven 私服的话,不需要就加#注释掉
#COPY settings.xml /usr/local/maven/apache-maven-3.6.3/conf/settings.xml

配置环境变量
ENV JAVA_HOME /usr/local/java/jdk1.8.0_231
ENV MAVEN_HOME /usr/local/maven/apache-maven-3.6.3
ENV PATH P A T H : PATH:PATH:JAVA_HOME/bin:$MAVEN_HOME/bin

environment目录：

Dockerfile文件
FROM 通过本地私服找到GitLab-Runner镜像
RUN 安装Docker（设置镜像源，更新apt-get仓库，apt-get安装Docker）
COPY daemon.json /etc/docker/daemon.json
COPY docker-compose /usr/local/bin
COPY JDK压缩包 /usr/loca/jdk
COPY Maven压缩包 /usr/local/maven
RUN 配置环境变量
JDK压缩包，Maven压缩包，docker-compose文件，daemon.json文件
设置宿主机和容器的Docker绑定信息：

将宿主机的/var/run/docker.sock文件的拥有者设置为root
在容器启动成功后，执行docker exec -it gitlab-runner usermod -aG root gitlab-runner目录
将GitLab的一个仓库和GitLabRunner绑定到一起：

执行docker exec -it gitlab-runner gitlab-runner register
根据要求分别数据GitLab的地址、token、描述、deploy、shell。
在GitLab中查看到绑定信息，点击绑定信息的编辑图标操作，勾选上第三个勾。
创建Maven项目指定ci以及相应的配置文件：

.gitlab-ci.yml

stages:
- test
```

test:
stage: test
script:
- echo xxxx
- pwd
- /usr/local/maven/apache-maven-3.6.3-bin/bin/mvn clean package -DskipTests
- cp target/testci-1.0…war testci.war
- docker-compose down
- docker-compose up -d --build
- docker image prune -f


 - docker-compose.yml

 - Dockerfile
         自定义镜像，将war包部署到tomcat服务器
1
2
3
4
5
二. CD
1.1 安装Jenkins
复制笔记中的docker-compose.yml文件中的内容，直接启动即可。
–
version: “3.1”
services:
jenkins:
image: 10.0.134.175:5000/jenkins:2.235
restart: always
container_name: jenkins
ports:
-9999:8080
-50000:50000
volumes:
-./data:/var/jenkins_home

第一次启动会失败，查看日志，数据卷data目录权限不足：chmod 777 data。
重启jenkins容器。（这次启动速度较慢，知道可以访问到jenkins首页）。
需要在首页输入日志中提供的一个密钥。
选择自动安装插件还是手动指定安装插件，选择后者。
必须要安装的内容有2个：Publish Over SSH，Git Parameter
开始安装。（漫长的等待，并且伴随着不断的失败，不断的重试。）
直到可以访问到指定管理员信息的界面。
指定用户信息。
指定默认URL。
进入到Jenkins的首页。


还需要再Jenkins中再次安装一个插件


1.2 CD流程
当程序员将代码推送到GitLab上后，会再GitLab仓库版本中打标签，指定版本号。
jekins可以将之打包并部署到目标服务器的环境下运行，如果出现问题，还可以快速回滚到上一个版本

GitLab Jenkins 目标服务器（测试环境，生产环境）

Jenkins绑定目标服务器。
系统管理：系统配置：拉到最下面能看到Publish over SSH：
链接目标服务器的后续操作


Jenkins链接GitLab。（采用SSH无密码链接的方式）
进入到Jenkins容器内部，先跳转到用户目录~，执行ssh-keygen -t rsa -C “邮箱（随便写）”
在~目录下，会生成一个.ssh隐藏目录，进入.ssh目录。
能查看到私钥和公钥，将公钥复制到GitLab的settings配置中。
GitLab的操作


需要在指定好GitLab无密码链接后，使用git clone 下载一次项目。

第一次使用SSH登录时， Git会询问yes/no。

在Jenkins中安装JDK和Maven
在宿主机中映射Jenkins的数据卷目录下，解压JDK和Maven的压缩包。
在Jenkins页面中配置
配置方式



1.3 CD前期测试
Jenkins可以去GitLab中拉取代码,并且在Jenkins内部将项目打成war包.







1.4 配置Jenkins通过tag标签实现操作.
给GitLab中的项目打标签（tag）。

配置Jenkins信息：

General：参数化构建：Git参数
名称：tag
参数类型：标签
默认值：master
再次build with parameter时，就可以看到GitLab中项目的标签信息了。

为了指定标签构建的同时，可以选择指定标签下的项目代码，需要重新配置打包方式：

构建：执行shell去构建项目

echo $tag
pwd
git checkout $tag
git pull origin $tag
/var/jenkins_home/apache-maven-3.6.3/bin/mvn clean package -DskipTest


- 为了可以将war包，部署到目标服务器上，需要指定配置信息：

 - 构建后操作：Send build artifacts over SSH：

 - ```
Source files：**/*.war,docker-compose.yml,Dockerfile
Remote directory：在绑定的目标服务器目录下再次创建一个目录，将内容存放。（testcd）
Exec command：
	cd /usr/local/jenkins/testcd
    cp target/test-cd-1.0-SNAPSHOT.war ./testcd.war
    docker-compose down
    docker-compose up -d --build
    docker image prune -f
1
2
3
4
5
6
7
8
9
10
11
12
13
14
在IDEA项目中准备docker-compose.yml文件，以及Dockerfile文件。
最后就可以访问测试了

以上就是ci和cd的基本操作了 
```