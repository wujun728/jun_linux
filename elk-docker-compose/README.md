###  elk集成环境 - docker-compose构建脚本

#### 1.前言
- 1.本仓库只为快速创建 `elasticsearch+logstash+kibana`  集成环境，主要为项目所产生的日志文件，提供顶级解决方案。 
- 2.此外,我们已经集成了 ip 转 geo 位置信息数据库,应用程序日志解决方案已经非常全面了.  
- elk 工作原理  
 ![elk工作原理](https://www.ginskeleton.com/images/elk_struct.png)

#### 2.ELK 统一设置版本号 
- 1.`docker-compose.yml` 同目录的 `.env` 文件可以设置 `elk` 版本号，例如：默认为 `7.13.3` .
- 2.官方最新版本号查看地址：[elasticsearch官网版本](https://www.elastic.co/cn/downloads/elasticsearch)   
- 3.ELK 版本每次升级都都可能导致出现语法方面的兼容性问题，因此升级最新版本前请做好测试工作.     
 

#### 3.ELK 各个子项配置介绍

- elasticsearch 配置   
 必须按照我们提供的配置项自行做检查与确认,例如：给日志目录初始化权限，否则 elasticsearch 启动报错.  
```code   
# 配置文件目录 
 elasticsearch > config 
 # 如果服务器配置比较高，建议将 jvm.options 配置文件中的内存使用设置大一点，例如 默认为 1g，可以设置为 2g 
    -Xms1g
    -Xmx1g
    
 # 特别注意（这里最容易报错，导致容器启动失败）：
 # 按照用户组、用户id分配权限，1000 、1000 分别表示容器内的 elasticsearch 组 和 elasticsearch 用户
 chown  -R   1000:1000  ./elasticsearch/*
    
```

- kibana 配置
> kibana 主要提供界面展示系统，他需要连接 elasticsearch 获取数据，默认配置使用即可，不需要修改.  
```code   

# 配置文件目录 , 可以在这里查询具体配置，默认即可
 kibana > config 
    
```

- logstash 配置
- 如果您的应用日志分布在多台服务器，请参考 logstash 独立部署版本：http://gitee.com/daitougege/elk-logstash

> 1.logstash 可以分布在任何服务器，负责采集 nginx、go应用程序的日志，向 elasticsearch 服务器发送日志.如果你的应用程序产生的日志是独立的服务器，那么就需要在每台应用服务器安装.    
> 2.注意: logstash 采集的目标日志必须是 json 格式,例如 nginx 日志需要 json化等,此部分您可以参考：https://gitee.com/daitougege/GinSkeleton/blob/master/docs/elk_log.md.    
```code   

# 配置文件目录 ,
 logstash > config 
          > pipeline   
          
  # 其中 config 目录主要配置 logstash 本身的参数
   1.  logstash > config  > jvm.options 可以限制内存使用 ，默认为 512M ,如果服务器配置高，可以设置为 1g  
     -Xms512m
     -Xmx512m
   2.  logstash > config  > logstash.yml 可以配置数据对接的 elasticsearch 服务器ip等参数，默认即可
   
   # 本配置项定义 logstash 需要采集的目标日志文件路径、名称以及发送到 elasticsearch 服务器时的文件名等，相对比较复杂。
   # 请参考我们提供的格式修改即可，这样是最简单的办法.  
   # 一个应用程序需要配置一个日志路径、文件名
   3.  logstash > pipeline  > logstash.conf 配置采集的日志对象处理逻辑，请参考默认的格式配置即可
```

#### 4.快速安装与启动
```code  
 # 1.安装 docker 环境,如果没有docker环境，请先百度一下，安装。
 # 1.安装 docker-compose 环境,如果没有 docker-compose 扩展，参考 http://github.com/docker/compose/ 
 # 3.下载/克隆 本项目,在 docker-compose.yml 同目录执行命令 docker-compose  up -d  即可
```
![elk启动效果图](https://www.ginskeleton.com/images/elk_status.png)  

#### 5.注意事项  
- 1.本仓库提供的是 elk 集成环境,如果是中大型项目,可能 logstash 分布在多台服务器，那么服务器只需要安装 elasticsearch+kibana 即可.  
- 2.请自行在 docker-compose.yml 文件屏蔽 logstash 相关项即可。
- 3.独立安装 logstash ,请屏蔽 elasticsearch+kibana  项即可。  
- 4.以上操作都只是基于我们提供的docker-compose.yml 文件，您进行合适的选择即可.

#### 6.访问与指标采集设置操作  
> 现在我们可以访问kibana地址：`http://172.21.0.13:5601` , 如果是云服务器就使用外网地址访问即可.  
> 以下操作基本都是可视化界面，通过鼠标点击等操作完成，我就以截图展示一个完整的主线操作流程, 其他知识请自行查询官网或者加我们的项目群咨询讨论.  
![步骤1](https://www.ginskeleton.com/images/elk001.png)     
![步骤2](https://www.ginskeleton.com/images/elk002.png)      
![步骤3](https://www.ginskeleton.com/images/elk003.png)      
![步骤4](https://www.ginskeleton.com/images/elk004.png)

> 特别说明：以下数据是基于测试环境, 有一些数据是直接把老项目的日志文件覆盖到指定位置，所以界面的查询日期跨度比较大.  
> nginx access 的日志  
![nginx_access日志](https://www.ginskeleton.com/images/elk005.png)

>> goskeleton 的日志  
![goskeleton的elk日志](https://www.ginskeleton.com/images/elk006.png)

> nginx error 的日志  
![nginx_access日志](https://www.ginskeleton.com/images/elk007.png)


#### 7.更炫酷未来
> 基于以上数据我们可以在 elk 做数据统计、分析，例如：可视化展示网站访问量. 哪些接口访问最多、哪些接口访问最耗时，就需要优先优化。
> elk 能做的事情超乎你的想象(机器学习、数据关联性分析、地理位置分布分析、各种图形化等等), 请参考官方提供的可视化模板，自己做数据展示设计即可。  
> 比较遗憾的是我们做的模板无法直接分享给其他人,只能分享最终的效果，其他开发者可自行参考制作自己的展示模板.          
![logstash样图](https://www.ginskeleton.com/images/logstash1.png)  