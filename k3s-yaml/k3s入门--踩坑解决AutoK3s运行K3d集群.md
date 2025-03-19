# k3s入门--踩坑解决AutoK3s运行K3d集群



先简单介绍下各个名词，`k3s`理解为是k8s的简化版只保留核心模块。

`k3s`集群怎么搭建呢？一种熟练的会敲命令行，另一群入门的会用可视化界面搭建集群，即`AutoK3s`。

`k3s`集群运行在什么环境呢？一种是普遍的有多台linux机器（或虚拟机），另一种入门的就是在一台linux机器上，让`k3s`集群运行在docker容器里面。

今天我们就在一台虚拟机上用 `AutoK3s` 可视化界面搭建一套多节点的 `k3s` 集群，这种集群的类型官方就叫 `k3d`，即 `k3s in docker` 模式。

这篇文章视频 [www.bilibili.com/video/BV1g3…](https://link.juejin.cn/?target=https%3A%2F%2Fwww.bilibili.com%2Fvideo%2FBV1g3zbYiEiN%2F)

一些参考资料：

[rancher官网](https://link.juejin.cn/?target=https%3A%2F%2Fdocs.rancher.cn%2Fdocs%2Fk3s%2Fautok3s%2F_index)

[【K3s踩坑记录】1-集群搭建](https://link.juejin.cn/?target=https%3A%2F%2Fsheep-in-box.github.io%2F2024%2F08%2F08%2F%E3%80%90K3s%E8%B8%A9%E5%9D%91%E8%AE%B0%E5%BD%95%E3%80%911-%E9%9B%86%E7%BE%A4%E6%90%AD%E5%BB%BA%2F)

[使用K3s快速搭建集群](https://link.juejin.cn/?target=https%3A%2F%2Fwww.yuque.com%2Fwukong-zorrm%2Fqdoy5p%2Flgspzc)

[国内镜像地址](https://link.juejin.cn/?target=https%3A%2F%2Fdocker.linkedbus.com%2F%23mirror-address)

## 干净centos服务器安装docker

```swift
swift代码解读复制代码# 设置yum国内源
sed -e 's|^mirrorlist=|#mirrorlist=|g' \
          -e 's|^#baseurl=http://mirror.centos.org|baseurl=http://mirrors.aliyun.com|g' \
          -i.bak \
          /etc/yum.repos.d/CentOS-*.repo

# 同步
yum makecache

#关闭防火墙
systemctl stop firewalld 
systemctl disable firewalld

#关闭selinx
setenforce 0
sed -i s#SELINUX=enforcing#SELINUX=disabled#g /etc/sysconfig/selinux
 
#安装 docker 依赖包
yum install -y yum-utils device-mapper-persistent-data lvm2

#配置 docker-ce 国内 yum 源（阿里云）
yum-config-manager --add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo

#安装 docker-ce
yum install -y docker-ce docker-ce-cli containerd.io
systemctl enable docker
systemctl start docker

#修改daemon
mkdir -p /etc/docker
  echo -e "{
  \"registry-mirrors\": [
    \"https://docker.linkedbus.com\",
    \"https://dockerpull.org\",
    \"https://s1qalke8.mirror.aliyuncs.com\",
    \"https://registry.docker-cn.com\",
    \"http://hub-mirror.c.163.com\",
    \"https://docker.mirrors.ustc.edu.cn\"
  ],
  \"insecure-registries\":[],
  \"log-driver\": \"json-file\",
  \"log-opts\": {
    \"max-size\": \"100m\",
    \"max-file\": \"3\",
    \"labels\": \"production_status\",
    \"env\": \"os,customer\"
  }
}" > /etc/docker/daemon.json

# 重启docker
systemctl daemon-reload
systemctl restart docker
```

## 运行AutoK3s并支持k3d

```arduino
arduino

代码解读
复制代码docker run -itd --restart=unless-stopped --net host -v /var/run/docker.sock:/var/run/docker.sock cnrancher/autok3s:v0.6.0
```

现在可以访问8080端口打开`AutoK3s`UI界面配置集群

![image.png](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/24a6c25fa8f240d08d088d1723f147cb~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5LiA5Liq5LiN5Lya6YeN5aSN55qEaWQ=:q75.awebp?rk3s=f64ab15b&x-expires=1742802687&x-signature=x%2B1g8KTFD8dqm1I67GHEOXn%2B1zA%3D)

![image.png](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/d108b46ca43b471380366449b4328e14~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5LiA5Liq5LiN5Lya6YeN5aSN55qEaWQ=:q75.awebp?rk3s=f64ab15b&x-expires=1742802687&x-signature=267vUbPzcACgd5ru1epLX%2Bjm0LE%3D)

## 新建集群

在Cluster界面，点Create新建，选k3d，点开Advance

![image.png](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/8132a40fe37b49719ba1fa5904c35c44~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5LiA5Liq5LiN5Lya6YeN5aSN55qEaWQ=:q75.awebp?rk3s=f64ab15b&x-expires=1742802687&x-signature=yVoJMn4ut%2BvvAsX7De6%2FMuRY2t8%3D)

设置Ports

注意端口范围必须 30000-32767，其中30181和30180可以用同一个端口，也可不同

```java
java

代码解读
复制代码30181:30180@loadbalancer
```

更多格式参考

```java
java代码解读复制代码30182:30180@agent:0
30180:30180@loadbalancer
```

设置Registry

```lua
lua代码解读复制代码mirrors:
  docker.io:
    endpoint:
      - "https://docker.linkedbus.com"
      - "https://dockerpull.org"
      - "https://docker.xuanyuan.me"
      - "https://registry.cn-hangzhou.aliyuncs.com/"
      - "https://registry.dockermirror.com"
  quay.io:
    endpoint:
      - "https://quay.tencentcloudcr.com/"
  registry.k8s.io:
    endpoint:
      - "https://registry.aliyuncs.com/v2/google_containers"
  gcr.io:
    endpoint:
      - "https://gcr.m.daocloud.io/"
  k8s.gcr.io:
    endpoint:
      - "https://registry.aliyuncs.com/google_containers"
  ghcr.io:
    endpoint:
      - "https://ghcr.m.daocloud.io/"
```

![image.png](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/f464d6dd61b74225b3219664a6a95867~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5LiA5Liq5LiN5Lya6YeN5aSN55qEaWQ=:q75.awebp?rk3s=f64ab15b&x-expires=1742802687&x-signature=pnU79OWw33p0%2B5Zl%2FuORRYZFLCw%3D)

![image.png](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/5bbcb32b48414805ae4fee462848439e~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5LiA5Liq5LiN5Lya6YeN5aSN55qEaWQ=:q75.awebp?rk3s=f64ab15b&x-expires=1742802687&x-signature=UFnc94Df8Jq146CNy560BVzfOcA%3D)

成功运行后，看虚拟机多了三个docker容易，分别是我们新建的 master,worker和loadbalancer，如果刚才master和worker写多，也会相应多容器，后面我们部署的应用就会在这些master和worker里面运行。

![image.png](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/e7db0f214f4c4b34997060ea4c9a018d~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5LiA5Liq5LiN5Lya6YeN5aSN55qEaWQ=:q75.awebp?rk3s=f64ab15b&x-expires=1742802687&x-signature=oLTMv4rJZdP9iReMmBNpuSXFHe8%3D)

## 【非必需处理】填坑修复agent执行kubectl命令报错

在两个节点中去执行 kubuctl 命令，发现只有 server节点有效，agent节点报错

需要拷贝server节点的配置文件到agent节点中，并修改里面url地址

![image.png](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/b4eeb78756fa4e07b99edd5a33d5c44b~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5LiA5Liq5LiN5Lya6YeN5aSN55qEaWQ=:q75.awebp?rk3s=f64ab15b&x-expires=1742802687&x-signature=dOib9VSIDaDIJ2NPCiavJEr4QHo%3D)

```sql
sql

代码解读
复制代码kubectl describe pod
```

![image.png](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/a1a6d08a468d4790ad3d00b121fb8e06~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5LiA5Liq5LiN5Lya6YeN5aSN55qEaWQ=:q75.awebp?rk3s=f64ab15b&x-expires=1742802687&x-signature=6xO2haCW9q42oojG2i3o9oso86I%3D)

server 节点执行命令正常

![image.png](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/3e9892236c474427adf7e2c0aab35438~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5LiA5Liq5LiN5Lya6YeN5aSN55qEaWQ=:q75.awebp?rk3s=f64ab15b&x-expires=1742802687&x-signature=VLciCy%2FBOK0mf28dljGr3Ua%2BbOI%3D)

agent 节点执行命令报错 `The connection to the server localhost:8080 was refused - did you specify the right host or port?`

![image.png](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/bac30aa6dfb148d8ab45d7e5ecc80286~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5LiA5Liq5LiN5Lya6YeN5aSN55qEaWQ=:q75.awebp?rk3s=f64ab15b&x-expires=1742802687&x-signature=4N3BsnrNHqS0W7J47DBDTmzSh3E%3D)

现在要把server节点的 `kubeconfig.yaml` 拷贝到 agent 节点 `k3s.yaml` 文件

查看 server 的 containerid 是 b88f5391ac22

查看 agent 的 containerid 是 1e190b196813

![image.png](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/a0004060d9ec4ec19b9d1956d8bcbb2b~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5LiA5Liq5LiN5Lya6YeN5aSN55qEaWQ=:q75.awebp?rk3s=f64ab15b&x-expires=1742802687&x-signature=FXfZRyTJoVLEEZ1XYV4lzZOYbTw%3D)

```bash
bash代码解读复制代码docker cp b88f5391ac22:/output/kubeconfig.yaml k3s.yaml

docker inspect b88f5391ac22
```

看到其中ip地址

![image.png](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/213b6a88a1ff495cbb58a696ec34a195~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5LiA5Liq5LiN5Lya6YeN5aSN55qEaWQ=:q75.awebp?rk3s=f64ab15b&x-expires=1742802687&x-signature=ByZJoVgndDPd36LgRiuQbFO5lmk%3D)

修改 k3s.yaml 地址

```
代码解读
复制代码vi k3s.yaml
```

![image.png](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/6b0e558b51334c91a2dd94f2f991b90d~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5LiA5Liq5LiN5Lya6YeN5aSN55qEaWQ=:q75.awebp?rk3s=f64ab15b&x-expires=1742802687&x-signature=eMcnuO4da6DLolp2duO%2Bk6rmP6M%3D)

```bash
bash代码解读复制代码# 在agent中新建目录
docker exec 1e190b196813 mkdir /.kube

# 复制到agent中
docker cp k3s.yaml 1e190b196813:/.kube/config

# 重启agent节点
docker restart 1e190b196813
```

现在一切正常了，agent中也可执行kubectl命令

![image.png](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/b54952f63a2041178448738fd93c2dc9~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5LiA5Liq5LiN5Lya6YeN5aSN55qEaWQ=:q75.awebp?rk3s=f64ab15b&x-expires=1742802687&x-signature=P7p8ItRTG2HWuODqwYpB9Kvy1LI%3D)

## 在集群中部署nginx应用

打开Explorer

![image.png](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/e071ba8545014b9a998f85b11c286906~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5LiA5Liq5LiN5Lya6YeN5aSN55qEaWQ=:q75.awebp?rk3s=f64ab15b&x-expires=1742802687&x-signature=zqAopj7wTHW9SCTLCRuza3JFyM8%3D)

点Explorer进入管理，路由出错，点 Back to Home

![image.png](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/990e5b4152934d4bbade46d2ed5a9ea0~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5LiA5Liq5LiN5Lya6YeN5aSN55qEaWQ=:q75.awebp?rk3s=f64ab15b&x-expires=1742802687&x-signature=aLJPWO7wN36cZcybm6BjCODq9a8%3D)

在 Deployments 中 Create 新建应用

![image.png](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/c760d9ea655f42c1a6647b8bf9db9a43~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5LiA5Liq5LiN5Lya6YeN5aSN55qEaWQ=:q75.awebp?rk3s=f64ab15b&x-expires=1742802687&x-signature=NuG1P5ka0UmIwbekVa6EqRw%2BpSU%3D)

我使用我腾讯云上镜像

```bash
bash

代码解读
复制代码ccr.ccs.tencentyun.com/rootegg/nginx:1.27.2
```

![image.png](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/163256a722e042068d9384a6f2f28552~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5LiA5Liq5LiN5Lya6YeN5aSN55qEaWQ=:q75.awebp?rk3s=f64ab15b&x-expires=1742802687&x-signature=lYYaWgQ0StDZmbt%2FPjh%2BdFb7M0Q%3D)

注意要填前面loaderbalance的30180端口，这样我们就可以用30181来访问nginx了

![image.png](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/61ac541054c8407e841dbfb64b2834c7~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5LiA5Liq5LiN5Lya6YeN5aSN55qEaWQ=:q75.awebp?rk3s=f64ab15b&x-expires=1742802687&x-signature=jr7MQCmPZ4ko7YcQrgiWpvzooTU%3D)

可以到前面cluster页面查看部署日志

```sql
sql

代码解读
复制代码kubectl describe pod
```

![image.png](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/09a9c39f787747eebc5fdeff6fe9544e~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5LiA5Liq5LiN5Lya6YeN5aSN55qEaWQ=:q75.awebp?rk3s=f64ab15b&x-expires=1742802687&x-signature=G2IPMD54Cd7WIJwzzH7gk4qbXtY%3D)

显示 `active` 就成功了，如果这里一直显示 `Deployment does not have minimum availability. `刚才那句，就说明刚才registry设置docker.io镜像那里地址被墙了，要重新换国内镜像地址。

![image.png](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/e5cd687cfee8408bb39ef65978cbb731~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5LiA5Liq5LiN5Lya6YeN5aSN55qEaWQ=:q75.awebp?rk3s=f64ab15b&x-expires=1742802687&x-signature=t8sBycHkXeSpwlBcvqL5V%2B7KWIo%3D)

## 成功访问nginx

![image.png](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/15d0ab34b4c74e6ba82036d56848abbf~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5LiA5Liq5LiN5Lya6YeN5aSN55qEaWQ=:q75.awebp?rk3s=f64ab15b&x-expires=1742802687&x-signature=95C8txO2jwNsJq%2FUHZK48EVVyYw%3D)

