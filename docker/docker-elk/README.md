# docker-elk
使用Docker-ELK项目，你可以快速拥有一套实用的Elasticsearch+Logstash+Kibana构成的日志管理系统。其中还包含了一个从web server获取日志的例子，助你更快的将ELK日志管理系统投入生产。项目中的elk-filebeat使用了[Filebeat](https://www.elastic.co/guide/en/beats/filebeat/current/filebeat-overview.html)作为服务器的日志采集器；elk-forwarder使用了[logstash-forwarder](https://github.com/elastic/logstash-forwarder)作为服务器的日志采集器。
## 准备
Docker-ELK所使用的Dockerfile和配置文件可以从[http://git.oschina.net/gongxusheng/docker-elk](http://git.oschina.net/gongxusheng/docker-elk)下载，下载后请上传到Linux服务器并解压。使用前请确保成功安装了[Docker](https://docs.docker.com/engine/installation/linux/centos/)和[Docker-compose](https://docs.docker.com/compose/install/)。本程序在Ubuntu 14.04.4 LTS上经过了测试。
## 使用elk-filebeat
![filebeat](http://git.oschina.net/uploads/images/2016/0410/000417_3453c47c_411046.png "filebeat")

Filebeat的原理如图所示。要启动项目，请在elk-filebeat目录中执行
```
docker-compose up
```
即可启动项目。等待项目成功启动以后，访问[http://yourhost:5601](http://)即可打开Kibana界面。访问Nginx的自带页面[http://yourhost:8080](http://)，就可以在Kibana界面中看到访问日志被采集到日志管理系统中。
### 采集其它服务器的日志
上面的例子ELK服务器和产生日志的Nginx服务器在同一台服务器上，如果Nginx服务器在其它服务器上时，请先启动ELK服务。然后在产生日志的Nginx服务器上下载并解压Docker-ELK项目

1) 编辑elk-filebeat/client-sample/filebeat/filebeat.yml文件
```
output:
  logstash:
    hosts: ["yourhost:5044"]
```
替换其中的yourhost为ELK服务器的hostname或者IP

2) 在elk-filebeat/client-sample中目录中执行
```
docker-compose up
```
## 使用elk-forwarder
1) 编辑/etc/hosts文件，将elk-server指向127.0.0.1

2) 在elk-forwarder目录中执行
```
docker-compose up
```
即可启动项目。等待项目成功启动以后，访问[http://yourhost:5601](http://)即可打开Kibana界面。访问Apache的自带页面[http://yourhost:8080](http://)，就可以在Kibana界面中看到访问日志被采集到日志管理系统中。
### 采集其它服务器的日志
上面的例子ELK服务器和产生日志的Apache服务器在同一台服务器上，如果Apache服务器在其它服务器上时，请先启动ELK服务。然后在产生日志的Apache服务器上下载并解压Docker-ELK项目

1) 编辑/etc/hosts文件，将elk-server指向ELK服务器的IP
```
127.0.0.1  localhost elk-server
```
2) 在elk-forwarder/client_sample目录中执行
```
docker-compose up
```
### (可选)生成SSL Key
执行以下命令，即当前目录的子目录certs中生成SSL Key。
```
docker run --rm -e COMMON_NAME=elk-server -e KEY_NAME=logstash-forwarder -v $PWD/certs:/certs centurylink/openssl
```
要注意保持COMMON_NAME和logstash-forward-config.json文件中的"servers"列表保持一致，否则会遇到SSL握手失败的异常。
###( 可选)编译logstash-forwarder
logstash-forwarder是用go语言编译的，下载[logstash-forwarder](https://github.com/elastic/logstash-forwarder)并解压，在解压后的目录中执行以下命令即可编译最新版本的logstash-forwarder
```
docker run --rm -v "$PWD":/usr/src/logstash-forwarder -w /usr/src/logstash-forwarder golang go build -v
```
## 参考资料
[Filebeat Reference](https://www.elastic.co/guide/en/beats/filebeat/current/filebeat-overview.html)

[ELK Docker Sample](https://github.com/elastic/examples/tree/master/ELK_docker_setup/v2)