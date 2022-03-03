[Kubernetes实战总结](https://www.cnblogs.com/leozhanggg/p/12837025.html)

------

# >>> 目录 <<<

------

## 一、概述 二、核心组件 三、基本概念 四、系统架构 五、镜像制作 六、服务编排 七、持续部署 八、故障排查

 

------

#  >>> 正文 <<<

------

#  **一、**  **概述**

![img](https://img2020.cnblogs.com/blog/1059616/202005/1059616-20200506160121529-1075155306.png)

Kubernetes是容器集群管理系统，是一个开源的平台，可以实现容器集群的自动化部署、自动扩缩容、维护等功能。Kubernetes特点**:**

☛  **可移植:** 支持公有云，私有云，混合云，多重云

☛   **可扩展:** 模块化, 插件化, 可挂载, 可组合

☛   **自动化:** 自动部署，自动重启，自动复制，自动伸缩/扩展

 

 

------

# **二、**  **核心组件**

 ![img](https://img2020.cnblogs.com/blog/1059616/202005/1059616-20200506160147297-1734941214.png)

### **1)**  **主要组件**

●  **etcd****：**保存了整个集群的状态；

●  **apiserver****：**提供了资源操作的唯一入口，并提供访问控制、API注册和发现等机制；

●  **scheduler****：**负责资源的调度，按照预定的调度策略将Pod调度到相应的机器上；

●  **controller** **manager****：**负责维护集群的状态，比如故障检测、自动扩展、滚动更新等；

●  **kubelet****：**负责维护容器的生命周期，同时也负责数据卷（CVI）和网络（CNI）的管理；

●  **kube-proxy****：**负责为Service提供集群内部的服务发现和负载均衡；

●  **Container runtime****：**负责镜像管理以及Pod和容器的真正运行（CRI）；

 

### **2)**  **扩展组件**

●  **kube-dns****：**负责为整个集群提供DNS服务

●  **Metrics****：**提供资源监控

●  **Dashboard****：**提供GUI

●  **Ingress Controller****：**为服务提供外网入口

● **Federation****：**提供跨可用区的集群

●  **Fluentd-elasticsearch**：提供集群日志采集、存储与查询

 

 

------

# **三、**  **基本概念**

![img](https://img2020.cnblogs.com/blog/1059616/202005/1059616-20200506160220501-101937147.png)

### **1)**  **集群管理**

◆ **Master****：**K8s集群的管理节点，负责整个集群的管理和控制。

◆ **Node****：**K8s集群的工作节点，负责集群中的工作负载。

◆ **Namespace****：**为K8s集群提供虚拟的隔离作用。

◆ **Label****：**通过给指定资源捆绑一个或多个不同的资源标签，来实现多维度的资源分组管理。

 

### **2)**  **资源管理**

◆ **Pod****：**K8s集群中运行部署应用的最小单元，可以支持多容器。

◆ **RC****：**K8s集群中最早的保证Pod高可用的API对象，之后扩展匹配模式新增了**RS**。

◆ **Deployment****：**一个应用模式更广的API对象，通过操作RS进行创建、更新、滚动升级服务。

◆ **StatefulSet****：**K8s提供的管理有状态应用的负载管理控制器API。

◆ **DaemonSet****：**确保其创建的Pod在集群中的每一台（或指定）Node上都运行一个副本。

◆ **Job****：**K8s用来控制批处理型任务的API对象，之后基于时间管理新增了**CronJob**。

◆ **Service****：**定义了一个服务的多个Pod逻辑合集和访问Pod的策略，实现服务发现和负载均衡。

◆ **HPA****：**实现基于CPU使用率（或在使用自定义指标）的Pod自动伸缩的功能。

 

### **3)**  **存储管理**

◆ **Secret****：**用来保存和传递密码、密钥、认证凭证这些敏感信息的对象。

◆ **ConfigMap****：**将配置信息与镜像内容分离，以使容器化的应用程序具有可移植性。

◆ **Volume****：**是Pod中能够被多个容器访问的共享目录。

◆ **PV****：**持久化存储和与之相关联的持久化存储声明（**PVC**），使得K8s集群具备了存储的逻辑抽象能力。

 

 

------

# **四、**  **系统架构**

![img](https://img2020.cnblogs.com/blog/1059616/202005/1059616-20200506155422738-253453922.png)

### **1)** **集群高可用**

K8s作为容器应用的管理中心，通过对Pod的数量进行监控，并且根据主机或容器失效的状态将新的Pod调度到其他Node上，实现了应用层的高可用性。

针对K8s集群高可用性还应包含以下两个层面的考虑：Etcd 数据存储的高可用性（至少3台）和Master组件的高可用性。

这里我们采用 Hproxy + Keepalive 高可用方案，并且与 Etcd 服务、Master组件均部署到同一节点。

 

### **2)** **控制管理**

K8s集群的管理和控制主要由Master节点负责，它来负责具体的执行过程，我们后面执行的所有命令基本都是在Master节点上运行的。

Master节点通常会占据一个独立的服务器，其主要原因是它太重要了，是整个集群的“首脑”，如果宕机或者不可用，那么对集群内容器应用的管理都将失效。

 

### **3)** **工作负载**

K8s集群中的计算能力由Node提供，最初Node称为服务节点Minion，后来改名为Node。

K8s集群中的Node也就等同于Mesos集群中的Slave节点，是所有Pod运行所在的工作主机，可以是物理机也可以是虚拟机。

 

### **4)** **系统监控**

Prometheus（普罗米修斯）是一套开源的监控、报警、时间序列数据库的组合。

基本原理是通过HTTP协议周期性抓取被监控组件的状态，这样做的好处是任意组件只要提供HTTP接口就可以接入监控系统，不需要任何SDK或者其他的集成过程。

这样做非常适合作为虚拟化环境监控系统，比如Docker、Kubernetes。

![img](https://img2020.cnblogs.com/blog/1059616/202005/1059616-20200506160038548-481015366.png)

组件说明：

■  **Prometheus****：**负责实现对K8s集群监控数据的获取，存储以及查询。

■  **PrometheusOperator****：**为Prometheus实例的部署和管理提供了简单的监视定义。

■  **KubeStateMetrics****：**是K8s集群资源使用情况的聚合器，收集数据给K8s集群内使用(如HPA)。

■  **AlertManager****：**负责将告警信息重复数据删除，分组和路由到正确的接收者集成。

■  **NodeExporter****：**用于采集集群中各个节点的资源使用情况。

■  **Grafana****：**一个跨平台的开源的度量分析和可视化工具。

 

### **5)** **日志收集**

ELK分别指Elastic公司的Elasticsearch、Logstash、Kibana。在比较旧的ELK架构中，Logstash身兼日志的采集、过滤两职。

但由于Logstash基于JVM，性能有一定限制，因此，目前业界更推荐使用Go语言开发Fliebeat代替Logstash的采集功能，Logstash只作为了日志过滤的中间件。

 

 

![img](https://img2020.cnblogs.com/blog/1059616/202005/1059616-20200506160304143-1290453471.png)

组件说明：

■  **Filebeat****：**一个轻量型的单一功能数据采集器。

■  **Logstash****：**能够同时从多个来源采集数据，转换数据，将数据发送到诸如ES中。

■  **Elasticsearch****：**一个实时、分布式、可扩展的搜索引擎，通常用于索引和搜索大量日志数据。

■  **Kibana****：**可以让用户在 ES 中使用图形和图表对数据进行可视化。

 

### **6)** **镜像仓库**

Harbor是一个开源镜像仓库，可通过基于角色的访问控制来保护镜像，新版本的Harbor还增加了扫描镜像中的漏洞并将镜像签名为受信任。

作为CNCF孵化项目，Harbor提供合规性，性能和互操作性，以帮助你跨Kubernetes和Docker等云原生计算平台持续，安全地管理镜像。

Harbor组件均以Docker容器方式启动，因此，你可以将其部署在任何支持Docker的Linux发行版上。

 ![img](https://img2020.cnblogs.com/blog/1059616/202005/1059616-20200506160406753-531423813.png)

 

 

------

# **五、**  **镜像制作**

### **1)** **镜像构建**

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

```
# 适用java1.8服务
FROM hub.jhmy.com/base/java:1.8

# 维护者
MAINTAINER zhangfan

# 工作目录
WORKDIR /root

# 复制文件到镜像
COPY *.jar .
COPY lib/ lib/
COPY hosts.bak .

# 查看当前目录
RUN ls -l .

# 容器启动时运行命令
CMD ["./run.sh"]
```

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

构建镜像示例：**docker build -t hub.jhmy.com/test/jmnbservice .**

 

### **2)** **容器结构**

当容器启动时，一个新的可写层被加载到镜像的顶部。
这一层通常被称作“容器层”，其余层都称作“镜像层”。

 ![img](https://img2020.cnblogs.com/blog/1059616/202005/1059616-20200506161706677-361388620.png)

启动容器示例：**docker run -dit --name=myapp hub.jhmy.com/test/jmnbservice**

进入容器示例：**docker exec -it jmnbservice bash**

 ![img](https://img2020.cnblogs.com/blog/1059616/202005/1059616-20200506161639752-917578364.png)

 

 

------

# **六、**  **服务编排**

### **1)** **ConfigMap****资源定义**

主要定义配置文件内容。

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

```
apiVersion: v1
kind: ConfigMap
metadata:
  name: jmnbservice
  namespace: default
data:
  application.properties: |
 
    server.port=1111
    spring.server.port=2222
    spring.dubbo.port=3333
    logging.config=classpath:logback-spring.xml
    logback.logdir=/home/jhmyPro/xsr/logs
    logback.maxHistory=7
    logback.totalSizeCap=10GB
    logback.maxFileSize=128MB
    dubbo.registry.address=zookeeper://10.11.12.13:2181
    spring.application.name=JmNbService
    ......
```

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

 

### **2)** **Deployment****资源定义**

需要定义Pod副本数、匹配标签、容器名称、对应镜像、监听端口、环境变量(java运行参数)、资源限制（cpu和memory）、挂载配置等。

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: jmnbservice
  namespace: default
spec:
  replicas: 2
  selector:
    matchLabels:
      app: jmnbservice
      project: nb
  template:
    metadata:
      labels:
        app: jmnbservice
        project: nb
      annotations:
        version: "20200321"
    spec:
      containers:
      - name: jmnbservice
        image: hub.jhmy.com/test/jmnbservice:latest
        imagePullPolicy: Always
        env:
        - name: JVM_OPTS
          value: "-Xms1024m -Xmx1024m"
        ports:
        - name: spring
          containerPort: 1111
        - name: server
          containerPort: 2222
        - name: dubbo
          containerPort: 3333
        resources:
          limits:
            cpu: 200m
            memory: 2Gi
          requests:
            cpu: 100m
            memory: 1Gi
        volumeMounts:
        - name: config
          mountPath: /root/application.properties
          subPath: application.properties
        - name: html
          mountPath: /usr/local/nginx/html/clientexe
        - name: log
          mountPath: /home
      volumes:
      - name: config
        configMap:
          name: jmnbservice
      - name: html
        persistentVolumeClaim:
          claimName: nginxhtml
      - name: log
        hostPath:
          path: /home
          type: DirectoryOrCreate
```

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

 

### **3)** **Service****资源定义**

 主要定义匹配Pod标签、暴露方式、以及暴露端口。

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

```
apiVersion: v1
kind: Service
metadata:
  name: jmnbservice
  namespace: default
spec:
  type: NodePort
  selector:
    app: jmnbservice
    project: nb
  ports:
  - name: spring
    port: 1111
    nodePort: 30121
  - name: server
    port: 2222
    nodePort: 30122
  - name: dubbo
    port: 3333
    nodePort: 30123
```

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

 

 

------

# **七、**  **持续部署**

### **1)** **部署应用**

部署应用之前，请确保相关编排文件均已开发完成。至此，我们可以执行 **kubectl create/apply** 命令进行部署。

推荐使用apply，这样可以避免重复部署时报错，而且有利于编排文件修改更新，即当你修改编排文件后，只需要再次执行apply命令即可完成更新。

当然，如果你需要确保此次部署为唯一创建且信息完整，请使用create命令,并且你可以使用 **kubectl delete** 命令删除资源。

最后我们可以使用 **-f** 标签指定具体编排文件，也可以指定路径，批量执行。

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

```
[root@k8s-32 JmDiService]# ls
ConfigMap.yaml  Deployment.yaml  Service.yaml
[root@k8s-32 JmDiService]# kubectl apply -f .
configmap/jmdiservice created
deployment.apps/jmdiservice created
service/jmdiservice created
[root@k8s-32 JmDiService]# kubectl get cm; kubectl get deploy; kubectl get svc
NAME          DATA   AGE
jmdiservice   1      70s
NAME          READY   UP-TO-DATE   AVAILABLE   AGE
jmdiservice   2/2     2            2           70s
NAME          TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)           AGE
jmdiservice   NodePort    10.102.153.176   <none>        20036:30111/TCP   69s
kubernetes    ClusterIP   10.96.0.1        <none>        443/TCP           5d16h
```

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

 

### **2)** **滚动更新**

通常进行应用升级，都是镜像版本的升级，我们可以使用 **kubectl set image** 命令设置新的镜像名称即可；

如果需要更新具体资源字段，则可以使用 **kubectl patch** 命令；当然，你也可以使用 **kubectl edit** 命令编辑资源对象。

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

```
[root@k8s-32 JmDiService]# kubectl get deployment
NAME          READY   UP-TO-DATE   AVAILABLE   AGE
jmdiservice   2/2     2            2           4h54m
[root@k8s-32 JmDiService]# kubectl set image deployment/jmdiservice jmdiservice=hub.jhmy.com/project-test/jmdiservice:latest
deployment.apps/jmdiservice image updated
[root@k8s-32 JmDiService]# kubectl patch deployment/jmdiservice --patch '{"spec": {"template": {"metadata": {"annotations":{"version": "20200506" }}}}}'
deployment.apps/jmdiservice patched
```

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

 

### **3)** **版本回滚**

我们使用上面更新应用时K8S都会记录下当前的配置文件，保存为一个revision (版本)，这样就可以通过这个版本回滚到特定的时间。

我们可以通过 **kubectl rollout history** 命令查看历史记录，并通过 **kubectl rollout undo** 撤销本次发布回滚到上一个部署版本，也可以使用--to-revision标签回滚到指定版本。

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

```
[root@k8s-32 JmDiService]# kubectl rollout history deployment/jmdiservice
deployment.apps/jmdiservice
REVISION  CHANGE-CAUSE
1         <none>
2         <none>
3         <none>

[root@k8s-32 JmDiService]# kubectl rollout undo --to-revision=2 deployment/jmdiservice
deployment.apps/jmdiservice rolled back
```

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

 

### **4)** **CICD****流程**

 ![img](https://img2020.cnblogs.com/blog/1059616/202005/1059616-20200506164127623-1490653987.png)

 

 

 

------

# **八、**  **故障排查**

### **1)** **查看系统Event**

通过 **kubectl describe pod** 命令，可以显示Pod创建时的配置定义、状态等信息，还可以显示与该Pod相关的最近的Event事件， 事件信息对于查错非常有用。

 ![img](https://img2020.cnblogs.com/blog/1059616/202005/1059616-20200506163341109-981750425.png)

 

### **2)** **查看容器日志**

在需要排查容器内部应用程序生成的日志时， 我们可以使用 **kubectl logs ** 命令。

 ![img](https://img2020.cnblogs.com/blog/1059616/202005/1059616-20200506163402499-154353064.png)

 

### **3)** **查看K8s服务日志**

K8s服务默认使用systemd系统管理，那么systemd的journal系统会接管服务程序的输出日志。

我们可以 **tailf /var/log/messages** 查看系统日志，也可以使用 **journalctl** 工具来查看k8s组件的日志。

 ![img](https://img2020.cnblogs.com/blog/1059616/202005/1059616-20200506163428608-777966006.png)

 

### **4)** **寻求帮助**

◎ Kubernetes官方网站任务详解：https://kubernetes.io/zh/docs/tasks/

◎ Kubernetes GitHub库问题列表：https://github.com/kubernetes/kubernetes/issues

 ![img](https://img2020.cnblogs.com/blog/1059616/202005/1059616-20200506163512671-189750593.png)

 

 

> 作者：[Leozhanggg](https://www.cnblogs.com/leozhanggg/)
>
> 出处：https://www.cnblogs.com/leozhanggg/p/12837025.html