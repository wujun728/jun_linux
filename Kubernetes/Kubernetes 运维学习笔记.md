 

**一、Kubernetes 介绍**

Kubernetes是一个全新的基于容器技术的分布式架构领先方案, 它是Google在2014年6月开源的一个容器集群管理系统，使用Go语言开发，Kubernetes也叫K8S。K8S是Google内部一个叫Borg的容器集群管理系统衍生出来的，Borg已经在Google大规模生产运行十年之久。K8S主要用于自动化部署、扩展和管理容器应用，提供了资源调度、部署管理、服务发现、扩容缩容、监控等一整套功能。2015年7月，Kubernetes v1.0正式发布，截止到2017年9月29日最新稳定版本是v1.8。Kubernetes目标是让部署容器化应用简单高效。

Kubernetes最初源于谷歌内部的Borg，提供了面向应用的容器集群部署和管理系统。Kubernetes 的目标旨在消除编排物理/虚拟计算，网络和存储基础设施的负担，并使应用程序运营商和开发人员完全将重点放在以容器为中心的原语上进行自助运营。Kubernetes 也提供稳定、兼容的基础（平台），用于构建定制化的workflows 和更高级的自动化任务。

Kubernetes 具备完善的集群管理能力，包括多层次的安全防护和准入机制、多租户应用支撑能力、透明的服务注册和服务发现机制、内建负载均衡器、故障发现和自我修复能力、服务滚动升级和在线扩容、可扩展的资源自动调度机制、多粒度的资源配额管理能力。Kubernetes 还提供完善的管理工具，涵盖开发、部署测试、运维监控等各个环节。

**二、Kubernetes主要功能**

Kubernetes是docker容器用来编排和管理的工具，它是基于Docker构建一个容器的调度服务，提供资源调度、均衡容灾、服务注册、动态扩缩容等功能套件。Kubernetes提供应用部署、维护、 扩展机制等功能，利用Kubernetes能方便地管理跨机器运行容器化的应用，其主要功能如下：

数据卷: Pod中容器之间共享数据，可以使用数据卷。

应用程序健康检查: 容器内服务可能进程堵塞无法处理请求，可以设置监控检查策略保证应用健壮性。

复制应用程序实例: 控制器维护着Pod副本数量，保证一个Pod或一组同类的Pod数量始终可用。

弹性伸缩: 根据设定的指标（CPU利用率）自动缩放Pod副本数。

服务发现: 使用环境变量或DNS服务插件保证容器中程序发现Pod入口访问地址。

负载均衡: 一组Pod副本分配一个私有的集群IP地址，负载均衡转发请求到后端容器。在集群内部其他Pod可通过这个ClusterIP访问应用。

滚动更新: 更新服务不中断，一次更新一个Pod，而不是同时删除整个服务。

服务编排: 通过文件描述部署服务，使得应用程序部署变得更高效。

资源监控: Node节点组件集成cAdvisor资源收集工具，可通过Heapster汇总整个集群节点资源数据，然后存储到InfluxDB时序数据库，再由Grafana展示。

提供认证和授权: 支持属性访问控制（ABAC）、角色访问控制（RBAC）认证授权策略。

**除此之外, Kubernetes主要功能还体现在:**
**-** 使用Docker对应用程序包装(package)、实例化(instantiate)、运行(run)。
**-** 将多台Docker主机抽象为一个资源，以集群的方式运行、管理跨机器的容器，包括任务调度、资源管理、弹性伸缩、滚动升级等功能。
**-** 使用编排系统（YAML File）快速构建容器集群，提供负载均衡，解决容器直接关联及通信问题
**-** 解决Docker跨机器容器之间的通讯问题。
**-** 自动管理和修复容器，简单说，比如创建一个集群，里面有十个容器，如果某个容器异常关闭，那么，会尝试重启或重新分配容器，始终保证会有十个容器在运行，反而杀死多余的。Kubernetes的自我修复机制使得容器集群总是运行在用户期望的状态. 当前Kubernetes支持GCE、vShpere、CoreOS、OpenShift。

kubernetes的集群至少有两个主机组成：master + node ，即为master/node架构。master为集群的控制面板，master主机需要做冗余，一般建议为3台；而node主机不需要做冗余，因为node的主要作用是运行pod，贡献计算能力和存储能力，而pod控制器会自动管控pod资源，如果资源少，pod控制器会自动创建pod，即pod控制器会严格按照用户指定的副本来管理pod的数量。客户端的请求下发给master,即把创建和启动容器的请求发给master，master中的调度器分析各node现有的资源状态，把请求调用到对应的node启动容器。

可以理解为kubernetes把容器抽象为pod来管理1到多个彼此间有非常紧密联系的容器，但是LAMP的容器主机A,M,P只是有关联，不能说是非常紧密联系，因此A,M,P都要运行在三个不同的pod上。在kubernetes中，要运行几个pod，是需要定义一个配置文件，在这个配置文件里定义用哪个控制器启动和控制几个pod，在每个pod里要定义那几台容器，kubernetes通过这个配置文件，去创建一个控制器，由此控制器来管控这些pod,如果这些pod的某几个down掉后，控制器会通过健康监控功能，随时监控pod，发现pod异常后,根据定义的策略进行操作，即可以进行自愈。

**kubernetes内部需要5套证书，手动创建或者自动生成，分别为：**
**1.** etcd内部通信需要一套ca和对应证书。
**2.** etcd与外部通信也要有一套ca和对应证书。
**3.** APIserver间通信需要一套证书。
**4.** apiserver与node间通信需要一套证书。
**5.** node和pod间通信需要一套ca证书。

目前来说还不能实现把所有的业务都迁到kubernetes上，如存储，因为这个是有状态应用，出现错误排查很麻烦，所以目前kubernetes主要是运行无状态应用。

所以一般而言，负载均衡器运行在kubernetes之外，nginx或者tomcat这种无状态的应用运行于kubernetes集群内部，而数据库如mysql，zabbix，zoopkeeper等有状态的，一般运行于kubernetes外部，通过网络连接，实现kubernetes集群的pod调用这些外部的有状态应用。

**三、Kubernetes架构和组件**

![img](https://img2018.cnblogs.com/blog/907596/201903/907596-20190313230043695-283099100.jpg)

**kubernetes主要由以下几个核心组件组成：**
etcd: 集群的主数据库，保存了整个集群的状态; etcd负责节点间的服务发现和配置共享。etcd分布式键值存储系统, 用于保持集群状态，比如Pod、Service等对象信息。
kube-apiserver: 提供了资源操作的唯一入口，并提供认证、授权、访问控制、API注册和发现等机制；这是kubernetes API，作为集群的统一入口，各组件协调者，以HTTPAPI提供接口服务，所有对象资源的增删改查和监听操作都交给APIServer处理后再提交给Etcd存储。
kube-controller-manager: 负责维护集群的状态，比如故障检测、自动扩展、滚动更新等；它用来执行整个系统中的后台任务，包括节点状态状况、Pod个数、Pods和Service的关联等, 一个资源对应一个控制器，而ControllerManager就是负责管理这些控制器的。
kube-scheduler: 资源调度，按照预定的调度策略将Pod调度到相应的机器上；它负责节点资源管理，接受来自kube-apiserver创建Pods任务，并分配到某个节点。它会根据调度算法为新创建的Pod选择一个Node节点。
kubectl: 客户端命令行工具，将接受的命令格式化后发送给kube-apiserver，作为整个系统的操作入口。
kubelet: 负责维护容器的生命周期，负责管理pods和它们上面的容器，images镜像、volumes、etc。同时也负责Volume（CVI）和网络（CNI）的管理；kubelet运行在每个计算节点上，作为agent，接受分配该节点的Pods任务及管理容器，周期性获取容器状态，反馈给kube-apiserver; kubelet是Master在Node节点上的Agent，管理本机运行容器的生命周期，比如创建容器、Pod挂载数据卷、下载secret、获取容器和节点状态等工作。kubelet将每个Pod转换成一组容器。
container runtime: 负责镜像管理以及Pod和容器的真正运行（CRI）；
kube-proxy: 负责为Service提供cluster内部的服务发现和负载均衡；它运行在每个计算节点上，负责Pod网络代理。定时从etcd获取到service信息来做相应的策略。它在Node节点上实现Pod网络代理，维护网络规则和四层负载均衡工作。
docker或rocket(rkt): 运行容器。

**除了上面的几个核心组建, 还有一些常用插件**(Add-ons)：
kube-dns: 负责为整个集群提供DNS服务;
Ingress Controller: 为服务提供外网入口;
Heapster: 提供资源监控;
Dashboard: 提供GUI;
Federation: 提供跨可用区的集群;
Fluentd-elasticsearch: 提供集群日志采集、存储与查询;

其中:
master组件包括: kube-apiserver, kube-controller-manager, kube-scheduler;
Node组件包括: kubelet, kube-proxy, docker或rocket(rkt);
第三方服务：etcd

**Kubernetes Master控制组件****，调度管理整个系统（集群），包含如下组件:**
Kubernetes API Server: 作为Kubernetes系统入口，其封装了核心对象的增删改查操作，以RESTful API接口方式提供给外部客户和内部组件调用,维护的REST对象持久化到Etcd中存储。
Kubernetes Scheduler: 为新建立的Pod进行节点(node)选择(即分配机器)，负责集群的资源调度。组件抽离，可以方便替换成其他调度器。
Kubernetes Controller: 负责执行各种控制器，目前已经提供了很多控制器来保证Kubernetes的正常运行。
Replication Controller: 管理维护Replication Controller，关联Replication Controller和Pod，保证Replication Controller定义的副本数量与实际运行Pod数量一致。
Node Controller: 管理维护Node，定期检查Node的健康状态，标识出(失效|未失效)的Node节点。
Namespace Controller: 管理维护Namespace，定期清理无效的Namespace，包括Namesapce下的API对象，比如Pod、Service等。
Service Controller: 管理维护Service，提供负载以及服务代理。
EndPoints Controller: 管理维护Endpoints，关联Service和Pod，创建Endpoints为Service的后端，当Pod发生变化时，实时更新Endpoints (即Pod Ip + Container Port)。
Service Account Controller: 管理维护Service Account，为每个Namespace创建默认的Service Account，同时为Service Account创建Service Account Secret。
Persistent Volume Controller: 管理维护Persistent Volume和Persistent Volume Claim，为新的Persistent Volume Claim分配Persistent Volume进行绑定，为释放的Persistent Volume执行清理回收。
Daemon Set Controller: 管理维护Daemon Set，负责创建Daemon Pod，保证指定的Node上正常的运行Daemon Pod。
Deployment Controller: 管理维护Deployment，关联Deployment和Replication Controller，保证运行指定数量的Pod。当Deployment更新时，控制实现Replication Controller和　Pod的更新。
Job Controller: 管理维护Job，为Jod创建一次性任务Pod，保证完成Job指定完成的任务数目
Pod Autoscaler Controller: 实现Pod的自动伸缩，定时获取监控数据，进行策略匹配，当满足条件时执行Pod的伸缩动作。

![img](https://img2018.cnblogs.com/blog/907596/201903/907596-20190313230350218-1815553005.png)

**Kubernetes Node运行节点，运行管理业务容器，包含如下组件:**
Kubelet: 负责管控容器，Kubelet会从Kubernetes API Server接收Pod的创建请求，启动和停止容器，监控容器运行状态并汇报给Kubernetes API Server。
Kubernetes Proxy: 负责为Pod创建代理服务，Kubernetes Proxy会从Kubernetes API Server获取所有的Service信息，并根据Service的信息创建代理服务，实现Service到Pod的请求路由和转发，从而实现Kubernetes层级的虚拟转发网络。
Docker: Node上需要运行容器服务

![img](https://img2018.cnblogs.com/blog/907596/201903/907596-20190313230419161-405620081.png)

​                          **Kubernetes的分层设计理念**                            
Kubernetes设计理念和功能类似Linux的分层架构，如下图:

![img](https://img2018.cnblogs.com/blog/907596/201903/907596-20190313232548842-1949056485.png)

核心层：Kubernetes最核心的功能，对外提供API构建高层的应用，对内提供插件式应用执行环境;
应用层：部署(无状态应用、有状态应用、批处理任务、集群应用等)和路由(服务发现、DNS解析等);
管理层：系统度量(如基础设施、容器和网络的度量)，自动化(如自动扩展、动态Provision等)以及策略管理(RBAC、Quota、PSP、NetworkPolicy等);
接口层：kubectl命令行工具、客户端SDK以及集群联邦;
生态系统：在接口层之上的庞大容器集群管理调度的生态系统，可以划分为两个范畴:  
\- Kubernetes外部：日志、监控、配置管理、CI、CD、Workflow、FaaS、OTS应用、ChatOps等;  
\- Kubernetes内部：CRI、CNI、CVI、镜像仓库、Cloud Provider、集群自身的配置和管理等;

**四、Kubernetes基本对象概念**

Kubernetes中的大部分概念Node、Pod、Replication Controller、Service等都可以看作一种“资源对象”，几乎所有的资源对象都可以通过kubectl工具（API调用）执行增、删、改、查等操作并将其保存在etcd中持久化存储。从这个角度来看，kubernetes其实是一个高度自动化的资源控制系统，通过跟踪对比etcd库里保存的“资源期望状态”与当前环境中的“实际资源状态”的差异来实现自动控制和自动纠错的高级功能。

基本对象：
**Pod**: Pod是最小部署单元，一个Pod有一个或多个容器组成，Pod中容器共享存储和网络，在同一台Docker主机上运行; Pod 中的容器会作为一个整体被Master调度到一个Node上运行。pod 是一组container，pod里面的container是共享网络栈和存储卷等资源，是一个整体. pod 可以认为是容器组的概念，里面有个infra container 负责pod内所有container 共享 namespace。docker的容器可以类比成OS中的进程，而K8S的pod则更像是OS中的“进程组”概念。
**Service** : Service一个应用服务抽象，定义了Pod逻辑集合和访问这个Pod集合的策略。Service代理Pod集合对外表现是为一个访问入口，分配一个集群IP地址，来自这个IP的请求将负载均衡转发后端Pod中的容器。Service通过LableSelector选择一组Pod提供服务。
**Volume**: 数据卷，共享Pod中容器使用的数据。
**Namespace**: 命名空间将对象逻辑上分配到不同Namespace，可以是不同的项目、用户等区分管理，并设定控制策略，从而实现多租户。命名空间也称为虚拟集群。
**Lable**: 标签用于区分对象（比如Pod、Service），键/值对存在；每个对象可以有多个标签，通过标签关联对象。

基于基本对象更高层次抽象： 
**ReplicaSet:** 下一代ReplicationController。确保任何给定时间指定的Pod副本数量，并提供声明式更新等功能。RC与RS唯一区别就是lableselector支持不同，RS支持新的基于集合的标签，RC仅支持基于等式的标签。
**Deployment**: Deployment是一个更高层次的API对象，它管理ReplicaSets和Pod，并提供声明式更新等功能。官方建议使用Deployment管理ReplicaSets，而不是直接使用ReplicaSets，这就意味着可能永远不需要直接操作ReplicaSet对象。负责无状态应用pod控制，支持二级控制器（HPA，HorizontalPodAutoscaler水平pod自动控制器）。
**StatefulSet**: StatefulSet适合持久性的应用程序，有唯一的网络标识符（IP），持久存储，有序的部署、扩展、删除和滚动更新。负责有状态应用pod控制。
**DaemonSet**: DaemonSet确保所有（或一些）节点运行同一个Pod。当节点加入Kubernetes集群中，Pod会被调度到该节点上运行，当节点从集群中移除时，DaemonSet的Pod会被删除。删除DaemonSet会清理它所有创建的Pod。
**Job**: 一次性任务，运行完成后Pod销毁，不再重新启动新容器。还可以任务定时运行。Kubernetes中的Job 用于运行结束就删除的应用。

​                                                                       **
**

API对象是K8s集群中管理操作单元。K8s集群系每支持一项新功能，引入一项新技术，一定会新引入对应的API对象，支持对该功能的管理操作。例如副本集Replica Set对应的API对象是RS。Kubernetes中所有的配置都是通过API对象的spec去设置的，也就是用户通过配置系统的理想状态来改变系统，这是k8s重要设计理念之一，即所有的操作都是声明式 (Declarative) 的而不是命令式(Imperative)的。声明式操作在分布式系统中好处是稳定，不怕丢操作或运行多次，例如设置副本数为3的操作运行多次也还是一个结果, 而给副本数加1的操作就不是声明式的, 运行多次结果就错了。

**Cluster**
Cluster 是计算、存储和网络资源的集合，Kubernetes 利用这些资源运行各种基于容器的应用

**Master**
kubernetes集群的管理节点，负责管理集群，提供集群的资源数据访问入口。拥有Etcd存储服务（可选），运行Api Server进程，Controller Manager服务进程及Scheduler服务进程，关联工作节点Node。Kubernetes API server提供HTTP Rest接口的关键服务进程，是Kubernetes里所有资源的增、删、改、查等操作的唯一入口。也是集群控制的入口进程；Kubernetes Controller Manager是Kubernetes所有资源对象的自动化控制中心；Kubernetes Schedule是负责资源调度（Pod调度）的进程.

**Node**
Node是Kubernetes集群架构中运行Pod的服务节点（亦叫agent或minion）。Node是Kubernetes集群操作的单元，用来承载被分配Pod的运行，是Pod运行的宿主机。关联Master管理节点，拥有名称和IP、系统资源信息。运行docker eninge服务，守护进程kunelet及负载均衡器kube-proxy. 每个Node节点都运行着以下一组关键进程: 
\- kubelet：负责对Pod对于的容器的创建、启停等任务
\- kube-proxy：实现Kubernetes Service的通信与负载均衡机制的重要组件
\- Docker Engine（Docker）：Docker引擎，负责本机容器的创建和管理工作

Node节点可以在运行期间动态增加到Kubernetes集群中，默认情况下，kubelet会想master注册自己，这也是Kubernetes推荐的Node管理方式，kubelet进程会定时向Master汇报自身情报，如操作系统、Docker版本、CPU和内存，以及有哪些Pod在运行等等，这样Master可以获知每个Node节点的资源使用情况，冰实现高效均衡的资源调度策略。、

**Pod**
运行于Node节点上，若干相关容器的组合。Pod内包含的容器运行在同一宿主机上，使用相同的网络命名空间、IP地址和端口，能够通过localhost进行通。Pod是Kurbernetes进行创建、调度和管理的最小单位，它提供了比容器更高层次的抽象，使得部署和管理更加灵活。一个Pod可以包含一个容器或者多个相关容器。

Pod其实有两种类型：普通Pod和静态Pod，后者比较特殊，它并不存在Kubernetes的etcd存储中，而是存放在某个具体的Node上的一个具体文件中，并且只在此Node上启动。普通Pod一旦被创建，就会被放入etcd存储中，随后会被Kubernetes Master调度到摸个具体的Node上进行绑定，随后该Pod被对应的Node上的kubelet进程实例化成一组相关的Docker容器并启动起来。在默认情况下，当Pod里的某个容器停止时，Kubernetes会自动检测到这个问起并且重启这个Pod（重启Pod里的所有容器），如果Pod所在的Node宕机，则会将这个Node上的所有Pod重新调度到其他节点上。

Pod是在K8s集群中运行部署应用或服务的最小单元，它是可以支持多容器的。Pod的设计理念是支持多个容器在一个Pod中共享网络地址和文件系统，可以通过进程间通信和文件共享这种简单高效的方式组合完成服务.比如你运行一个操作系统发行版的软件仓库，一个Nginx容器用来发布软件，另一个容器专门用来从源仓库做同步，这两个容器的镜像不太可能是一个团队开发的，但是他们一块儿工作才能提供一个微服务；这种情况下，不同的团队各自开发构建自己的容器镜像，在部署的时候组合成一个微服务对外提供服务。

kubernetes的最核心功能就是为了运行pod，其他组件是为了pod能够正常运行而执行的。pod可以分为两类：
**1.** 自主式pod
**2.** 控制器管理的pod

一个pod上有两类元数据，label 和 annotation
label：标签，对数据类型和程度要求严格，
annotation：注解，用于存储自己定义的复杂元数据，用来描述pod的属性

外部请求访问内部的pod经过了三级转发，第一级先到nodeip（宿主机ip）对应的端口，然后被转为cluster ip的service 端口，然后转换为PodIP的containerPort。

**Kubernetes 引入 Pod 主要基于下面两个目的：**
\- 可管理性
有些容器天生就是需要紧密联系, 一起工作。Pod 提供了比容器更高层次的抽象，将它们封装到一个部署单元中。Kubernetes 以 Pod 为最小单位进行调度、扩展、共享资源、管理生命周期。

\- 通信和资源共享
Pod 中的所有容器使用同一个网络 namespace，即相同的 IP 地址和 Port 空间。它们可以直接用 localhost 通信。同样的，这些容器可以共享存储，当 Kubernetes 挂载 volume 到 Pod，本质上是将 volume 挂载到 Pod 中的每一个容器。

![img](https://img2018.cnblogs.com/blog/907596/201908/907596-20190806151141561-1435899737.png)

File Puller 会定期从外部的 Content Manager 中拉取最新的文件，将其存放在共享的 volume 中。Web Server 从 volume 读取文件，响应 Consumer 的请求。这两个容器是紧密协作的，它们一起为 Consumer 提供最新的数据；同时它们也通过 volume 共享数据。所以放到一个 Pod 是合适的。

**Controller**
Kubernetes 通常不会直接创建 Pod，而是通过 Controller 来管理 Pod 的。Controller 中定义了 Pod 的部署特性，比如有几个副本，在什么样的 Node 上运行等。为了满足不同的业务场景, Kubernetes 提供了多种 Controller，包括 Deployment、ReplicaSet、DaemonSet、StatefuleSet、Job 等. 

**Replication Controller (副本集RC)**
Replication Controller用来管理Pod的副本，保证集群中存在指定数量的Pod副本。集群中副本的数量大于指定数量，则会停止指定数量之外的多余容器数量，反之，则会启动少于指定数量个数的容器，保证数量不变。Replication Controller是实现弹性伸缩、动态扩容和滚动升级的核心。

通过监控运行中的Pod来保证集群中运行指定数目的Pod副本。少于指定数目，RC就会启动运行新的Pod副本；多于指定数目，RC就会杀死多余的Pod副本 (这是k8s早期技术概念)

**Replica Set (副本集RS）**
RS是新一代RC，提供同样的高可用能力，区别主要在于RS后来居上，能支持更多种类的匹配模式。副本集对象一般不单独使用，而是作为Deployment的理想状态参数使用. Replica Set 实现了 Pod 的多副本管理。使用 Deployment 时会自动创建 ReplicaSet，也就是说 Deployment 是通过 ReplicaSet 来管理 Pod 的多个副本，我们通常不需要直接使用 ReplicaSet。

**Deployment (部署)**
Deployment 是最常用的 Controller，Deployment 可以管理 Pod 的多个副本，并确保 Pod 按照期望的状态运行。Deployment是一个比RS应用模式更广的API对象，支持动态扩展。可以创建一个新的服务，更新一个新的服务，也可以是滚动升级一个服务。滚动升级一个服务，实际是创建一个新的RS，然后逐渐将新RS中副本数增加到理想状态，将旧RS中的副本数减小到0的复合操作 (逐步升级新得副本，剔除旧的副本). 
**总结：**RC、RS和Deployment只是保证了支撑服务的微服务Pod的数量.

**DaemonSet**
DaemonSet 用于每个 Node 最多只运行一个 Pod 副本的场景。正如其名称所揭示的，DaemonSet 通常用于运行 daemon。

**StatefuleSet**
StatefuleSet 能够保证 Pod 的每个副本在整个生命周期中名称是不变的。而其他 Controller 不提供这个功能，当某个 Pod 发生故障需要删除并重新启动时，Pod 的名称会发生变化。同时 StatefuleSet 会保证副本按照固定的顺序启动、更新或者删除。

**Service**

Service定义了Pod逻辑集合和访问该集合的策略，是真实服务的抽象。Service提供了统一的服务访问入口以及服务代理和发现机制，关联多个相同Label的Pod，用户不需要了解后台Pod是如何运行。
外部系统访问Service的问题:
**->** 首先需要弄明白Kubernetes的三种IP这个问题
   **-** Node IP：Node节点的IP地址
　  **-** Pod IP： Pod的IP地址
　  **-** Cluster IP：Service的IP地址
**->**  首先,Node IP是Kubernetes集群中节点的物理网卡IP地址，所有属于这个网络的服务器之间都能通过这个网络直接通信。这也表明Kubernetes集群之外的节点访问Kubernetes集群之内的某个节点或者TCP/IP服务的时候，必须通过Node IP进行通信
**->** 其次，Pod IP是每个Pod的IP地址，他是Docker Engine根据docker0网桥的IP地址段进行分配的，通常是一个虚拟的二层网络。

最后Cluster IP是一个虚拟的IP，但更像是一个伪造的IP网络，原因有以下几点: 
**->** Cluster IP仅仅作用于Kubernetes Service这个对象，并由Kubernetes管理和分配P地址
**->** Cluster IP无法被ping，他没有一个“实体网络对象”来响应
**->** Cluster IP只能结合Service Port组成一个具体的通信端口，单独的Cluster IP不具备通信的基础，并且他们属于Kubernetes集群这样一个封闭的空间。
**->** Kubernetes集群之内，Node IP网、Pod IP网于Cluster IP网之间的通信，采用的是Kubernetes自己设计的一种编程方式的特殊路由规则。

RC、RS和Deployment只是保证了支撑服务的微服务Pod的数量，但是没有解决如何访问这些服务的问题。一个Pod只是一个运行服务的实例，随时可能在一个节点上停止，在另一个节点以一个新的IP启动一个新的Pod，因此不能以确定的IP和端口号提供服务。要稳定地提供服务需要服务发现和负载均衡能力。服务发现完成的工作，是针对客户端访问的服务，找到对应的的后端服务实例。在K8s集群中，客户端需要访问的服务就是Service对象。每个Service会对应一个集群内部有效的虚拟IP，集群内部通过虚拟IP访问一个服务。在K8s集群中微服务的负载均衡是由Kube-proxy实现的。Kube-proxy是K8s集群内部的负载均衡器。它是一个分布式代理服务器，在K8s的每个节点上都有一个；这一设计体现了它的伸缩性优势，需要访问服务的节点越多，提供负载均衡能力的Kube-proxy就越多，高可用节点也随之增多。与之相比，我们平时在服务器端做个反向代理做负载均衡，还要进一步解决反向代理的负载均衡和高可用问题。

Kubernetes 运行容器（Pod）与访问容器（Pod）这两项任务分别由 Controller 和 Service 执行。

**Namespace**
名字空间为K8s集群提供虚拟的隔离作用，K8s集群初始有两个名字空间，分别是默认名字空间default和系统名字空间kube-system，除此以外，管理员可以可以创建新的名字空间满足需要。

![img](https://img2018.cnblogs.com/blog/907596/201903/907596-20190313232215198-1967204451.png)

**Label**
Kubernetes中任意API对象都是通过Label进行标识，Label的实质是一系列的Key/Value键值对，其中key于value由用户自己指定。Label可以附加在各种资源对象上，如Node、Pod、Service、RC等，一个资源对象可以定义任意数量的Label，同一个Label也可以被添加到任意数量的资源对象上去。Label是Replication Controller和Service运行的基础，二者通过Label来进行关联Node上运行的Pod。

我们可以通过给指定的资源对象捆绑一个或者多个不同的Label来实现多维度的资源分组管理功能，以便于灵活、方便的进行资源分配、调度、配置等管理工作。
一些常用的Label如下：
版本标签："release":"stable","release":"canary"......
环境标签："environment":"dev","environment":"qa","environment":"production"
架构标签："tier":"frontend","tier":"backend","tier":"middleware"
分区标签："partition":"customerA","partition":"customerB"
质量管控标签："track":"daily","track":"weekly"

Label相当于我们熟悉的标签，给某个资源对象定义一个Label就相当于给它大了一个标签，随后可以通过Label Selector（标签选择器）查询和筛选拥有某些Label的资源对象，Kubernetes通过这种方式实现了类似SQL的简单又通用的对象查询机制。

Label Selector在Kubernetes中重要使用场景如下:
**->** kube-Controller进程通过资源对象RC上定义Label Selector来筛选要监控的Pod副本的数量，从而实现副本数量始终符合预期设定的全自动控制流程;
**->** kube-proxy进程通过Service的Label Selector来选择对应的Pod，自动建立起每个Service岛对应Pod的请求转发路由表，从而实现Service的智能负载均衡;
**->** 通过对某些Node定义特定的Label，并且在Pod定义文件中使用Nodeselector这种标签调度策略，kuber-scheduler进程可以实现Pod”定向调度“的特性;

​                                                                                 
**Master管理节点和Node工作节点的各组件关系:**

![img](https://img2018.cnblogs.com/blog/907596/201905/907596-20190531165628671-14705824.png)

Kuberneter工作流程：
1）通过kubectl向kubernetes Master发出指令, Master节点主要提供API Server、Scheduler、Controller组件，接收kubectl命令，从Node节点获取Node资源信息，并发出调度任务。
2）Node节点提供kubelet、kube-proxy，每个node节点都安装docker，是实际的执行者。kubernetes不负责网络，所以一般是用flannel或者weave。
3）etcd是一个键值存储仓库，etcd负责服务发现和node信息存储。**不过需要注意的是：**由于etcd是负责存储，所以不建议搭建单点集群，如zookeeper一样，由于存在选举策略，所以一般推荐奇数个集群，如3，5，7。只要集群半数以上的结点存活，那么集群就可以正常运行，否则集群可能无法正常使用。

**Master**：集群控制管理节点，所有的命令都经由master处理。

![img](https://img2018.cnblogs.com/blog/907596/201903/907596-20190313222141535-880155421.png)

**Node**：是kubernetes集群的工作负载节点。Master为其分配工作，当某个Node宕机时，Master会将其工作负载自动转移到其他节点。

![img](https://img2018.cnblogs.com/blog/907596/201903/907596-20190313222650824-93538855.png)

Node节点可动态增加到kubernetes集群中，前提是这个节点已经正确安装、配置和启动了上述的关键进程，默认情况下，kubelet会向Master注册自己，这也kubernetes推荐的Node管理方式。一旦Node被纳入集群管理范围，kubelet会定时向Master汇报自身的情况，以及之前有哪些Pod在运行等，这样Master可以获知每个Node的资源使用情况，并实现高效均衡的资源调度策略。如果Node没有按时上报信息，则会被Master判断为失联，Node状态会被标记为Not Ready，随后Master会触发工作负载转移流程。

**Pod**：是kubernetes最重要也是最基本的概念。每个Pod都会包含一个 “根容器”，还会包含一个或者多个紧密相连的业务容器。

![img](https://img2018.cnblogs.com/blog/907596/201903/907596-20190313223036439-466023285.png)

Kubernetes为每个Pod都分配了唯一IP地址, 称之为PodIP, 一个Pod里多个容器共享PodIP地址. 要求底层网络支持集群内任意两个Pod之间的直接通信，通常采用虚拟二层网络技术来实现 (Flannel).

**Label**：是一个key=value的键值对，其中key与value由用户指定, 可以附加到各种资源对象上, 一个资源对象可以定义任意数量的Label。可以通过LabelSelector（标签选择器）查询和筛选资源对象。

![img](https://img2018.cnblogs.com/blog/907596/201903/907596-20190313223346653-822874121.png)

**RC**：Replication Controller声明某个Pod的副本数在任意时刻都符合某个预期值。定义包含如下：
\- Pod期待的副本数（replicas）;
\- 用于筛选目标Pod的Label Selector;
\- 当Pod副本数小于期望时，用于新的创建Pod的模板template;

**需要注意**
\- 通过改变RC里的Pod副本数量，可以实现Pod的扩容或缩容功能;
\- 通过改变RC里Pod模板中的镜像版本，可以实现Pod的滚动升级功能;

![img](https://img2018.cnblogs.com/blog/907596/201903/907596-20190313223917071-1603229987.png)

**Service**：“微服务”，kubernetes中的核心。通过分析、识别并建模系统中的所有服务为微服务，最终系统有多个提供不同业务能力而又彼此独立的微服务单元所组成，服务之间通过TCP/IP进行通信。每个Pod都会被分配一个单独的IP地址，而且每个Pod都提供了一个独立的Endpoint以被客户端访问。

客户端如何访问？
部署负载均衡器，为Pod开启对外服务端口，将Pod的Endpoint列表加入转发列表中，客户端通过负载均衡器的对外IP+Port来访问此服务。每个Service都有一个全局唯一的虚拟ClusterIP，这样每个服务就变成了具备唯一IP地址的“通信节点”，服务调用就变成了最基础的TCP网络通信问题。

**Volume**：是Pod中能够被多个容器访问的共享目录。定义在Pod之上，被一个Pod里的多个容器挂载到具体的文件目录之下；Volume与Pod生命周期相同。Volume可以让一个Pod里的多个容器共享文件、让容器的数据写到宿主机的磁盘上或者写文件到 网络存储中，具体如下图所示：
![img](https://img2018.cnblogs.com/blog/907596/201903/907596-20190313224329386-903560638.png)

在kubernetes1.2的时候，RC就由Replication Controller升级成Replica Set，“下一代RC”。命令兼容适用，Replica Set主要被Deployment这个更高层的资源对象所使用，从而形成一套Pod创建、删除、更新的编排机制。当我们使用Deployment时，无需关心它是如何创建和维护ReplicaSet的，这一切是自动发生的。

**Docker**: 既然k8s是基于容器的，那么就不得不提到docker。2013年初，docker横空出世，孕育着新思想的“容器”，Docker选择容器作为核心和基础，以容器为资源分割和调度的基本单位，封装整个软件运行时环境，为开发者和系统管理员设计，用于构建、发布和运行分布式应用的平台。是一个跨平台、可移植并且简单易用的容器解决方案。通过操作系统内核技术（namespaces、cgroups等）为容器提供资源隔离与安全保障。
![img](https://img2018.cnblogs.com/blog/907596/201903/907596-20190313224553325-108461685.png)

上图是一个image的简单使用。我们可以通过一个dockerfile来build自己的image。可以把image上传（push）到自己的私有镜像仓库，也可以从私有仓库pull到本地进行使用。可以单独使用命令行，直接run container，可以对container进行stop、start、restart操作。也可以对image进行save保存操作以及加载load操作，大家具体可以根据自己的使用，选择不同的操作即可。

Docker资源隔离技术
Docker选择容器作为核心和基础，以容器为资源分割和调度的基本单位，封装整个软件运行时环境，为开发者和系统管理员设计，用于构建、发布和运行分布式应用的平台。Docker是一个跨平台、可移植并且简单易用的容器解决方案, 通过操作系统内核技术（namespaces、cgroups等）为容器提供资源隔离与安全保障。

Docker监控
cAdvisor（Container Advisor）是Google开发的用于分析运行中容器的资源占用和性能指标的开源工具。cAdvisor是一个运行时的守护进程，负责收集、聚合、处理和输出运行中容器的信息。对于每个容器，cAdvisor都有资源隔离参数、资源使用历史情况以及完整的历史资源使用和网络统计信息的柱状图。cAdvisor不但可以为用户提供监控服务，还可以结合其他应用为用户提供良好的服务移植和定制。包括结合InfluxDB对数据进行存储，以及结合Grafana提供web控制台，自定义查询指标，并进行展示:

**当下配合Kubernetes集群比较成熟的监控方案是: Prometheus +Grafana**

**五、Kubernetes集群里容器之间的通讯方式**

Kubernetes集群里面容器是存在于pod里面的，所以容器之间通讯，一般分为三种类型：
-> **pod内部容器之间**
-> **pod与pod容器之间**
-> **pod访问service服务**

**1）pod内部容器之间**
这种情况下容器通讯比较简单，因为k8s pod内部容器是共享网络空间的，所以容器直接可以使用localhost访问其他容器。k8s在启动容器的时候会先启动一个pause容器，这个容器就是实现这个功能的。

**2）pod与pod容器之间**
这种类型又可以分为两种情况：
-> 两个pod在同一台主机上面
-> 两个pod分布在不同主机之上
第一种情况，就比较简单了，就是docker默认的docker网桥互连容器。
第二种情况需要更为复杂的网络模型了，k8s官方推荐的是使用flannel组建一个大二层扁平网络，pod的ip分配由flannel统一分配，通讯过程也是走flannel的网桥。比如:

```
# docker --daemon --bip=172.17.18.1/24``注意，这其中的``"--bip=172.17.18.1/24"``这个参数，它限制了所在节点容器获得的IP范围。
```

每个node上面都会创建一个flannel0虚拟网卡，用于跨node之间通讯。所以容器直接可以直接使用pod id进行通讯。跨节点通讯时，发送端数据会从docker0路由到flannel0虚拟网卡，接收端数据会从flannel0路由到docker0，这是因为flannel会添加一个路由。

```
发送端：``# route -n``172.17.0.0  0.0.0.0  255.255.0.0   U 0 0 0  flannel0``172.17.13.0  0.0.0.0  255.255.255.0  U 0 0 0  docker0` `接收端：``172.18.0.0  0.0.0.0  255.255.0.0   U 0 0 0  flannel0``172.17.12.0  0.0.0.0  255.255.255.0  U 0 0 0  docker0
```

例如现在有一个数据包要从IP为172.17.13.2的容器发到IP为172.17.12.2的容器。根据数据发送节点的路由表，它只与172.17.0.0/16匹配这条记录匹配，因此数据从docker0出来以后就被投递到了flannel0。同理在目标节点，由于投递的地址是一个容器，因此目的地址一定会落在docker0对于的172.17.12.0/24这个记录上，自然的被投递到了docker0网卡。

**flannel的原理: 是将网络包封装在udp里面，所以发送端和接收端需要装包和解包，对性能有一定的影响。**除了flannel，k8s也支持其他的网络模型，比较有名的还有calico。

**3）pod 访问service服务**
这里涉及到k8s里面一个重要的概念service。它是一个服务的抽象，通过label（**k8s会根据service和pod直接的关系创建endpoint**，可以通过“**kubectl get ep**”查看）关联到后端的pod容器。**Service分配的ip叫cluster ip是一个虚拟ip（相对固定，除非删除service）**，这个ip只能在k8s集群内部使用，如果service需要对外提供，只能使用Nodeport方式映射到主机上，使用主机的ip和端口对外提供服务。（另外还可以使用LoadBalance方式，但这种方式是在gce这样的云环境里面使用的 ）。

节点上面有个kube-proxy进程，这个进程从master apiserver获取信息，感知service和endpoint的创建，然后做下面两个事情：
-> 为每个service 在集群中每个节点上面创建一个随机端口，任何该端口上面的连接会代理到相应的pod
-> 集群中每个节点安装iptables规则，用于clusterip + port路由到上一步定义的随机端口上面，所以集群中每个node上面都有service的转发规则：

```
KUBE-PORTALS-CONTAINER 从容器中通过service cluster ip和端口访问service的请求``KUBE-PORTALS-HOST 从主机中通过service cluster ip和端口访问service的请求``KUBE-NODEPORT-CONTAINER 从容器中通过service nodeport端口访问service的请求``KUBE-NODEPORT-HOST 从主机中通过service nodeport端口访问service的请求。
```

比如下面是一个测试环境内容:

```
-A KUBE-NODEPORT-CONTAINER -p tcp -m comment --comment``"smart/ccdb:port1521"` `-m tcp --dport 50171 -j REDIRECT --to-ports 52244``-A KUBE-NODEPORT-HOST -p tcp -m comment --comment``"smart/ccdb:port1521"` `-m tcp --dport 50171 -j DNAT --to-destination 10.45.25.227:52244``-A KUBE-PORTALS-CONTAINER -d 10.254.120.169``/32` `-p tcp -m comment --comment``"smart/ccdb:port1521"` `-m tcp --dport 1521 -j REDIRECT --to-ports 52244``-A KUBE-PORTALS-HOST -d 10.254.120.169``/32` `-p tcp -m comment --comment``"smart/ccdb:port1521"` `-m tcp --dport 1521 -j DNAT --to-destination 10.45.25.227:5224452244
```

这些就是kube-proxy针对service “"smart/ccdb:port1521"” 在节点上面监听的端口。

**六、Kubernetes日常维护命令**

```
一. 查看集群信息``=============================================================================================================``[root@k8s-master01 ~]``# kubectl cluster-info``[root@k8s-master01 ~]``# kubectl cluster-info dump``  ` `二. 查看各组件状态``=============================================================================================================``[root@k8s-master01 ~]``# kubectl -s http://localhost:8080 get componentstatuses``NAME         STATUS  MESSAGE       ERROR``controller-manager  Healthy  ok       ``scheduler      Healthy  ok       ``etcd-0        Healthy  {``"health"``:``"true"``}``  ` `或者``[root@k8s-master01 ~]``# kubectl -s http://172.16.60.220:8080 get componentstatuses``NAME         STATUS  MESSAGE       ERROR``scheduler      Healthy  ok       ``controller-manager  Healthy  ok       ``etcd-0        Healthy  {``"health"``:``"true"``}``  ` `三. GET信息``=============================================================================================================``1) 查看节点 (k8s-master01 对应的是 172.16.60.220的主机名)``[root@k8s-master01 ~]``# kubectl get node                #将命令中的node变为nodes也是可以的``NAME     STATUS  AGE``k8s-node01  Ready   1d``k8s-node02  Ready   1d``  ` `[root@k8s-master01 ~]``# kubectl -s http://k8s-master01:8080 get node  #将命令中的node变为nodes也是可以的``NAME     STATUS  AGE``k8s-node01  Ready   1d``k8s-node02  Ready   1d``  ` `2) 查看pods清单（查看pod ip地址，下面命令加上``"-o wide"``）``[root@k8s-master01 ~]``# kubectl get pod              #将pod变为pods也可以。如果有namespace，需要跟上"-n namespace名字" 或 "--all-namespaces"      ``NAME           READY   STATUS  RESTARTS  AGE``nginx-controller-d97wj  1``/1`    `Running  0     1h``nginx-controller-lf11n  1``/1`    `Running  0     1h``tomcat-controller-35kzb  1``/1`    `Running  0     18m``tomcat-controller-lsph4  1``/1`    `Running  0     18m``  ` `[root@k8s-master01 ~]``# kubectl -s http://k8s-master01:8080 get pod     #将命令中的pod变为pods也是可以的``NAME           READY   STATUS  RESTARTS  AGE``nginx-controller-d97wj  1``/1`    `Running  0     1h``nginx-controller-lf11n  1``/1`    `Running  0     1h``tomcat-controller-35kzb  1``/1`    `Running  0     18m``tomcat-controller-lsph4  1``/1`    `Running  0     18m``  ` `3) 查看service清单``[root@k8s-master01 ~]``# kubectl get service                       #将命令中的service变为services也是可以的``NAME            CLUSTER-IP    EXTERNAL-IP  PORT(S)     AGE``kubernetes         172.16.0.1        443``/TCP`     `1d``nginx-service-clusterip  172.16.77.193      8001``/TCP`     `1h``nginx-service-nodeport   172.16.234.94      8000:32172``/TCP`  `59m``tomcat-service-clusterip  172.16.144.116      8801``/TCP`     `14m``tomcat-service-nodeport  172.16.183.234      8880:31960``/TCP`  `11m``  ` `[root@k8s-master01 ~]``# kubectl -s http://172.16.60.220:8080 get service        #将命令中的service变为services也是可以的``NAME            CLUSTER-IP    EXTERNAL-IP  PORT(S)     AGE``kubernetes         172.16.0.1        443``/TCP`     `1d``nginx-service-clusterip  172.16.77.193      8001``/TCP`     `1h``nginx-service-nodeport   172.16.234.94      8000:32172``/TCP`  `1h``tomcat-service-clusterip  172.16.144.116      8801``/TCP`     `17m``tomcat-service-nodeport  172.16.183.234      8880:31960``/TCP`  `14m``  ` `或者 (后面的``sed``表示 打印奇数行)``[root@k8s-master01 ~]``# kubectl get services -o json|grep '"name":'|sed -n '1~2p'``        ``"name"``:``"kubernetes"``,``        ``"name"``:``"nginx-service-clusterip"``,``        ``"name"``:``"nginx-service-nodeport"``,``        ``"name"``:``"tomcat-service-clusterip"``,``        ``"name"``:``"tomcat-service-nodeport"``,``  ` `4) 查看replicationControllers清单 (同理可以将命令中的replicationControllers变为replicationController也是可以的)``[root@k8s-master01 ~]``# kubectl get replicationControllers``NAME        DESIRED  CURRENT  READY   AGE``nginx-controller  2     2     2     2h``tomcat-controller  2     2     2     1h``  ` `[root@k8s-master01 ~]``# kubectl -s http://172.16.60.220:8080 get replicationControllers``NAME        DESIRED  CURRENT  READY   AGE``nginx-controller  2     2     2     2h``tomcat-controller  2     2     2     1h``  ` `5) 查看rc和namespace``[root@k8s-master01 ~]``# kubectl get rc,namespace``NAME          DESIRED  CURRENT  READY   AGE``rc``/nginx-controller`  `2     2     2     2h``rc``/tomcat-controller`  `2     2     2     1h``  ` `NAME       STATUS  AGE``ns``/default`    `Active  1d``ns``/kube-system`  `Active  1d``  ` `6) 查看pod和svc(和service一样)``[root@k8s-master01 ~]``# kubectl get pods,svc``NAME             READY   STATUS  RESTARTS  AGE``po``/nginx-controller-d97wj`  `1``/1`    `Running  0     2h``po``/nginx-controller-lf11n`  `1``/1`    `Running  0     2h``po``/tomcat-controller-35kzb`  `1``/1`    `Running  0     1h``po``/tomcat-controller-lsph4`  `1``/1`    `Running  0     1h``  ` `NAME              CLUSTER-IP    EXTERNAL-IP  PORT(S)     AGE``svc``/kubernetes`         `172.16.0.1        443``/TCP`     `1d``svc``/nginx-service-clusterip`  `172.16.77.193      8001``/TCP`     `2h``svc``/nginx-service-nodeport`   `172.16.234.94      8000:32172``/TCP`  `2h``svc``/tomcat-service-clusterip`  `172.16.144.116      8801``/TCP`     `1h``svc``/tomcat-service-nodeport`  `172.16.183.234      8880:31960``/TCP`  `1h``  ` `7) 以jison格式输出pod的详细信息.``[root@k8s-master01 ~]``# kubectl get pods``NAME           READY   STATUS  RESTARTS  AGE``nginx-controller-d97wj  1``/1`    `Running  0     2h``nginx-controller-lf11n  1``/1`    `Running  0     2h``tomcat-controller-35kzb  1``/1`    `Running  0     1h``tomcat-controller-lsph4  1``/1`    `Running  0     1h``  ` `注意下面命令中的pods的名称可以通过上面命令查看``[root@k8s-master01 ~]``# kubectl get po nginx-controller-d97wj -o json``{``  ``"apiVersion"``:``"v1"``,``  ``"kind"``:``"Pod"``,``  ``"metadata"``: {``    ``"annotations"``: {``...................``...................``    ``"hostIP"``:``"172.16.60.222"``,``    ``"phase"``:``"Running"``,``    ``"podIP"``:``"192.168.100.2"``,``    ``"startTime"``:``"2019-03-15T14:40:18Z"``  ``}``}``  ` `还可以输出其它格式和方法(kubectl get -h查看帮助)``[root@k8s-master01 ~]``# kubectl get -h``  ` `8) 查看指定pod跑在哪个node上``[root@k8s-master01 ~]``# kubectl get po nginx-controller-d97wj -o wide ``NAME           READY   STATUS  RESTARTS  AGE    IP       NODE``nginx-controller-d97wj  1``/1`    `Running  0     2h    192.168.100.2  k8s-node02``  ` `9) 获取指定json或ymal格式的KEY数据,custom-columns=XXXXX（自定义列名）:.status.hostIP（以“点开始”，然后写路径就可以）``注意: 下面命令中的nginx-controller-d97wj是pod单元名称 (kubectl get pods 可以查看pods)``[root@k8s-master01 ~]``# kubectl get po nginx-controller-d97wj -o custom-columns=HOST-IP:.status.hostIP,POD-IP:.status.podIP ``HOST-IP     POD-IP``172.16.60.222  192.168.100.2``  ` `10) describe方法``describe类似于get，同样用于获取resource的相关信息。不同的是，get获得的是更详细的resource个性的详细信息，describe获得的是resource集群相关的信息。``describe命令同get类似，但是describe不支持-o选项，对于同一类型resource，describe输出的信息格式，内容域相同。``  ` `需要注意: 如果发现是查询某个resource的信息，使用get命令能够获取更加详尽的信息。但是如果想要查询某个resource的状态，如某个pod并不是在running状态，``这时需要获取更详尽的状态信息时，就应该使用describe命令。``  ` `[root@k8s-master01 ~]``# kubectl describe po nginx-controller-d97wj``Name:      nginx-controller-d97wj``Namespace:   default``Node:      k8s-node02``/172``.16.60.222``Start Time:   Fri, 15 Mar 2019 22:40:18 +0800``Labels:     name=nginx``Status:     Running``IP:       192.168.100.2``Controllers:  ReplicationController``/nginx-controller``Containers:`` ``nginx:``  ``Container ID:        docker:``//8ae4502b4e62120322de98aa532e653d3d2e058ffbb0b842e0f265621bebbe61``  ``Image:           172.16.60.220:5000``/nginx``  ``Image ID:          docker-pullable:``//172``.16.60.220:5000``/nginx``@sha256:7734a210432278817f8097acf2f72d20e2ccc7402a0509810c44b3a8bfe0094a``  ``Port:            80``/TCP``  ``State:           Running``   ``Started:         Fri, 15 Mar 2019 22:40:19 +0800``  ``Ready:           True``  ``Restart Count:       0``  ``Volume Mounts:       ``  ``Environment Variables:   ``Conditions:`` ``Type     Status`` ``Initialized  True`` ``Ready     True`` ``PodScheduled True``No volumes.``QoS Class:   BestEffort``Tolerations:  ``No events.``  ` `11) create创建``kubectl命令用于根据文件或输入创建集群resource。如果已经定义了相应resource的yaml或son文件，直接kubectl create -f filename即可创建文件内定义的``resource。也可以直接只用子命令[namespace``/secret/configmap/serviceaccount``]等直接创建相应的resource。从追踪和维护的角度出发，建议使用json或``yaml的方式定义资源。``  ` `命令格式:``# kubectl create -f 文件名``  ` `12) replace更新替换资源``replace命令用于对已有资源进行更新、替换。如前面create中创建的nginx，当我们需要更新resource的一些属性的时候，如果修改副本数量，增加、修改label，``更改image版本，修改端口等。都可以直接修改原yaml文件，然后执行replace命令。``  ` `需要注意: 名字不能被更更新。另外，如果是更新label，原有标签的pod将会与更新label后的rc断开联系，有新label的rc将会创建指定副本数的新的pod，但是默认``并不会删除原来的pod。所以此时如果使用get po将会发现pod数翻倍，进一步check会发现原来的pod已经不会被新rc控制，此处只介绍命令不详谈此问题，好奇者可自行实验。``  ` `命令格式:``# kubectl replace -f nginx-rc.yaml``  ` `13) patch``如果一个容器已经在运行，这时需要对一些容器属性进行修改，又不想删除容器，或不方便通过replace的方式进行更新。kubernetes还提供了一种在容器运行时，直接``对容器进行修改的方式，就是patch命令。 如创建pod的label是app=nginx-2，如果在运行过程中，需要把其label改为app=nginx-3。``这个patch命令如下：``[root@k8s-master01 ~]``# kubectl patch pod nginx-controller-d97wj -p '{"metadata":{"labels":{"app":"nginx-3"}}}'``"nginx-controller-d97wj"` `patched``  ` `14) edit``edit提供了另一种更新resource源的操作，通过edit能够灵活的在一个common的resource基础上，发展出更过的significant resource。``例如，使用edit直接更新前面创建的pod的命令为：``# kubectl edit po nginx-controller-d97wj``  ` `上面命令的效果等效于：``# kubectl get po nginx-controller-d97wj -o yaml >> /tmp/nginx-tmp.yaml``# vim /tmp/nginx-tmp.yaml       // 这此文件里做一些修改``# kubectl replace -f /tmp/nginx-tmp.yaml``  ` `15) Delete``根据resource名或label删除resource。``# kubectl delete -f nginx-rc.yaml``# kubectl delete po nginx-controller-d97wj``# kubectl delete po nginx-controller-lf11n``  ` `16) apply``apply命令提供了比patch，edit等更严格的更新resource的方式。通过apply，用户可以将resource的configuration使用``source` `control的方式维护在版本库中。``每次有更新时，将配置文件push到server，然后使用kubectl apply将更新应用到resource。kubernetes会在引用更新前将当前配置文件中的配置同已经应用的配置``做比较，并只更新更改的部分，而不会主动更改任何用户未指定的部分。``  ` `apply命令的使用方式同replace相同，不同的是，apply不会删除原有resource，然后创建新的。apply直接在原有resource的基础上进行更新。同时kubectl apply``还会resource中添加一条注释，标记当前的apply。类似于git操作。``  ` `17) logs``logs命令用于显示pod运行中，容器内程序输出到标准输出的内容。跟docker的logs命令类似。如果要获得``tail` `-f 的方式，也可以使用-f选项。``# kubectl logs nginx-controller-d97wj``  ` `18) rolling-update``rolling-update是一个非常重要的命令，对于已经部署并且正在运行的业务，rolling-update提供了不中断业务的更新方式。rolling-update每次起一个新的pod，``等新pod完全起来后删除一个旧的pod，然后再起一个新的pod替换旧的pod，直到替换掉所有的pod。``  ` `rolling-update需要确保新的版本有不同的name，Version和label，否则会报错 。``# kubectl rolling-update nginx-controller -f nginx-rc.yaml``  ` `如果在升级过程中，发现有问题还可以中途停止update，并回滚到前面版本``# kubectl rolling-update nginx-controller --rollback``  ` `rolling-update还有很多其他选项提供丰富的功能，如--update-period指定间隔周期，使用时可以使用-h查看help信息.``  ` `19) scale (注意下面的nginx-controller 是在nginx-rc.yaml文件中定义的name名称)``scale用于程序在负载加重或缩小时副本进行扩容或缩小，如前面创建的nginx有两个副本，可以轻松的使用scale命令对副本数进行扩展或缩小。``扩展副本数到4：``# kubectl scale rc nginx-controller --replicas=4``  ` `重新缩减副本数到2：``# kubectl scale rc nginx-controller --replicas=2``  ` `20) autoscale``scale虽然能够很方便的对副本数进行扩展或缩小，但是仍然需要人工介入，不能实时自动的根据系统负载对副本数进行扩、缩。autoscale命令提供了自动根据pod负载``对其副本进行扩缩的功能。``  ` `autoscale命令会给一个rc指定一个副本数的范围，在实际运行中根据pod中运行的程序的负载自动在指定的范围内对pod进行扩容或缩容。如前面创建的nginx，可以用``如下命令指定副本范围在1~4``# kubectl autoscale rc nginx-controller --min=1 --max=4``  ` `21) attach``attach命令类似于docker的attach命令，可以直接查看容器中以daemon形式运行的进程的输出，效果类似于logs -f，退出查看使用ctrl-c。如果一个pod中有多个容器，``要查看具体的某个容器的的输出，需要在pod名后使用-c containers name指定运行的容器。如下示例的命令为查看kube-system namespace中的kube-dns-v9-rcfuk pod``中的skydns容器的输出。``# kubectl attach kube-dns-v9-rcfuk -c skydns --namespace=kube-system``  ` `22)``exec``exec``命令同样类似于docker的``exec``命令，为在一个已经运行的容器中执行一条shell命令，如果一个pod容器中，有多个容器，需要使用-c选项指定容器。``  ` `23) run``类似于docker的run命令，直接运行一个image。``  ` `24) cordon, drain, uncordon``这三个命令是正式release的1.2新加入的命令，三个命令一起介绍，是因为三个命令配合使用可以实现节点的维护。在1.2之前，因为没有相应的命令支持，如果要维护一个``节点，只能stop该节点上的kubelet将该节点退出集群，是集群不在将新的pod调度到该节点上。如果该节点上本生就没有pod在运行，则不会对业务有任何影响。如果该节``点上有pod正在运行，kubelet停止后，master会发现该节点不可达，而将该节点标记为notReady状态，不会将新的节点调度到该节点上。同时，会在其他节点上创建新的``pod替换该节点上的pod。这种方式虽然能够保证集群的健壮性，但是任然有些暴力，如果业务只有一个副本，而且该副本正好运行在被维护节点上的话，可能仍然会造成业``务的短暂中断。``  ` `1.2中新加入的这3个命令可以保证维护节点时，平滑的将被维护节点上的业务迁移到其他节点上，保证业务不受影响。如下图所示是一个整个的节点维护的流程（为了方便``demo增加了一些查看节点信息的操作）：``1- 首先查看当前集群所有节点状态，可以看到共四个节点都处于ready状态；``2- 查看当前nginx两个副本分别运行在d-node1和k-node2两个节点上；``3- 使用cordon命令将d-node1标记为不可调度；``4- 再使用kubectl get nodes查看节点状态，发现d-node1虽然还处于Ready状态，但是同时还被禁能了调度，这意味着新的pod将不会被调度到d-node1上。``5- 再查看nginx状态，没有任何变化，两个副本仍运行在d-node1和k-node2上；``6- 执行drain命令，将运行在d-node1上运行的pod平滑的赶到其他节点上；``7- 再查看nginx的状态发现，d-node1上的副本已经被迁移到k-node1上；这时候就可以对d-node1进行一些节点维护的操作，如升级内核，升级Docker等；``8- 节点维护完后，使用uncordon命令解锁d-node1，使其重新变得可调度；8）检查节点状态，发现d-node1重新变回Ready状态``  ` `# kubectl get nodes``# kubectl get po -o wide``# kubectl cordon d-node1``# kubectl get nodes``# kubectl get po -o wide``# kubectl drain d-node1``# kubectl get po -o wide``# kubectl uncordon``# kubectl uncordon d-node1``# kubectl get nodes``  ` `25) 查看某个pod重启次数(这个是参考)``# kubectl get pod nginx-controller-d97wj --template="{{range .status.containerStatuses}}{{.name}}:{{.restartCount}}{{end}}"``  ` `26) 查看pod生命周期``[root@k8s-master01 ~]``# kubectl get pod nginx-controller-d97wj --template="{{.status.phase}}"``Running`` ` `四、日常维护命令``=============================================================================================================``kubectl get pods``kubectl get rc``kubectl get service``kubectl get componentstatuses``kubectl get endpoints``kubectl cluster-info``kubectl create -f redis-master-controller.yaml``kubectl delete -f redis-master-controller.yaml``kubectl delete pod nginx-772ai``kubectl logs -f pods``/heapster-xxxxx` `-n kube-system          ``#查看日志``kubectl scale rc redis-slave --replicas=3               ``#修改RC的副本数量，来实现Pod的动态缩放``etcdctl cluster-health                        ``#检查网络集群健康状态``etcdctl --endpoints=http:``//172``.16.60.220:2379 cluster-health     ``#带有安全认证检查网络集群健康状态``etcdctl member list``etcdctl``set` `/k8s/network/config` `'{ "Network": "10.1.0.0/16" }'``etcdctl get``/k8s/network/config`` ` ` ` `五、基础进阶``=============================================================================================================``kubectl get services kubernetes-dashboard -n kube-system     ``#查看所有service``kubectl get deployment kubernetes-dashboard -n kube-system    ``#查看所有发布``kubectl get pods --all-namespaces                 ``#查看所有pod``kubectl get pods -o wide --all-namespaces             ``#查看所有pod的IP及节点``kubectl get pods -n kube-system |``grep` `dashboard``kubectl describe service``/kubernetes-dashboard` `--namespace=``"kube-system"``kubectl describe pods``/kubernetes-dashboard-349859023-g6q8c` `--namespace=``"kube-system"`    `#指定类型查看``kubectl describe pod nginx-772ai                 ``#查看pod详细信息``kubectl scale rc nginx --replicas=5                ``#动态伸缩``kubectl scale deployment redis-slave --replicas=5         ``#动态伸缩``kubectl scale --replicas=2 -f redis-slave-deployment.yaml     ``#动态伸缩``kubectl``exec` `-it tomcat-controller-35kzb``/bin/bash`         `#进入容器``kubectl label nodes k8s-node01 zone=north        ``#增加节点lable值 spec.nodeSelector: zone: north, 指定pod在哪个节点``kubectl get nodes -lzone                ``#获取zone的节点``kubectl label pod tomcat-controller-35kzb role=master  ``#增加lable值 [key]=[value]``kubectl label pod tomcat-controller-35kzb role-           ``#删除lable值``kubectl label pod tomcat-controller-35kzb role=backend --overwrite  ``#修改lable值``kubectl rolling-update redis-master -f redis-master-controller-v2.yaml   ``#配置文件滚动升级``kubectl rolling-update redis-master --image=redis-master:2.0        ``#命令升级``kubectl rolling-update redis-master --image=redis-master:1.0 --rollback  ``#pod版本回滚`` ` `六、yaml使用及命令``=============================================================================================================``kubectl create -f nginx-deployment.yaml ``#创建deployment资源``kubectl get deploy   ``#查看deployment``kubectl get rs     ``#查看ReplicaSet``kubectl get pods --show-labels ``#查看pods所有标签。可以添加"-all-namespaces" 或者 "-n kube-system"表示查看所有命名空间或某一命名空间里pods的标签``kubectl get pods -l app=nginx  ``#根据标签查看pods`` ` `kubectl``set` `image deployment``/nginx-deployment` `nginx=nginx:1.11  ``#滚动更新镜像``或者``kubectl edit deployment``/nginx-deployment``或者``kubectl apply -f nginx-deployment.yaml              ``#也表示对yaml修改后进行更新操作，更新到kubernetes集群配置中`` ` `kubectl rollout status deployment``/nginx-deployment`         `#实时观察发布状态：`` ` `kubectl rollout``history` `deployment``/nginx-deployment`        `#查看deployment历史修订版本``kubectl rollout``history` `deployment``/nginx-deployment` `--revision=3`` ` `kubectl rollout undo deployment``/nginx-deployment`          `#回滚到以前版本``kubectl rollout undo deployment``/nginx-deployment` `--to-revision=3`` ` `kubectl scale deployment nginx-deployment --replicas=10      ``#扩容deployment的Pod副本数量`` ` `kubectl autoscale deployment nginx-deployment --min=10 --max=15 --cpu-percent=80  ``#设置启动扩容/缩容`` ` `七、命名空间``=============================================================================================================``kubectl get namespace              ``#获取k8s的命名空间``kubectl get pod --namespace =[命令空间名称]    ``#获取对应命名空间内的pod，"--namespace"可以写成"-c"``kubectl --namespace [命令空间名称] logs [pod名称] -c 容器名称  ``#获取对应namespace中对应pod的日志，如果不加"-c 容器名称",则默认查看的是该pod下第一个容器的日志`` ` `pod维护示例：``查看某个命令空间下的pod``# kubectl get pods -n namespace `` ` `在没有pod 的yaml文件时，强制重启某个pod``# kubectl get pod podname -n namespace -o yaml | kubectl replace --force -f -`` ` `查看某个pod重启次数(这个是参考)``# kubectl get pod podname -n namespace --template="{{range .status.containerStatuses}}{{.name}}:{{.restartCount}}{{end}}"`` ` `查看pod生命周期``# kubectl get pod podname --template="{{.status.phase}}"`` ` `查看kube-space命令空间下的pod``[root@m7-autocv-gpu01 ~]``# kubectl get pods -n kube-system -o wide|grep -E 'elasticsearch|fluentd|kibana'``elasticsearch-logging-0         1``/1`   `Running  0     5h9m  172.30.104.6  m7-autocv-gpu03  ``elasticsearch-logging-1         1``/1`   `Running  0     4h59m  172.30.232.8  m7-autocv-gpu02  ``fluentd-es-v2.2.0-mkkcf         1``/1`   `Running  0     5h9m  172.30.104.7  m7-autocv-gpu03  ``kibana-logging-f6fc77549-nlxfg      1``/1`   `Running  0     42s   172.30.96.7  m7-autocv-gpu01  `` ` `[root@m7-autocv-gpu01 ~]``# kubectl get pod kibana-logging-f6fc77549-nlxfg -n kube-system -o yaml | kubectl replace --force -f -``pod``"kibana-logging-f6fc77549-d47nc"` `deleted``pod``/kibana-logging-f6fc77549-d47nc` `replaced`` ` `[root@m7-autocv-gpu01 ~]``# kubectl get pod kibana-logging-f6fc77549-nlxfg -n kube-system --template="{{range .status.containerStatuses}}{{.name}}:{{.restartCount}}{{end}}"``kibana-logging:0`` ` `[root@m7-autocv-gpu01 ~]``# kubectl get pod kibana-logging-f6fc77549-nlxfg -n kube-system --template="{{.status.phase}}"``Running` `八、进入pod内的容器``=============================================================================================================``kubernetes中登录pod中的容器，如下，kevintest-f857f78ff-dlp24是pod名称，webha是命名空间``# kubectl -n webha exec -it kevintest-f857f78ff-dlp24 -- bash    #登录后终端信息中显示主机名``# kubectl -n webha exec -it kevintest-f857f78ff-dlp24 sh      #登录后终端信息中不显示主机名` `如果pod中有多个容器，则默认登录到第一个容器中。``也可以通过-c参数制定登录到哪个容器中, 比如进入kevintest-f857f78ff-dlp24的nginx_bo容器``# kubectl -n webha exec -it kevintest-f857f78ff-dlp24 -c nginx_bo -- bash
```

**七、Kubernetes集群部署失败的一般原因**

**1. 错误的容器镜像/非法的仓库权限**
其中两个最普遍的问题是：a) 指定了错误的容器镜像；b) 使用私有镜像却不提供仓库认证信息。这在首次使用 Kubernetes 或者绑定 CI/CD 环境时尤其棘手。看个例子:

```
首先我们创建一个名为 fail 的 deployment，它指向一个不存在的 Docker 镜像：``$ kubectl run fail --image=rosskukulinski``/dne``:v1.0.0` `然后我们查看 Pods，可以看到有一个状态为 ErrImagePull 或者 ImagePullBackOff 的 Pod：``$ kubectl get pods``NAME          READY   STATUS       RESTARTS  AGE``fail-1036623984-hxoas  0``/1`    `ImagePullBackOff  0     2m` `想查看更多信息，可以 describe 这个失败的 Pod：``$ kubectl describe pod fail-1036623984-hxoas` `查看 describe 命令的输出中 Events 这部分，我们可以看到如下内容：``Events:``FirstSeen  LastSeen  Count  From            SubObjectPath    Type    Reason   Message``---------  --------  -----  ----            -------------    --------  ------   -------``5m    5m   1  {default-scheduler }              Normal   Scheduled  Successfully assigned fail-1036623984-hxoas to gke-nrhk-1-default-pool-a101b974-wfp7``5m    2m   5  {kubelet gke-nrhk-1-default-pool-a101b974-wfp7} spec.containers{fail}  Normal   Pulling   pulling image``"rosskukulinski/dne:v1.0.0"``5m    2m   5  {kubelet gke-nrhk-1-default-pool-a101b974-wfp7} spec.containers{fail}  Warning   Failed   Failed to pull image``"rosskukulinski/dne:v1.0.0"``: Error: image rosskukulinski``/dne` `not found``5m    2m   5  {kubelet gke-nrhk-1-default-pool-a101b974-wfp7}       Warning   FailedSync Error syncing pod, skipping: failed to``"StartContainer"` `for` `"fail"` `with ErrImagePull:``"Error: image rosskukulinski/dne not found"` `5m  11s 19 {kubelet gke-nrhk-1-default-pool-a101b974-wfp7} spec.containers{fail}  Normal BackOff   Back-off pulling image``"rosskukulinski/dne:v1.0.0"``5m  11s 19 {kubelet gke-nrhk-1-default-pool-a101b974-wfp7}       Warning FailedSync Error syncing pod, skipping: failed to``"StartContainer"` `for` `"fail"` `with ImagePullBackOff:``"Back-off pulling image \"rosskukulinski/dne:v1.0.0\""` `显示错误的那句话：Failed to pull image``"rosskukulinski/dne:v1.0.0"``: Error: image rosskukulinski``/dne` `not found 告诉我们 Kubernetes无法找到镜像 rosskukulinski``/dne``:v1.0.0。` `因此问题变成：为什么 Kubernetes 拉不下来镜像？` `除了网络连接问题外，还有三个主要元凶：``- 镜像 tag 不正确``- 镜像不存在（或者是在另一个仓库）``- Kubernetes 没有权限去拉那个镜像` `如果你没有注意到你的镜像 tag 的拼写错误，那么最好就用你本地机器测试一下。` `通常我会在本地开发机上，用 docker pull 命令，带上 完全相同的镜像 tag，来跑一下。比如上面的情况，我会运行命令 docker pull rosskukulinski``/dne``:v1.0.0。``如果这成功了，那么很可能 Kubernetes 没有权限去拉取这个镜像。参考镜像拉取 Secrets 来解决这个问题。``如果失败了，那么我会继续用不显式带 tag 的镜像测试 - docker pull rosskukulinski``/dne` `- 这会尝试拉取 tag 为 latest 的镜像。如果这样成功，表明原来指定的 tag 不存在。这可能是人为原因，拼写错误，或者 CI``/CD` `的配置错误。` `如果 docker pull rosskukulinski``/dne``（不指定 tag）也失败了，那么我们碰到了一个更大的问题：我们所有的镜像仓库中都没有这个镜像。默认情况下，Kubernetes 使用 Dockerhub 镜像仓库，如果你在使用 Quay.io，AWS ECR，或者 Google Container Registry，你要在镜像地址中指定这个仓库的 URL，比如使用 Quay，镜像地址就变成 quay.io``/rosskukulinski/dne``:v1.0.0。` `如果你在使用 Dockerhub，那你应该再次确认你发布镜像到 Dockerhub 的系统，确保名字和 tag 匹配你的 deployment 正在使用的镜像。` `注意：观察 Pod 状态的时候，镜像缺失和仓库权限不正确是没法区分的。其它情况下，Kubernetes 将报告一个 ErrImagePull 状态。
```

**2. 应用启动之后又挂掉**
无论你是在 Kubernetes 上启动新应用，还是迁移应用到已存在的平台，应用在启动之后就挂掉都是一个比较常见的现象。看个例子:

```
我们创建一个 deployment，它的应用会在1秒后挂掉：``$ kubectl run crasher --image=rosskukulinski``/crashing-app` `我们看一下 Pods 的状态：``$ kubectl get pods``NAME            READY   STATUS       RESTARTS  AGE``crasher-2443551393-vuehs  0``/1`    `CrashLoopBackOff  2     54s` `CrashLoopBackOff 告诉我们，Kubernetes 正在尽力启动这个 Pod，但是一个或多个容器已经挂了，或者正被删除。` `让我们 describe 这个 Pod 去获取更多信息：``$ kubectl describe pod crasher-2443551393-vuehs``Name:    crasher-2443551393-vuehs``Namespace:  fail``Node:    gke-nrhk-1-default-pool-a101b974-wfp7``/10``.142.0.2``Start Time:  Fri, 10 Feb 2017 14:20:29 -0500``Labels:    pod-template-``hash``=2443551393``  ``run=crasher``Status:    Running``IP:    10.0.0.74``Controllers:  ReplicaSet``/crasher-2443551393``Containers:``crasher:``Container ID:  docker:``//51c940ab32016e6d6b5ed28075357661fef3282cb3569117b0f815a199d01c60``Image:    rosskukulinski``/crashing-app``Image ID:    docker:``//sha256``:cf7452191b34d7797a07403d47a1ccf5254741d4bb356577b8a5de40864653a5``Port:    ``State:    Terminated`` ``Reason:    Error`` ``Exit Code:  1`` ``Started:    Fri, 10 Feb 2017 14:22:24 -0500`` ``Finished:    Fri, 10 Feb 2017 14:22:26 -0500``Last State:    Terminated`` ``Reason:    Error`` ``Exit Code:  1`` ``Started:    Fri, 10 Feb 2017 14:21:39 -0500`` ``Finished:    Fri, 10 Feb 2017 14:21:40 -0500``Ready:    False``Restart Count:  4``...` `好可怕，Kubernetes 告诉我们这个 Pod 正被 Terminated，因为容器里的应用挂了。我们还可以看到应用的 Exit Code 是 1。后面我们可能还会看到一个 OOMKilled 错误。` `我们的应用正在挂掉？为什么？` `首先我们查看应用日志。假定你发送应用日志到 stdout（事实上你也应该这么做），你可以使用 kubectl logs 看到应用日志:``$ kubectl logs crasher-2443551393-vuehs` `不幸的是，这个 Pod 没有任何日志。这可能是因为我们正在查看一个新起的应用实例，因此我们应该查看前一个容器：``$ kubectl logs crasher-2443551393-vuehs --previous` `什么！我们的应用仍然不给我们任何东西。这个时候我们应该给应用加点启动日志了，以帮助我们定位这个问题。我们也可以本地运行一下这个容器，以确定是否缺失环境变量或者挂载卷。
```

**3. 缺失 ConfigMap 或者 Secret**
Kubernetes 最佳实践建议通过 ConfigMaps 或者 Secrets 传递应用的运行时配置。这些数据可以包含数据库认证信息，API endpoints，或者其它配置信息。一个常见的错误是，创建的 deployment 中引用的 ConfigMaps 或者 Secrets 的属性不存在，有时候甚至引用的 ConfigMaps 或者 Secrets 本身就不存在。

**缺失 ConfigMap**
第一个例子，我们将尝试创建一个 Pod，它加载 ConfigMap 数据作为环境变量：

```
# configmap-pod.yaml``apiVersion: v1``kind: Pod``metadata:``name: configmap-pod``spec:``containers:``- name:``test``-container`` ``image: gcr.io``/google_containers/busybox`` ``command``: [``"/bin/sh"``,``"-c"``,``"env"` `]`` ``env``:``  ``- name: SPECIAL_LEVEL_KEY``   ``valueFrom:``    ``configMapKeyRef:``     ``name: special-config``     ``key: special.how` `让我们创建一个 Pod：kubectl create -f configmap-pod.yaml。在等待几分钟之后，我们可以查看我们的 Pod：``$ kubectl get pods``NAME      READY   STATUS       RESTARTS  AGE``configmap-pod  0``/1`    `RunContainerError  0     3s` `Pod 状态是 RunContainerError 。我们可以使用 kubectl describe 了解更多：``$ kubectl describe pod configmap-pod``[...]``Events:``FirstSeen  LastSeen  Count  From            SubObjectPath      Type    Reason   Message``---------  --------  -----  ----            -------------      --------  ------   -------``20s    20s   1  {default-scheduler }                Normal   Scheduled  Successfully assigned configmap-pod to gke-ctm-1-sysdig2-35e99c16-tgfm``19s    2s   3  {kubelet gke-ctm-1-sysdig2-35e99c16-tgfm}  spec.containers{``test``-container} Normal   Pulling   pulling image``"gcr.io/google_containers/busybox"``18s    2s   3  {kubelet gke-ctm-1-sysdig2-35e99c16-tgfm}  spec.containers{``test``-container} Normal   Pulled   Successfully pulled image``"gcr.io/google_containers/busybox"``18s    2s   3  {kubelet gke-ctm-1-sysdig2-35e99c16-tgfm}          Warning   FailedSync Error syncing pod, skipping: failed to``"StartContainer"` `for` `"test-container"` `with RunContainerError:``"GenerateRunContainerOptions: configmaps \"special-config\" not found"` `Events 章节的最后一条告诉我们什么地方错了。Pod 尝试访问名为 special-config 的 ConfigMap，但是在该 namespace 下找不到。一旦我们创建这个 ConfigMap，Pod 应该重启并能成功拉取运行时数据。` `在 Pod 规格说明中访问 Secrets 作为环境变量会产生相似的错误，就像我们在这里看到的 ConfigMap错误一样。
```

但是假如你通过 Volume 来访问 Secrets 或者 ConfigMap会发生什么呢？

**缺失 Secrets**
下面是一个pod规格说明，它引用了名为 myothersecret 的 Secrets，并尝试把它挂为卷:

```
# missing-secret.yaml``apiVersion: v1``kind: Pod``metadata:``name: secret-pod``spec:``containers:``- name:``test``-container`` ``image: gcr.io``/google_containers/busybox`` ``command``: [``"/bin/sh"``,``"-c"``,``"env"` `]`` ``volumeMounts:``  ``- mountPath:``/etc/secret/``   ``name: myothersecret``restartPolicy: Never``volumes:``- name: myothersecret`` ``secret:``  ``secretName: myothersecret` `让我们用 kubectl create -f missing-secret.yaml 来创建一个 Pod。` `几分钟后，我们 get Pods，可以看到 Pod 仍处于 ContainerCreating 状态：``$ kubectl get pods``NAME      READY   STATUS       RESTARTS  AGE``secret-pod  0``/1`    `ContainerCreating  0     4h` `这就奇怪了。我们 describe 一下，看看到底发生了什么：``$ kubectl describe pod secret-pod``Name:    secret-pod``Namespace:  fail``Node:    gke-ctm-1-sysdig2-35e99c16-tgfm``/10``.128.0.2``Start Time:  Sat, 11 Feb 2017 14:07:13 -0500``Labels:    ``Status:    Pending``IP:    ``Controllers:  ` `[...]` `Events:``FirstSeen  LastSeen  Count  From            SubObjectPath  Type    Reason   Message``---------  --------  -----  ----            -------------  --------  ------   -------``18s    18s   1  {default-scheduler }            Normal   Scheduled  Successfully assigned secret-pod to gke-ctm-1-sysdig2-35e99c16-tgfm``18s    2s   6  {kubelet gke-ctm-1-sysdig2-35e99c16-tgfm}      Warning   FailedMount MountVolume.SetUp failed``for` `volume``"kubernetes.io/secret/337281e7-f065-11e6-bd01-42010af0012c-myothersecret"` `(spec.Name:``"myothersecret"``) pod``"337281e7-f065-11e6-bd01-42010af0012c"` `(UID:``"337281e7-f065-11e6-bd01-42010af0012c"``) with: secrets``"myothersecret"` `not found` `Events 章节再次解释了问题的原因。它告诉我们 Kubelet 无法从名为 myothersecret 的 Secret 挂卷。为了解决这个问题，我们可以创建 myothersecret ，它包含必要的安全认证信息。一旦 myothersecret 创建完成，容器也将正确启动。
```

**4. 活跃度/就绪状态探测失败**
在 Kubernetes 中处理容器问题时，需要注意的是：你的容器应用是 running 状态，不代表它在工作！？

Kubernetes 提供了两个基本特性，称作**活跃度探测**和**就绪状态探测**。本质上来说，活跃度/就绪状态探测将定期地执行一个操作（例如发送一个 HTTP 请求，打开一个 tcp 连接，或者在你的容器内运行一个命令），以确认你的应用和你预想的一样在工作。

如果活跃度探测失败，Kubernetes 将杀掉你的容器并重新创建一个。如果就绪状态探测失败，这个 Pod 将不会作为一个服务的后端 endpoint，也就是说不会流量导到这个 Pod，直到它变成 Ready。

如果你试图部署变更你的活跃度/就绪状态探测失败的应用，滚动部署将一直悬挂，因为它将等待你的所有 Pod 都变成 Ready。

这个实际是怎样的情况？以下是一个 Pod 规格说明，它定义了活跃度/就绪状态探测方法，都是基于8080端口对 /healthy 路由进行健康检查：

```
apiVersion: v1``kind: Pod``metadata:``name: liveness-pod``spec:``containers:``- name:``test``-container`` ``image: rosskukulinski``/leaking-app`` ``livenessProbe:``  ``httpGet:``   ``path:``/healthz``   ``port: 8080``  ``initialDelaySeconds: 3``  ``periodSeconds: 3`` ``readinessProbe:``  ``httpGet:``   ``path:``/healthz``   ``port: 8080``  ``initialDelaySeconds: 3``  ``periodSeconds: 3` `让我们创建这个 Pod：kubectl create -f liveness.yaml，过几分钟后查看发生了什么：``$ kubectl get pods``NAME      READY   STATUS  RESTARTS  AGE``liveness-pod  0``/1`    `Running  4     2m` `2分钟以后，我们发现 Pod 仍然没处于 Ready 状态，并且它已被重启了4次。让我们 describe 一下查看更多信息：``$ kubectl describe pod liveness-pod``Name:    liveness-pod``Namespace:  fail``Node:    gke-ctm-1-sysdig2-35e99c16-tgfm``/10``.128.0.2``Start Time:  Sat, 11 Feb 2017 14:32:36 -0500``Labels:    ``Status:    Running``IP:    10.108.88.40``Controllers:  ``Containers:``test``-container:``Container ID:  docker:``//8fa6f99e6fda6e56221683249bae322ed864d686965dc44acffda6f7cf186c7b``Image:    rosskukulinski``/leaking-app``Image ID:    docker:``//sha256``:7bba8c34dad4ea155420f856cd8de37ba9026048bd81f3a25d222fd1d53da8b7``Port:    ``State:    Running`` ``Started:    Sat, 11 Feb 2017 14:40:34 -0500``Last State:    Terminated`` ``Reason:    Error`` ``Exit Code:  137`` ``Started:    Sat, 11 Feb 2017 14:37:10 -0500`` ``Finished:    Sat, 11 Feb 2017 14:37:45 -0500``[...]``Events:``FirstSeen  LastSeen  Count  From            SubObjectPath      Type    Reason   Message``---------  --------  -----  ----            -------------      --------  ------   -------``8m    8m   1  {default-scheduler }                Normal   Scheduled  Successfully assigned liveness-pod to gke-ctm-1-sysdig2-35e99c16-tgfm``8m    8m   1  {kubelet gke-ctm-1-sysdig2-35e99c16-tgfm}  spec.containers{``test``-container} Normal   Created   Created container with docker``id` `0fb5f1a56ea0; Security:[seccomp=unconfined]``8m    8m   1  {kubelet gke-ctm-1-sysdig2-35e99c16-tgfm}  spec.containers{``test``-container} Normal   Started   Started container with docker``id` `0fb5f1a56ea0``7m    7m   1  {kubelet gke-ctm-1-sysdig2-35e99c16-tgfm}  spec.containers{``test``-container} Normal   Created   Created container with docker``id` `3f2392e9ead9; Security:[seccomp=unconfined]``7m    7m   1  {kubelet gke-ctm-1-sysdig2-35e99c16-tgfm}  spec.containers{``test``-container} Normal   Killing   Killing container with docker``id` `0fb5f1a56ea0: pod``"liveness-pod_fail(d75469d8-f090-11e6-bd01-42010af0012c)"` `container``"test-container"` `is unhealthy, it will be killed and re-created.``8m  16s 10 {kubelet gke-ctm-1-sysdig2-35e99c16-tgfm}  spec.containers{``test``-container} Warning Unhealthy  Liveness probe failed: Get http:``//10``.108.88.40:8080``/healthz``: dial tcp 10.108.88.40:8080: getsockopt: connection refused``8m  1s 85 {kubelet gke-ctm-1-sysdig2-35e99c16-tgfm}  spec.containers{``test``-container} Warning Unhealthy  Readiness probe failed: Get http:``//10``.108.88.40:8080``/healthz``: dial tcp 10.108.88.40:8080: getsockopt: connection refused` `Events 章节再次救了我们。我们可以看到活跃度探测和就绪状态探测都失败了。关键的一句话是 container``"test-container"` `is unhealthy, it will be killed and re-created。这告诉我们 Kubernetes 正在杀这个容器，因为容器的活跃度探测失败了。` `这里有三种可能性：``- 你的探测不正确，健康检查的 URL 是否改变了？``- 你的探测太敏感了， 你的应用是否要过一会才能启动或者响应？``- 你的应用永远不会对探测做出正确响应，你的数据库是否配置错了` `查看 Pod 日志是一个开始调测的好地方。一旦你解决了这个问题，新的 deployment 应该就能成功了。
```

**5. 超出CPU/内存的限制**
Kubernetes 赋予集群管理员限制 Pod 和容器的 CPU 或内存数量的能力。作为应用开发者，你可能不清楚这个限制，导致 deployment 失败的时候一脸困惑。我们试图部署一个未知 CPU/memory 请求限额的 deployment：

```
# gateway.yaml``apiVersion: extensions``/v1beta1``kind: Deployment``metadata:``name: gateway``spec:``template:``metadata:`` ``labels:``  ``app: gateway``spec:`` ``containers:``  ``- name:``test``-container``   ``image: nginx``   ``resources:``    ``requests:``     ``memory: 5Gi` `你会看到我们设了 5Gi 的资源请求。让我们创建这个 deployment：kubectl create -f gateway.yaml。` `现在我们可以看到我们的 Pod：``$ kubectl get pods``No resources found.` `为啥，让我们用 describe 来观察一下我们的 deployment：``$ kubectl describe deployment``/gateway``Name:      gateway``Namespace:    fail``CreationTimestamp:  Sat, 11 Feb 2017 15:03:34 -0500``Labels:      app=gateway``Selector:    app=gateway``Replicas:    0 updated | 1 total | 0 available | 1 unavailable``StrategyType:    RollingUpdate``MinReadySeconds:  0``RollingUpdateStrategy:  0 max unavailable, 1 max surge``OldReplicaSets:    ``NewReplicaSet:    gateway-764140025 (0``/1` `replicas created)``Events:``FirstSeen  LastSeen  Count  From        SubObjectPath  Type    Reason     Message``---------  --------  -----  ----        -------------  --------  ------     -------``4m    4m   1  {deployment-controller }      Normal   ScalingReplicaSet  Scaled up replica``set` `gateway-764140025 to 1` `基于最后一行，我们的 deployment 创建了一个 ReplicaSet（gateway-764140025） 并把它扩展到 1。这个是用来管理 Pod 生命周期的实体。我们可以 describe 这个 ReplicaSet：``$ kubectl describe rs``/gateway-764140025``Name:    gateway-764140025``Namespace:  fail``Image(s):  nginx``Selector:  app=gateway,pod-template-``hash``=764140025``Labels:    app=gateway``  ``pod-template-``hash``=764140025``Replicas:  0 current / 1 desired``Pods Status:  0 Running / 0 Waiting / 0 Succeeded / 0 Failed``No volumes.``Events:``FirstSeen  LastSeen  Count  From        SubObjectPath  Type    Reason   Message``---------  --------  -----  ----        -------------  --------  ------   -------``6m    28s   15 {replicaset-controller }      Warning   FailedCreate  Error creating: pods``"gateway-764140025-"` `is forbidden: [maximum memory usage per Pod is 100Mi, but request is 5368709120., maximum memory usage per Container is 100Mi, but request is 5Gi.]
```

上面可知，集群管理员设置了每个 Pod 的最大内存使用量为 100Mi。你可以运行 kubectl describe limitrange 来查看当前租户的限制。

那么现在就有3个选择：
\- 要求你的集群管理员提升限额；
\- 减少 deployment 的请求或者限额设置；
\- 直接编辑限额；

**6. 资源配额**
和资源限额类似，Kubernetes 也允许管理员给每个 namespace 设置资源配额。这些配额可以在 Pods，Deployments，PersistentVolumes，CPU，内存等资源上设置软性或者硬性限制。让我们看看超出资源配额后会发生什么。以下是我们的 deployment 例子:

```
# test-quota.yaml``apiVersion: extensions``/v1beta1``kind: Deployment``metadata:``name: gateway-``quota``spec:``template:``spec:`` ``containers:``  ``- name:``test``-container``   ``image: nginx` `我们可用 kubectl create -f``test``-``quota``.yaml 创建，然后观察我们的 Pods：``$ kubectl get pods``NAME              READY   STATUS  RESTARTS  AGE``gateway-``quota``-551394438-pix5d  1``/1`    `Running  0     16s` `看起来很好，现在让我们扩展到 3 个副本：kubectl scale deploy``/gateway-quota` `--replicas=3，然后再次观察 Pods：``$ kubectl get pods``NAME              READY   STATUS  RESTARTS  AGE``gateway-``quota``-551394438-pix5d  1``/1`    `Running  0     9m` `啊，我们的pod去哪了？让我们观察一下 deployment：``$ kubectl describe deploy``/gateway-quota``Name:      gateway-``quota``Namespace:    fail``CreationTimestamp:  Sat, 11 Feb 2017 16:33:16 -0500``Labels:      app=gateway``Selector:    app=gateway``Replicas:    1 updated | 3 total | 1 available | 2 unavailable``StrategyType:    RollingUpdate``MinReadySeconds:  0``RollingUpdateStrategy:  1 max unavailable, 1 max surge``OldReplicaSets:    ``NewReplicaSet:    gateway-``quota``-551394438 (1``/3` `replicas created)``Events:``FirstSeen  LastSeen  Count  From        SubObjectPath  Type    Reason     Message``---------  --------  -----  ----        -------------  --------  ------     -------``9m    9m   1  {deployment-controller }      Normal   ScalingReplicaSet  Scaled up replica``set` `gateway-``quota``-551394438 to 1``5m    5m   1  {deployment-controller }      Normal   ScalingReplicaSet  Scaled up replica``set` `gateway-``quota``-551394438 to 3` `在最后一行，我们可以看到 ReplicaSet 被告知扩展到 3 。我们用 describe 来观察一下这个 ReplicaSet 以了解更多信息：``kubectl describe replicaset gateway-``quota``-551394438``Name:    gateway-``quota``-551394438``Namespace:  fail``Image(s):  nginx``Selector:  app=gateway,pod-template-``hash``=551394438``Labels:    app=gateway``  ``pod-template-``hash``=551394438``Replicas:  1 current / 3 desired``Pods Status:  1 Running / 0 Waiting / 0 Succeeded / 0 Failed``No volumes.``Events:``FirstSeen  LastSeen  Count  From        SubObjectPath  Type    Reason     Message``---------  --------  -----  ----        -------------  --------  ------     -------``11m    11m   1  {replicaset-controller }      Normal   SuccessfulCreate  Created pod: gateway-``quota``-551394438-pix5d``11m    30s   33 {replicaset-controller }      Warning   FailedCreate    Error creating: pods``"gateway-quota-551394438-"` `is forbidden: exceeded``quota``: compute-resources, requested: pods=1, used: pods=1, limited: pods=1
```

上面可以看出，我们的 ReplicaSet 无法创建更多的 pods 了，因为配额限制了：exceeded quota: compute-resources, requested: pods=1, used: pods=1, limited: pods=1。

和资源限额类似，我们现在也有3个选项：
\- 要求集群管理员提升该 namespace 的配额
\- 删除或者收缩该 namespace 下其它的 deployment
\- 直接编辑配额

**7. 集群资源不足**
除非你的集群开通了集群自动伸缩功能，否则总有一天你的集群中 CPU 和内存资源会耗尽。这不是说 CPU 和内存被完全使用了,而是指它们被 Kubernetes 调度器完全使用了。如同我们在第 5 点看到的，集群管理员可以限制开发者能够申请分配给 pod 或者容器的 CPU 或者内存的数量。聪明的管理员也会设置一个默认的 CPU/内存 申请数量，在开发者未提供申请额度时使用。

如果你所有的工作都在 default 这个 namespace 下工作，你很可能有个默认值 100m 的容器 CPU申请额度，对此你甚至可能都不清楚。运行 kubectl describe ns default 检查一下是否如此。我们假定你的 Kubernetes 集群只有一个包含 CPU 的节点。你的 Kubernetes 集群有 1000m 的可调度 CPU。当前忽略其它的系统 pods（kubectl -n kube-system get pods），你的单节点集群能部署 10 个 pod(每个 pod 都只有一个包含 100m 的容器)。

10 Pods * (1 Container * 100m) = 1000m == Cluster CPUs

当你扩大到 11 个的时候，会发生什么？下面是一个申请 1CPU（1000m）的 deployment 例子

```
# cpu-scale.yaml``apiVersion: extensions``/v1beta1``kind: Deployment``metadata:``name: cpu-scale``spec:``template:``metadata:`` ``labels:``  ``app: cpu-scale``spec:`` ``containers:``  ``- name:``test``-container``   ``image: nginx``   ``resources:``    ``requests:``     ``cpu: 1` `我把这个应用部署到有 2 个可用 CPU 的集群。除了我的 cpu-scale 应用，Kubernetes 内部服务也在消耗 CPU 和内存。` `我们可以用 kubectl create -f cpu-scale.yaml 部署这个应用，并观察 pods：``$ kubectl get pods``NAME            READY   STATUS  RESTARTS  AGE``cpu-scale-908056305-xstti  1``/1`    `Running  0     5m` `第一个 pod 被调度并运行了。我们看看扩展一个会发生什么：``$ kubectl scale deploy``/cpu-scale` `--replicas=2``deployment``"cpu-scale"` `scaled``$ kubectl get pods``NAME            READY   STATUS  RESTARTS  AGE``cpu-scale-908056305-phb4j  0``/1`    `Pending  0     4m``cpu-scale-908056305-xstti  1``/1`    `Running  0     5m` `我们的第二个pod一直处于 Pending，被阻塞了。我们可以 describe 这第二个 pod 查看更多的信息:``$ kubectl describe pod cpu-scale-908056305-phb4j``Name:    cpu-scale-908056305-phb4j``Namespace:  fail``Node:    gke-ctm-1-sysdig2-35e99c16-qwds``/10``.128.0.4``Start Time:  Sun, 12 Feb 2017 08:57:51 -0500``Labels:    app=cpu-scale``  ``pod-template-``hash``=908056305``Status:    Pending``IP:    ``Controllers:  ReplicaSet``/cpu-scale-908056305``[...]``Events:``FirstSeen  LastSeen  Count  From      SubObjectPath  Type    Reason     Message``---------  --------  -----  ----      -------------  --------  ------     -------``3m    3m   1  {default-scheduler }      Warning   FailedScheduling  pod (cpu-scale-908056305-phb4j) failed to fit``in` `any node``fit failure on node (gke-ctm-1-sysdig2-35e99c16-wx0s): Insufficient cpu``fit failure on node (gke-ctm-1-sysdig2-35e99c16-tgfm): Insufficient cpu``fit failure on node (gke-ctm-1-sysdig2-35e99c16-qwds): Insufficient cpu
```

Events 模块告诉我们 Kubernetes 调度器（default-scheduler）无法调度这个 pod 因为它无法匹配任何节点。它甚至告诉我们每个节点哪个扩展点失败了（Insufficient cpu）。

那么我们如何解决这个问题？如果你太渴望你申请的 CPU/内存 的大小，你可以减少申请的大小并重新部署。当然，你也可以请求你的集群管理员扩展这个集群（因为很可能你不是唯一一个碰到这个问题的人）。

现在你可能会想：我们的 Kubernetes 节点是在我们的云提供商的自动伸缩群组里，为什么他们没有生效呢？原因是，你的云提供商没有深入理解 Kubernetes 调度器是做啥的。利用 Kubernetes 的集群自动伸缩能力允许你的集群根据调度器的需求自动伸缩它自身。如果你在使用 GCE，集群伸缩能力是一个 beta 特性。

**8. 持久化卷挂载失败**
另一个常见错误是创建了一个引用不存在的持久化卷（PersistentVolumes）的 deployment。不论你是使用 PersistentVolumeClaims（你应该使用这个！），还是直接访问持久化磁盘，最终结果都是类似的。

下面是我们的测试 deployment，它想使用一个名为 my-data-disk 的 GCE 持久化卷：

```
# volume-test.yaml``apiVersion: extensions``/v1beta1``kind: Deployment``metadata:``name: volume-``test``spec:``template:``metadata:`` ``labels:``  ``app: volume-``test``spec:`` ``containers:``  ``- name:``test``-container``   ``image: nginx``   ``volumeMounts:``   ``- mountPath:``/test``    ``name:``test``-volume`` ``volumes:`` ``- name:``test``-volume``  ``# This GCE PD must already exist (oops!)``  ``gcePersistentDisk:``   ``pdName: my-data-disk``   ``fsType: ext4` `让我们创建这个 deployment：kubectl create -f volume-``test``.yaml，过几分钟后查看 pod：``kubectl get pods``NAME              READY   STATUS       RESTARTS  AGE``volume-``test``-3922807804-33nux  0``/1`    `ContainerCreating  0     3m` `3 分钟的等待容器创建时间是很长了。让我们用 describe 来查看这个 pod，看看到底发生了什么：``$ kubectl describe pod volume-``test``-3922807804-33nux``Name:    volume-``test``-3922807804-33nux``Namespace:  fail``Node:    gke-ctm-1-sysdig2-35e99c16-qwds``/10``.128.0.4``Start Time:  Sun, 12 Feb 2017 09:24:50 -0500``Labels:    app=volume-``test``  ``pod-template-``hash``=3922807804``Status:    Pending``IP:    ``Controllers:  ReplicaSet``/volume-test-3922807804``[...]``Volumes:``test``-volume:``Type:  GCEPersistentDisk (a Persistent Disk resource``in` `Google Compute Engine)``PDName:  my-data-disk``FSType:  ext4``Partition:  0``ReadOnly:  ``false``[...]``Events:``FirstSeen  LastSeen  Count  From            SubObjectPath  Type    Reason   Message``---------  --------  -----  ----            -------------  --------  ------   -------``4m    4m   1  {default-scheduler }            Normal   Scheduled  Successfully assigned volume-``test``-3922807804-33nux to gke-ctm-1-sysdig2-35e99c16-qwds``1m    1m   1  {kubelet gke-ctm-1-sysdig2-35e99c16-qwds}      Warning   FailedMount Unable to``mount` `volumes``for` `pod``"volume-test-3922807804-33nux_fail(e2180d94-f12e-11e6-bd01-42010af0012c)"``: timeout expired waiting``for` `volumes to attach``/mount` `for` `pod``"volume-test-3922807804-33nux"``/``"fail"``. list of unattached``/unmounted` `volumes=[``test``-volume]``1m    1m   1  {kubelet gke-ctm-1-sysdig2-35e99c16-qwds}      Warning   FailedSync Error syncing pod, skipping: timeout expired waiting``for` `volumes to attach``/mount` `for` `pod``"volume-test-3922807804-33nux"``/``"fail"``. list of unattached``/unmounted` `volumes=[``test``-volume]``3m    50s   3  {controller-manager }            Warning   FailedMount Failed to attach volume``"test-volume"` `on node``"gke-ctm-1-sysdig2-35e99c16-qwds"` `with: GCE persistent disk not found: diskName=``"my-data-disk"` `zone=``"us-central1-a"
```

Events 模块留有我们一直在寻找的线索。我们的 pod 被正确调度到了一个节点（Successfully assigned volume-test-3922807804-33nux to gke-ctm-1-sysdig2-35e99c16-qwds），但是那个节点上的 kubelet 无法挂载期望的卷 test-volume。那个卷本应该在持久化磁盘被关联到这个节点的时候就被创建了，但是，正如我们看到的，controller-manager 失败了：Failed to attach volume "test-volume" on node "gke-ctm-1-sysdig2-35e99c16-qwds" with: GCE persistent disk not found: diskName="my-data-disk" zone="us-central1-a"。

最后一条信息相当清楚了：为了解决这个问题，我们需要在 GKE 的 us-central1-a 区中创建一个名为 my-data-disk 的持久化卷。一旦这个磁盘创建完成，controller-manager 将挂载这块磁盘，并启动容器创建过程。

**9. 校验错误**
看着整个 build-test-deploy 任务到了 deploy 步骤却失败了，原因竟是 Kubernetes 对象不合法。还有什么比这更让人沮丧的！

```
你可能之前也碰到过这种错误:``$ kubectl create -f``test``-application.deploy.yaml``error: error validating``"test-application.deploy.yaml"``: error validating data: found invalid field resources``for` `v1.PodSpec;``if` `you choose to ignore these errors, turn validation off with --validate=``false` `在这个例子中，我尝试创建以下 deployment：``# test-application.deploy.yaml``apiVersion: extensions``/v1beta1``kind: Deployment``metadata:``name:``test``-app``spec:``template:``metadata:`` ``labels:``  ``app:``test``-app``spec:`` ``containers:`` ``- image: nginx``  ``name: nginx`` ``resources:``  ``limits:``   ``cpu: 100m``   ``memory: 200Mi``  ``requests:``   ``cpu: 100m``   ``memory: 100Mi
```

一眼望去，这个 YAML 文件是正确的，但错误消息会证明是有用的。错误说的是 found invalid field resources for v1.PodSpec，再仔细看一下 v1.PodSpec， 我们可以看到 resource 对象变成了 v1.PodSpec的一个子对象。事实上它应该是 v1.Container 的子对象。在把 resource 对象缩进一层后，这个 deployment 对象就可以正常工作了。

除了查找缩进错误，另一个常见的错误是写错了对象名（比如 peristentVolumeClaim 写成了 persistentVolumeClaim），这样的错误有时会很费你的时间！

为了能在早期就发现这些错误，我推荐在 pre-commit 钩子或者构建的测试阶段添加一些校验步骤。例如，你可以：
**1.** 用 python -c 'import yaml,sys;yaml.safe_load(sys.stdin)' < test-application.deployment.yaml 验证 YAML 格式
**2.** 使用标识 --dry-run 来验证 Kubernetes API 对象，比如这样：kubectl create -f test-application.deploy.yaml --dry-run --validate=true

**重要提醒：**校验 Kubernetes 对象的机制是在服务端的校验，这意味着 kubectl 必须有一个在工作的 Kubernetes 集群与之通信。不幸的是，当前 kubectl 还没有客户端的校验选项，但是已经有 issue（kubernetes/kubernetes #29410 和 kubernetes/kubernetes #11488）在跟踪这个缺失的特性了。

**10. 容器镜像没有更新**
可能使用 Kubernetes 的大多数人都碰到过这个问题，它也确实是一个难题。

这个场景就像下面这样：
**1.** 使用一个镜像 tag（比如：rosskulinski/myapplication:v1） 创建一个 deployment
**2.** 注意到 myapplication 镜像中存在一个 bug
**3.** 构建了一个新的镜像，并推送到了相同的 tag（rosskukulinski/myapplication:v1）
**4.** 删除了所有 myapplication 的 pods，新的实例被 deployment 创建出了
**5.** 发现 bug 仍然存在
**6.** 重复 3-5 步直到你抓狂为止

这个问题关系到 Kubernetes 在启动 pod 内的容器时是如何决策是否做 docker pull 动作的。

在 v1.Container 说明中，有一个选项 ImagePullPolicy：

```
Image pull policy. One of Always, Never, IfNotPresent. Defaults to Always``if` `:latest tag is specified, or IfNotPresent otherwise.
```

因为我们把我们的镜像 tag 标记为 :v1，默认的镜像拉取策略是 IfNotPresent。Kubelet 在本地已经有一份 rosskukulinski/myapplication:v1 的拷贝了，因此它就不会在做 docker pull 动作了。当新的 pod 出现的时候，它仍然使用了老的有问题的镜像。

有三个方法来解决这个问题：
**1.** 切成 :latest tag（千万不要这么做！）
**2.** deployment 中指定 ImagePullPolicy: Always
**3.** 使用唯一的 tag（比如基于你的代码版本控制器的 commit id）

在开发阶段或者要快速验证原型的时候，我会指定 ImagePullPolicy: Always 这样我可以使用相同的 tag 来构建和推送。然而，在我的产品部署阶段，我使用基于 Git SHA-1 的唯一 tag。这样很容易查到产品部署的应用使用的源代码。

所以说，当使用kubernetes时，我们有这么多地方要当心，一般来说，大部分常见的部署失败都可以用下面的命令定位出来：
**1.** kubectl describe deployment/<deployname>
**2.** kubectl describe replicaset/<rsname>
**3.** kubectl get pods
**4.** kubectl describe pod/<podname>
**5.** kubectl logs <podname> --previous

下面是一个bash脚本，它在 CI/CD 的部署过程中任何失败的时候，都可以跑。在 Jenkins等的构建输出中，将显示有用的 Kubernetes 信息，帮助开发者快速找到任何明显的问题。

```
#!/bin/bash` `if` `[ -z``"$1"` `]``then`` ``echo` `"ERROR: No deployment specified"`` ``exit` `1``fi` `DEPLOY=${1}``NAMESPACE=${2:=default}` `printf` `"\n\nOk - Let's figure out why this deployment might have failed"` `printf` `"\n\n------------------------------\n\n"` `printf` `"> kubectl describe deployment ${DEPLOY} --namespace=${NAMESPACE}\n\n"``kubectl describe deployment ${DEPLOY} --namespace=${NAMESPACE}` `printf` `"\n\n------------------------------\n\n"` `CURRENT_GEN=$(kubectl get deployment ${DEPLOY} --namespace=${NAMESPACE} -o jsonpath=``'{.metadata.generation}'``)``OBS_GEN=$(kubectl get deployment ${DEPLOY} --namespace=${NAMESPACE} -o jsonpath=``'{.status.observedGeneration}'``)``REPLICAS=$(kubectl get deployment ${DEPLOY} --namespace=${NAMESPACE} -o jsonpath=``'{.status.replicas}'``)``UPDATED_REPLICAS=$(kubectl get deployment ${DEPLOY} --namespace=${NAMESPACE} -o jsonpath=``'{.status.updatedReplicas}'``)``AVAILABLE_REPLICAS=$(kubectl get deployment ${DEPLOY} --namespace=${NAMESPACE} -o jsonpath=``'{.status.availableReplicas}'``)` `if` `[``"$AVAILABLE_REPLICAS"` `==``"$REPLICAS"` `] && \``  ``[``"$UPDATED_REPLICAS"` `==``"$REPLICAS"` `] ;``then` ` ``printf` `"Available Replicas (${AVAILABLE_REPLICAS}) equals Current Replicas (${REPLICAS}) \n"`` ``printf` `"Updated Replicas (${UPDATED_REPLICAS}) equals Current Replicas (${REPLICAS}). \n"`` ``printf` `"Are you sure the deploy failed?\n\n"`` ``exit` `0``fi` `if` `[``"$AVAILABLE_REPLICAS"` `!=``"$REPLICAS"` `] ;``then`` ``printf` `"Available Replicas (${AVAILABLE_REPLICAS}) does not equal Current Replicas (${REPLICAS}) \n"``fi` `if` `[``"$UPDATED_REPLICAS"` `!=``"$REPLICAS"` `] ;``then`` ``printf` `"Updated Replicas (${UPDATED_REPLICAS}) does not equal Current Replicas (${REPLICAS}) \n"``fi` `printf` `"\n\n------------------------------\n\n"` `NEW_RS=$(kubectl describe deploy ${DEPLOY} --namespace=${NAMESPACE} |``grep` `"NewReplicaSet"` `|``awk` `'{print $2}'``)``POD_HASH=$(kubectl get rs ${NEW_RS} --namespace=${NAMESPACE} -o jsonpath=``'{.metadata.labels.pod-template-hash}'``)` `printf` `"Pods for this deployment:\n\n"``printf` `"> kubectl get pods --namespace=${NAMESPACE} -l pod-template-hash=${POD_HASH}\n\n"``kubectl get pods --namespace=${NAMESPACE} -l pod-template-``hash``=${POD_HASH}` `printf` `"\n\n------------------------------\n\n"` `printf` `"Detailed pods for this deployment:\n\n"` `printf` `"> kubectl describe pods --namespace=${NAMESPACE} -l pod-template-hash=${POD_HASH}\n\n"``kubectl describe pods --namespace=${NAMESPACE} -l pod-template-``hash``=${POD_HASH}` `printf` `"\n\n------------------------------\n\n"``printf` `"Containers that are currently 'waiting':\n\n"``printf` `"> kubectl get pods --namespace=${NAMESPACE} -l pod-template-hash=${POD_HASH} -o jsonpath='...'\n"``kubectl get pods --namespace=${NAMESPACE} -l pod-template-``hash``=${POD_HASH} -o jsonpath=``'{"\n"}{range .items[*]}{@.metadata.name}:{"\n"}{range @.status.conditions[*]}{"\t"}{@.lastTransitionTime}: {@.type}={@.status}{"\n"}{end}{"\n"}{"\tWaiting Containers\n"}{range @.status.containerStatuses[?(@.state.waiting)]}{"\t\tName: "}{@.name}{"\n\t\tImage: "}{@.image}{"\n\t\tState: Waiting"}{"\n\t\tMessage: "}{@.state.waiting.message}{"\n\t\tReason: "}{@.state.waiting.reason}{end}{"\n"}{end}'` `printf` `"\n\n------------------------------\n\n"` `printf` `"Pods with Terminated state\n\n"` `printf` `"> kubectl get pods --namespace=${NAMESPACE} -l pod-template-hash=${POD_HASH} -o jsonpath='...'\n"``kubectl get pods --namespace=${NAMESPACE} -l pod-template-``hash``=${POD_HASH} -o jsonpath=``'{"\n"}{range .items[*]}{"\n"}{@.metadata.name}:{"\n"}{"\n\tTerminated Containers\n"}{range @.status.containerStatuses[?(@.lastState.terminated)]}{"\t\tName: "}{@.name}{"\n\t\tImage: "}{@.image}{"\n\t\texitCode: "}{@.lastState.terminated.exitCode}{"\n\t\tReason: "}{@.lastState.terminated.reason}{"\n"}{end}{"\n"}{end}'` `printf` `"\n\n------------------------------\n\n"` `printf` `"Trying to get previous logs from each Terminated pod\n\n"` `kubectl get pods --namespace=${NAMESPACE} -l pod-template-``hash``=${POD_HASH} --no-headers |``awk` `'{print $1}'` `|``xargs` `-I pod sh -c``"printf \"pod\n\n\"; kubectl --namespace=${NAMESPACE} logs --previous --tail=100 --timestamps pod; printf \"\n\n\""
```

*************** 当你发现自己的才华撑不起野心时，就请安静下来学习吧！***************