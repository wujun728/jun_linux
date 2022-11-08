系统配置：CentOS7.6 4核4G
ELK版本：7.7.1
elastic官网地址：https://www.elastic.co/cn/
elastic产品地址：https://www.elastic.co/cn/elastic-stack
yum源地址：https://mirrors.tuna.tsinghua.edu.cn/elasticstack/yum

前言
日志主要包括系统日志和应用程序日志，运维和开发人员可以通过日志了解服务器中软硬件的信息，检查应用程序或系统的故障，了解故障出现的原因，以便解决问题。分析日志可以更清楚的了解服务器的状态和系统安全状况，从而可以维护服务器稳定运行。

ELK简介
ELK主要由ElasticSearch、Logstash和Kibana三个开源工具组成，还有其他专门由于收集数据的轻量型数据采集器Beats。

Elasticsearch ：分布式搜索引擎。具有高可伸缩、高可靠、易管理等特点。可以用于全文检索、结构化检索和分析，并能将这三者结合起来。Elasticsearch 是用Java 基于 Lucene 开发，现在使用最广的开源搜索引擎之一，Wikipedia 、StackOverflow、Github 等都基于它来构建自己的搜索引擎。

在elasticsearch中，所有节点的数据是均等的。

Logstash ：数据收集处理引擎。支持动态的从各种数据源搜集数据，并对数据进行过滤、分析、丰富、统一格式等操作，然后存储以供后续使用。

Kibana ：可视化化平台。它能够搜索、展示存储在 Elasticsearch 中索引数据。使用它可以很方便的用图表、表格、地图展示和分析数据。

Filebeat：轻量级数据收集引擎。相对于Logstash所占用的系统资源来说，Filebeat 所占用的系统资源几乎是微乎及微。它是基于原先 Logstash-fowarder 的源码改造出来。换句话说：Filebeat就是新版的 Logstash-fowarder，也会是 ELK Stack 在 Agent 的第一选择。

版本说明：
Elasticsearch、Logstash、Kibana、Filebeat安装的版本号必须全部一致,不然会出现kibana无法显示web页面。

ELK常见的几种架构：
1 Elasticsearch + Logstash + Kibana
这是一种最简单的架构。这种架构，通过logstash收集日志，Elasticsearch分析日志，然后在Kibana(web界面)中展示。这种架构虽然是官网介绍里的方式，但是往往在生产中很少使用。

2 Elasticsearch + Logstash + filebeat + Kibana
与上一种架构相比，这种架构增加了一个filebeat模块。filebeat是一个轻量的日志收集代理，用来部署在客户端，优势是消耗非常少的资源(较logstash)， 所以生产中，往往会采取这种架构方式，但是这种架构有一个缺点，当logstash出现故障， 会造成日志的丢失。

3 Elasticsearch + Logstash + filebeat + redis(也可以是其他中间件，比如RabbitMQ) + Kibana
这种架构是上面那个架构的完善版，通过增加中间件，来避免数据的丢失。当Logstash出现故障，日志还是存在中间件中，当Logstash再次启动，则会读取中间件中积压的日志。

架构图：



 1.部署elasticsearch

1.1.查看是否安装docker

[root@elasticsearch ~]# docker version
Client:
 Version:           18.06.1-ce
 API version:       1.38
 Go version:        go1.10.3
 Git commit:        e68fc7a
 Built:             Tue Aug 21 17:23:03 2018
 OS/Arch:           linux/amd64
 Experimental:      false

Server:
 Engine:
  Version:          18.06.1-ce
  API version:      1.38 (minimum version 1.12)
  Go version:       go1.10.3
  Git commit:       e68fc7a
  Built:            Tue Aug 21 17:25:29 2018
  OS/Arch:          linux/amd64
  Experimental:     false

需要注意的是，如果操作系统版本不是很新不要安装最新版本docker，比如我centos7.2安装docker最新版，后面出现 linux 与 docker 版本的兼容性问题，报错”container init exited prematurely“，卸载docker安装较早版本即可。

注意：关闭selinux、firewall、iptables，防火墙不关闭需对应放通端口，我直接关闭

1.2.查找安装elasticsearch镜像

docker search elasticsearch
docker pull elasticsearch:7.7.1
等待安装完成，查看elasticsearch镜像是否已加载。

[root@elasticsearch ~]# docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
logstash            7.7.1               7f059e3dee67        20 months ago       788MB
kibana              7.7.1               6de54f813b39        20 months ago       1.2GB
elasticsearch       7.7.1               830a894845e3        20 months ago       804MB
1.3.创建挂载目录

mkdir -p /data/elk/es/{config,data,logs}
1.4.赋予权限
docker中elasticsearch的用户UID是1000.

chown -R 1000:1000 /data/elk/es
1.5.创建挂载用配置

cd /data/elk/es/config
touch elasticsearch.yml
-----------------------配置内容----------------------------------
cluster.name: "my-es"
network.host: 0.0.0.0
http.port: 9200
1.6.运行elasticsearch
通过镜像，启动一个容器，并将9200和9300端口映射到本机（elasticsearch的默认端口是9200，我们把宿主环境9200端口映射到Docker容器中的9200端口）。此处建议给容器设置固定ip，我这里没设置。

docker run -it  -d -p 9200:9200 -p 9300:9300 --name es -e ES_JAVA_OPTS="-Xms1g -Xmx1g" -e "discovery.type=single-node" --restart=always -v /data/elk/es/config/elasticsearch.yml:/usr/share/elasticsearch/config/elasticsearch.yml -v /data/elk/es/data:/usr/share/elasticsearch/data -v /data/elk/es/logs:/usr/share/elasticsearch/logs elasticsearch:7.7.1
1.7.验证安装是否成功

[root@elasticsearch home]# curl http://localhost:9200
{
  "name" : "0adf1765ac08",
  "cluster_name" : "my-es",
  "cluster_uuid" : "MpKqrEKySnSdwux0m7AlEA",
  "version" : {
    "number" : "7.7.1",
    "build_flavor" : "default",
    "build_type" : "docker",
    "build_hash" : "ad56dce891c901a492bb1ee393f12dfff473a423",
    "build_date" : "2020-05-28T16:30:01.040088Z",
    "build_snapshot" : false,
    "lucene_version" : "8.5.1",
    "minimum_wire_compatibility_version" : "6.8.0",
    "minimum_index_compatibility_version" : "6.0.0-beta1"
  },
  "tagline" : "You Know, for Search"
}

此处我在安装时在宿主机无法访问容器内的es，报错curl: (56) Recv failure: Connection reset by peer，折腾很久解决，问题解决方法见我的另一篇文章：链接。前面的配置已纠正该问题，所以参考本文配置不会出现该问题。

2.部署kibana

2.1.安装kibana

docker pull kibana:7.7.1
docker images查看是否完成

2.2.获取elasticsearch容器ip

[root@elasticsearch home]# docker inspect --format '{{ .NetworkSettings.IPAddress }}' es
172.17.0.2
2.3.配置文件
在服务器上新建配置文件，用于docker文件映射。所使用目录需对应新增。
vi /data/elk/kibana/kibana.yml

#Default Kibana configuration for docker target
server.name: kibana
server.host: "0"
elasticsearch.hosts: ["http://172.17.0.2:9200"]
xpack.monitoring.ui.container.elasticsearch.enabled: true
2.4.运行kibana

docker run -d --restart=always --log-driver json-file --log-opt max-size=100m --log-opt max-file=2 --name kibana -p 5601:5601 -v /data/elk/kibana/kibana.yml:/usr/share/kibana/config/kibana.yml kibana:7.7.1
2.5.访问
浏览器上输入：http://ip:5601，如无法访问进容器检查配置是否生效

2.6.检查kibana容器配置文件
将配置文件中elasticsearch.hosts地址修改为elasticsearch容器地址。

docker exec -it kibana /bin/bash

vi config/kibana.yml，修改后的配置如下：

#Default Kibana configuration for docker target
server.name: kibana
server.host: "0"
elasticsearch.hosts: ["http://172.17.0.2:9200"]
xpack.monitoring.ui.container.elasticsearch.enabled: true
重启kibana：docker restart kibana

2.7.重新访问
浏览器上输入：http://ip:5601，由于启动较慢，可多刷新几次。



 3.部署logstash
3.1.获取logstash镜像

docker pull logstash:7.7.1
3.2.编辑logstash.yml配置文件。所使用目录需对应新增。

vi /data/elk/logstash/logstash.yml

http.host: "0.0.0.0"
xpack.monitoring.elasticsearch.hosts: [ "http://172.17.0.2:9200" ]
xpack.monitoring.elasticsearch.username: elastic
xpack.monitoring.elasticsearch.password: changeme
#path.config: /data/elk/logstash/conf.d/*.conf
path.config: /data/docker/logstash/conf.d/*.conf
path.logs: /var/log/logstash
3.3.编辑logstash.conf文件，此处先配置logstash直接采集本地数据发送至es

vi /data/elk/logstash/conf.d/syslog.conf 

input {
  syslog {
    type => "system-syslog"
    port => 5044
  }
}
output {
  elasticsearch {
    hosts => ["192.168.200.94:9200"]  # 定义es服务器的ip
    index => "system-syslog-%{+YYYY.MM}" # 定义索引
  }
}
编辑本地rsyslog配置增加：

vi /etc/rsyslog.conf #增加一行
*.* @@192.168.200.94:5044
#配置修改后重启服务

systemctl restart rsyslog
3.4.运行logstash

docker run -d --restart=always --log-driver json-file --log-opt max-size=100m --log-opt max-file=2 -p 5044:5044 --name logstash -v /data/elk/logstash/logstash.yml:/usr/share/logstash/config/logstash.yml -v /data/elk/logstash/conf.d/:/data/docker/logstash/conf.d/ logstash:7.7.1
3.5.测试es接收logstash数据

[root@elk logstash]# curl http://localhost:9200/_cat/indices?v
health status index                    uuid                   pri rep docs.count docs.deleted store.size pri.store.size
green  open   .apm-custom-link         WBgbpphkQCS73sfjjIG0-Q   1   0          0            0       208b           208b
green  open   .kibana_task_manager_1   xmBASGi9QheR-r8hG2XLZA   1   0          5            0       28kb           28kb
green  open   .apm-agent-configuration MsvsgveHSCOhBQRCgTnsRg   1   0          0            0       208b           208b
yellow open   system-syslog-2022.02    1Vcjw7Q-TTqVscpknyK7HA   1   1          6            0     20.7kb         20.7kb
green  open   .kibana_1                vJ-B5wakRSmOrwM6ri-xgw   1   0         84            2      115kb          115kb
获取到system-syslog-相关日志，则es已能获取来自logstash的数据，kibana中也同步显示数据。

 4.部署filebeat

在需要监测的机器yum安装filebeat

wget https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-7.7.1-x86_64.rpm
rpm -ivh filebeat-7.7.1-x86_64.rpm
filebeat配置，此处先配置filebeat直接发送数据到es

#=========================== Filebeat inputs =============================
filebeat.inputs:
- type: log
  enabled: true
  paths:
    #- /var/log/*.log
    - /var/log/messages
      #- c:\programdata\elasticsearch\logs\*
#-------------------------- Elasticsearch output ------------------------------
output.elasticsearch:
  # Array of hosts to connect to.
  hosts: ["192.168.200.94:9200"]
#----------------------------- Logstash output --------------------------------
#output.logstash:
  # The Logstash hosts
  #hosts: ["192.168.200.94:5044"]

启动服务

systemctl restart filebeat.service
es接收数据查询

[root@elk conf.d]# curl http://localhost:9200/_cat/indices?v
health status index                            uuid                   pri rep docs.count docs.deleted store.size pri.store.size
yellow open   filebeat-7.7.1-2022.02.04-000001 vHSJTNWARySiC7IOOSABtw   1   1      11528            0      2.9mb          2.9mb
green  open   .apm-custom-link                 WBgbpphkQCS73sfjjIG0-Q   1   0          0            0       208b           208b
green  open   .kibana_task_manager_1           xmBASGi9QheR-r8hG2XLZA   1   0          5            0     64.1kb         64.1kb
green  open   .apm-agent-configuration         MsvsgveHSCOhBQRCgTnsRg   1   0          0            0       208b           208b
green  open   .kibana_1                        vJ-B5wakRSmOrwM6ri-xgw   1   0        158            3    101.5kb        101.5kb
可查到filebeat-7.7.1-*数据，kibana中也显示对应数据。

5.filebeat采集数据，logstash过滤，在kibana中显示

5.1删除之前的logstash生成的测试数据

curl -XDELETE http://localhost:9200/system-syslog-2022.02
5.2修改filebeat.yml，后重启服务

#-------------------------- Elasticsearch output ------------------------------
#output.elasticsearch:
  # Array of hosts to connect to.
  #hosts: ["192.168.200.94:9200"]
#----------------------------- Logstash output --------------------------------
output.logstash:
  # The Logstash hosts
  hosts: ["192.168.200.94:5044"]
5.3将之前的syslog.conf重命名为syslog.conf.bak，增加logstash配置 ，其中可增加过滤相关配置，此处未配置。

vi /data/elk/logstash/conf.d/logstash.conf

input {
  beats {
    port => 5044
  }
}
output {
  elasticsearch {
    hosts => ["172.17.0.2:9200"]
    index => "filebeat_g-%{+YYYY.MM.dd}"
  }
}
5.4查看es是否获取数据

[root@elk conf.d]# curl http://localhost:9200/_cat/indices?v
health status index                            uuid                   pri rep docs.count docs.deleted store.size pri.store.size
green  open   .apm-custom-link                 WBgbpphkQCS73sfjjIG0-Q   1   0          0            0       208b           208b
yellow open   filebeat-2022.02.04              sVdMntvdQb6YIdjpeSFNrg   1   1         43            0    130.9kb        130.9kb
yellow open   filebeat-7.7.1-2022.02.04-000001 vHSJTNWARySiC7IOOSABtw   1   1      11623            0        3mb            3mb
green  open   .kibana_task_manager_1           xmBASGi9QheR-r8hG2XLZA   1   0          5            0     64.1kb         64.1kb
green  open   .apm-agent-configuration         MsvsgveHSCOhBQRCgTnsRg   1   0          0            0       208b           208b
yellow open   filebeat_g-2022.02.04           njA2A64zS16W3YMpPMzHQA   1   1          5            0    103.4kb        103.4kb
green  open   .kibana_1                        vJ-B5wakRSmOrwM6ri-xgw   1   0        163            3     81.5kb         81.5kb
filebeat_g-*数据已经获取，kibana中增加相关索引即可。

5.5kibana增加索引







 至此安装完成。

后记：本文只是实践并记录了ELK的docker安装方式，参考了下列文档，但这些文档中配置文件较多错误所以自己按调整过的正确配置编辑了本文，仅供参考。

1.ELK详细安装部署_xllove2008的博客-CSDN博客_elk部署

2.ELK 架构之 Logstash 和 Filebeat 安装配置 - 田园里的蟋蟀 - 博客园

3.Linux搭建ELK日志收集系统：FIlebeat+Redis+Logstash+Elasticse
————————————————
版权声明：本文为CSDN博主「yuemancanyang」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/yuemancanyang/article/details/122769308