# k3s在线和离线安装过程



因为还对k8s不熟悉，就先用简化版的k3s跑起来，再逐步学习。

这两天试了k3s的自动化脚本`AutoK3S`的`native`和`k3d`都没有成功，native模式下没部署成功，因为网络等问题。k3d部署成功了，但是运行容器没成功，应该是containerd容器拉取镜像的网络问题。

现在用k3s脚本来部署，但是containerd还是拉取镜像失败，又改成k3s+docker模式，终于成功了。

这篇文章就是从头k3s+docker部署，并成功运行nginx的步骤。还是很不容易，按照下面的命名一句句执行就能成功，万事开头难吧！还是使用centos7.6虚拟机单机部署。

![image.png](https://p9-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/f18a1104591d4431ae9536e3aa63a16b~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5LiA5Liq5LiN5Lya6YeN5aSN55qEaWQ=:q75.awebp?rk3s=f64ab15b&x-expires=1742717246&x-signature=66sHr6a9Mxob0CaW2jkFD%2Fk3q9c%3D)

## 先yum用国内镜像

```bash
bash代码解读复制代码

sed -e 's|^mirrorlist=|#mirrorlist=|g' \
          -e 's|^#baseurl=http://mirror.centos.org|baseurl=http://mirrors.aliyun.com|g' \
          -i.bak \
          /etc/yum.repos.d/CentOS-*.repo
          
yum makecache

#关闭防火墙
systemctl stop firewalld 
systemctl disable firewalld

#关闭selinx
setenforce 0
sed -i s#SELINUX=enforcing#SELINUX=disabled#g /etc/sysconfig/selinux
```

## 方式一：containerd + 手动部署镜像方式

参考 [sheep-in-box.github.io/2024/08/08/…](https://link.juejin.cn/?target=https%3A%2F%2Fsheep-in-box.github.io%2F2024%2F08%2F08%2F%E3%80%90K3s%E8%B8%A9%E5%9D%91%E8%AE%B0%E5%BD%95%E3%80%911-%E9%9B%86%E7%BE%A4%E6%90%AD%E5%BB%BA%2F)

### 下载安装包

分别下载安装脚本`install.sh`、二进制文件`k3s`、必要的镜像包`k3s-airgap-images-amd64.tar.gz`
直接导入到`~`目录下

[github.com/k3s-io/k3s](https://link.juejin.cn/?target=https%3A%2F%2Fgithub.com%2Fk3s-io%2Fk3s)

![image.png](https://p9-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/4d88d2a6da724a4f8067de1f4dadc75e~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5LiA5Liq5LiN5Lya6YeN5aSN55qEaWQ=:q75.awebp?rk3s=f64ab15b&x-expires=1742717246&x-signature=Yv0eYg5%2BUkdXDD1%2Ful7f0F6BH5g%3D)

[github.com/k3s-io/k3s/…](https://link.juejin.cn/?target=https%3A%2F%2Fgithub.com%2Fk3s-io%2Fk3s%2Freleases)

![image.png](https://p9-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/403eba63f1fe4b5ab5b58400a4db437a~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5LiA5Liq5LiN5Lya6YeN5aSN55qEaWQ=:q75.awebp?rk3s=f64ab15b&x-expires=1742717246&x-signature=9uS%2BCe%2B1%2FhG5y9DX2N7loMUTVbM%3D)

### 执行安装前的准备

- 将`k3s`二进制文件移动到`/usr/local/bin`目录，并添加执行权限

  ```BASH
  BASH代码解读复制代码mv k3s /usr/local/bin
  chmod +x /usr/local/bin/k3s
  ```

- 将镜像移动到`/var/lib/rancher/k3s/agent/images/`目录（无需解压）

  ```BASH
  BASH代码解读复制代码mkdir -p /var/lib/rancher/k3s/agent/images/
  cp ./k3s-airgap-images-amd64.tar.gz /var/lib/rancher/k3s/agent/images/
  ```

- 添加执行权限

  ```BASH
  BASH
  
  代码解读
  复制代码chmod +x install.sh
  ```

### 克隆虚拟机

- 将当前准备好的虚拟机（假定为master）克隆两个worker，最好打个快照

- 克隆的两个worker节点重新生成MAC地址

- 给所有节点重新设置hostname

  ```BASH
  BASH
  
  代码解读
  复制代码hostnamectl set-hostname <newhostname>
  ```

### 执行安装脚本

- master节点执行

  ```BASH
  BASH代码解读复制代码
  
  # 离线安装
  INSTALL_K3S_SKIP_DOWNLOAD=true ./install.sh
  # 安装完成后，查看节点状态
  kubectl get node
  # 查看token
  cat /var/lib/rancher/k3s/server/node-token
  # 复制得到的token
  # 监测节点情况
  watch -n 1 kubectl get node
  ```

- worker节点执行

  ```BASH
  BASH代码解读复制代码
  
  
  INSTALL_K3S_SKIP_DOWNLOAD=true \
  K3S_URL=https://192.168.6.170:6443 \
  K3S_TOKEN=xxx \
  ./install.sh
  ```

K3S_URL 是主节点ip，K3S_TOKEN是上面查看token全部拷贝进来

![image.png](https://p9-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/02a3867a843c4e2688ceefac03e27692~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5LiA5Liq5LiN5Lya6YeN5aSN55qEaWQ=:q75.awebp?rk3s=f64ab15b&x-expires=1742717246&x-signature=b5g4nAy8IosS72cCDto38Dr9jMw%3D)

- 此时master节点应该可以监测到

  ```css
  css代码解读复制代码NAME          STATUS   ROLES                  AGE    VERSION
  k8s-master    Ready    control-plane,master   xmxs   v1.30.3+k3s1
  k8s-worker1   Ready    <none>                 xmxs   v1.30.3+k3s1
  k8s-worker2   Ready    <none>                 xmxs   v1.30.3+k3s1
  ```

## 方式二：docker + 手动部署镜像方式

参考 [sheep-in-box.github.io/2024/08/08/…](https://link.juejin.cn/?target=https%3A%2F%2Fsheep-in-box.github.io%2F2024%2F08%2F08%2F%E3%80%90K3s%E8%B8%A9%E5%9D%91%E8%AE%B0%E5%BD%95%E3%80%911-%E9%9B%86%E7%BE%A4%E6%90%AD%E5%BB%BA%2F)

### 下载安装包

分别下载安装脚本`install.sh`、二进制文件`k3s`、必要的镜像包`k3s-airgap-images-amd64.tar.gz`
直接导入到`~`目录下

[github.com/k3s-io/k3s](https://link.juejin.cn/?target=https%3A%2F%2Fgithub.com%2Fk3s-io%2Fk3s)

![image.png](https://p9-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/4d88d2a6da724a4f8067de1f4dadc75e~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5LiA5Liq5LiN5Lya6YeN5aSN55qEaWQ=:q75.awebp?rk3s=f64ab15b&x-expires=1742717246&x-signature=Yv0eYg5%2BUkdXDD1%2Ful7f0F6BH5g%3D)

[github.com/k3s-io/k3s/…](https://link.juejin.cn/?target=https%3A%2F%2Fgithub.com%2Fk3s-io%2Fk3s%2Freleases)

![image.png](https://p9-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/403eba63f1fe4b5ab5b58400a4db437a~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5LiA5Liq5LiN5Lya6YeN5aSN55qEaWQ=:q75.awebp?rk3s=f64ab15b&x-expires=1742717246&x-signature=9uS%2BCe%2B1%2FhG5y9DX2N7loMUTVbM%3D)

### 执行安装前的准备

- 将`k3s`二进制文件移动到`/usr/local/bin`目录，并添加执行权限

  ```BASH
  BASH代码解读复制代码
  
  mv k3s /usr/local/bin
  chmod +x /usr/local/bin/k3s
  ```

- 将镜像移动到`/var/lib/rancher/k3s/agent/images/`目录（无需解压）

  ```BASH
  BASH代码解读复制代码
  
  mkdir -p /var/lib/rancher/k3s/agent/images/
  cp ./k3s-airgap-images-amd64.tar.gz /var/lib/rancher/k3s/agent/images/
  ```

- 添加执行权限

  ```BASH
  BASH
  
  代码解读
  复制代码chmod +x install.sh
  ```

### 克隆虚拟机

- 将当前准备好的虚拟机（假定为master）克隆两个worker，最好打个快照

- 克隆的两个worker节点重新生成MAC地址

- 给所有节点重新设置hostname

  ```BASH
  BASH
  
  代码解读
  复制代码hostnamectl set-hostname <newhostname>
  ```

### 执行安装脚本

与containerd不同的就是第一句，docker需要手动load需要的镜像；containerd会自动导入镜像。

- master节点执行

  ```BASH
  BASH代码解读复制代码
  
  # 手动docker load导入镜像
  gunzip -c k3s-airgap-images-amd64.tar.gz | docker load
  # 离线安装
  INSTALL_K3S_SKIP_DOWNLOAD=true INSTALL_K3S_EXEC='--docker' ./install.sh
  # 安装完成后，查看节点状态
  kubectl get node
  # 查看token
  cat /var/lib/rancher/k3s/server/node-token
  # 复制得到的token
  # 监测节点情况
  watch -n 1 kubectl get node
  ```

- worker节点执行

  ```BASH
  BASH代码解读复制代码
  
  INSTALL_K3S_SKIP_DOWNLOAD=true \
  K3S_URL=https://192.168.6.170:6443 \
  K3S_TOKEN=xxx \
  ./install.sh
  ```

K3S_URL 是主节点ip，K3S_TOKEN是上面查看token全部拷贝进来

![image.png](https://p9-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/02a3867a843c4e2688ceefac03e27692~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5LiA5Liq5LiN5Lya6YeN5aSN55qEaWQ=:q75.awebp?rk3s=f64ab15b&x-expires=1742717246&x-signature=b5g4nAy8IosS72cCDto38Dr9jMw%3D)

- 此时master节点应该可以监测到

  ```css
  css代码解读复制代码NAME          STATUS   ROLES                  AGE    VERSION
  k8s-master    Ready    control-plane,master   xmxs   v1.30.3+k3s1
  k8s-worker1   Ready    <none>                 xmxs   v1.30.3+k3s1
  k8s-worker2   Ready    <none>                 xmxs   v1.30.3+k3s1
  ```

## 方式三： docker + 国内在线安装

推荐官网文档 [docs.rancher.cn/docs/k3s/ad…](https://link.juejin.cn/?target=https%3A%2F%2Fdocs.rancher.cn%2Fdocs%2Fk3s%2Fadvanced%2F_index%23%E4%BD%BF%E7%94%A8-docker-%E4%BD%9C%E4%B8%BA%E5%AE%B9%E5%99%A8%E8%BF%90%E8%A1%8C%E6%97%B6)

### 安装docker

```swift
swift代码解读复制代码

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

### 安装k3s主节点

网络问题可能失败，所以失败就再执行这句，为什么不用默认的containerd呢，因为用不了，所以后面参数`--docker`用docker了。

国内镜像地址参考 [forums.rancher.cn/t/k3s/3314/…](https://link.juejin.cn/?target=https%3A%2F%2Fforums.rancher.cn%2Ft%2Fk3s%2F3314%2F4)

改为docker参考 [blog.csdn.net/wenyichuan/…](https://link.juejin.cn/?target=https%3A%2F%2Fblog.csdn.net%2Fwenyichuan%2Farticle%2Fdetails%2F107088681)

```ini
ini代码解读复制代码curl -sfL https://rancher-mirror.rancher.cn/k3s/k3s-install.sh | \
  INSTALL_K3S_MIRROR=cn \
  K3S_TOKEN=12345 sh -s - --docker \
  --system-default-registry=registry.cn-hangzhou.aliyuncs.com
```

失败了就再执行一遍，都是网络问题

![image.png](https://p9-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/6a8fe21548a649ceae952314ec8c32fd~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5LiA5Liq5LiN5Lya6YeN5aSN55qEaWQ=:q75.awebp?rk3s=f64ab15b&x-expires=1742717246&x-signature=brpKeJeA1HHc%2FJlsSiACSw95GMU%3D)

### 检查安装成功

后面会出现docker和版本号，就表示docker正常了

```arduino
arduino

代码解读
复制代码kubectl get node -o wide
```

![image.png](https://p9-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/7977dfbdfb9147918e7d3eb0d6aa171a~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5LiA5Liq5LiN5Lya6YeN5aSN55qEaWQ=:q75.awebp?rk3s=f64ab15b&x-expires=1742717246&x-signature=54GGrIBVT3Cb1Ff2zzJ1PeM843g%3D)

后面部署是参考 [www.cnblogs.com/voipman/p/1…](https://link.juejin.cn/?target=https%3A%2F%2Fwww.cnblogs.com%2Fvoipman%2Fp%2F15378589.html)

## 坑点

### 【非必须处理】worker节点无法使用`kubectl`命令

- 跟着做到这一步发现，master节点可以使用`kubectl`，但是worker节点会报错

  ```yaml
  yaml代码解读复制代码W0206 03:45:01.740148    9354 loader.go:222]Config not found: /etc/rancher/k3s/k3s.yaml
  E0206 03:45:01.741036    9354 memcache.go:238] couldn't get current server APl group list: Get http://localhost:8080/api?timeout-32s dial tcp 127.0.0.1:8080:connect: connection refused
  E0206 03:45:01.741740 9354 memcache.go:238] couldn't get current server APl group list: Get http://localhost:8080/api?timeout-32s dial tcp 127.0.0.1:8080:connect: connection refused
  E0206 03:45:01.743821 9354 memcache.go:238] couldn't get current server APl group list: Get http://localhost:8080/api?timeout-32s dial tcp 127.0.0.1:8080:connect: connection refused
  E0206 03:45:01.745916 9354 memcache.go:238] couldn't get current server APl group list: Get http://localhost:8080/api?timeout-32s dial tcp 127.0.0.1:8080:connect: connection refused
  E0206 03:45:01.747884 9354 memcache.go:238] couldn't get current server APl group list: Get http://localhost:8080/api?timeout-32s dial tcp 127.0.0.1:8080:connect: connection refused
  The connection to the server localhost:8080 was refused - did you specify the right host or port?
  ```

- 一开始网上搜索还以为是部署错误，后来才知道原来是正常的，是由于没有集群密钥。如果需要在agent节点运行`kubectl`命令，那么执行以下操作

  ```BASH
  BASH代码解读复制代码mkdir ~/.kube  
  scp 192.168.6.170:/etc/rancher/k3s/k3s.yaml ~/.kube/config
  ```

- 然后替换config中的server ip地址

  ```BASH
  BASH代码解读复制代码vi ~/.kube/config
  # server: https://192.168.6.170:6443
  ```

- 至此，就可以在worker节点运行`kubectl`命令了

### 【必须】配置镜像源（大坑）

- 配置镜像地址，国内访问不到docker.io拉去镜像，不然会一直失败，应该是新建`/etc/rancher/k3s/registries.yaml`，写入这个配置文件来配置镜像源（如果没有这个路径就创建）

  ```BASH
  BASH代码解读复制代码mkdir -p /etc/rancher/k3s
  vi /etc/rancher/k3s/registries.yaml
  ```

- 以下是`registries.yaml`参考，里面的镜像源目前可以用，但是不能保证不过时

  ```YAML
  YAML代码解读复制代码mirrors:
    docker.io:
      endpoint:
        - "https://docker.linkedbus.com"
        - "https://dockerpull.org"
        - "https://docker.xuanyuan.me"
        - "https://registry.cn-hangzhou.aliyuncs.com/"
        - "https://registry.dockermirror.com"
        - "https://docker.m.daocloud.io"
    quay.io:
      endpoint:
        - "https://quay.m.daocloud.io"
    registry.k8s.io:
      endpoint:
        - "https://k8s.m.daocloud.io"
    gcr.io:
      endpoint:
        - "https://gcr.m.daocloud.io/"
    k8s.gcr.io:
      endpoint:
        - "https://k8s-gcr.m.daocloud.io"
    ghcr.io:
      endpoint:
        - "https://ghcr.m.daocloud.io"
  ```

- 另外，不止是master节点需要进行配置，worker节点也需要，网上搜索的结果是worker节点会从master获取镜像源，似乎也是不对的！创建pod进行镜像拉取时，默认会在pod所创建的worker节点上进行拉取，也就会使用worker节点上的镜像源配置

- 重启每个节点

  ```arduino
  arduino代码解读复制代码# master
  systemctl restart k3s
  # worker
  systemctl restart k3s-agent
  ```

### 【非必须处理】测试创建pod（坑）

- 创建一个nginx的pod试试看，在master节点上执行

  ```ini
  ini代码解读复制代码
  
  kubectl run mynginx --image=nginx
  # 查看Pod
  kubectl get pod
  # 描述
  kubectl describe pod mynginx
  # 查看Pod的运行日志
  kubectl logs mynginx
  ```

- 如果失败了，可能需要先在对应的worker节点上把镜像拉下来，再进行创建。如果失败有可能是因为创建pod的时候无限从网络拉取pod，而网络又不稳定，于是崩溃

  ```
  代码解读
  复制代码
  
  crictl pull nginx
  ```

- 你可能发现这样还是起不来，为什么呢？原来在于pod的拉取策略：`imagePullPolicy`。如果没有指定拉取策略，同时拉取镜像为`latest`或无标签（那也是latest），`imagePullPolicy`会自动设置为`Always`，意为永远都会从网络上pull，即使本地有`latest`的镜像（djw：这个b有点蠢嘛）。解决办法有两种，一种是创建镜像的时候指定事先下好的版本，一种是指定`imagePullPolicy`为`IfNotPresent`，也就是先判断是否在本地存在，如果有就不拉取。

  ```arduino
  arduino
  
  代码解读
  复制代码
  
  kubectl run mynginx --image=nginx --image-pull-policy=IfNotPresent
  ```

## 部署应用和服务

### 新建部署配置文件

nginx-deployment.yaml

```yaml
yaml代码解读复制代码apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: nginx
  name: nginx-deployment1
  namespace: nginx
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - image: ccr.ccs.tencentyun.com/rootegg/nginx:1.27.2
        ports:
        - containerPort: 80
        name: nginx
      tolerations:
      - key: "key"
        operator: "Equal"
        value: "nginx"
        effect: "NoSchedule"
```

### 在k3s中运行nginx容器

```csharp
csharp代码解读复制代码# 建nginx命名空间
kubectl create ns nginx
kubectl get namespaces

# 应用
kubectl create -f nginx-deployment.yaml

# 查看应用
kubectl describe deployment nginx -n nginx

# 查看pod
kubectl get pods -n nginx

# 查看pod详情
kubectl describe pod -n nginx
```

上面三句查看可以看到效果

![image.png](https://p9-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/754c48b647ea4c068372541067609512~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5LiA5Liq5LiN5Lya6YeN5aSN55qEaWQ=:q75.awebp?rk3s=f64ab15b&x-expires=1742717246&x-signature=TftA7%2BtJuhDU3%2FvhJ5s1gy%2F1BIA%3D)

![image.png](https://p9-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/7087046b64b541c3be60b1a068366ae8~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5LiA5Liq5LiN5Lya6YeN5aSN55qEaWQ=:q75.awebp?rk3s=f64ab15b&x-expires=1742717246&x-signature=6nU02eRBiUvibAuP2RQm8jVJWQM%3D)

![image.png](https://p9-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/9c5dcfb211bf4b61ab0f141b27ca5c2a~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5LiA5Liq5LiN5Lya6YeN5aSN55qEaWQ=:q75.awebp?rk3s=f64ab15b&x-expires=1742717246&x-signature=SZpI7786Bnqir3VP42CgJJf5maM%3D)

### 新建服务配置文件

nginx-service.yaml

```yaml
yaml代码解读复制代码apiVersion: v1
kind: Service
metadata:
  labels:
   app: nginx
  name: nginx-deployment1
  namespace: nginx
spec:
  ports:
  - port: 9000
    name: nginx-service80
    protocol: TCP
    targetPort: 80
    nodePort: 31090
  selector:
    app: nginx
  type: NodePort
```

### 新建服务

```csharp
csharp代码解读复制代码# 创建
kubectl create -f nginx-service.yaml

# 查看
kubectl get services -n nginx

# 查看详情
kubectl describe service -n nginx
```

最后访问 [xxxx.xxx:31090](https://link.juejin.cn/?target=http%3A%2F%2Fxxxx.xxx%3A31090) 成功

![image.png](https://p9-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/f18a1104591d4431ae9536e3aa63a16b~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5LiA5Liq5LiN5Lya6YeN5aSN55qEaWQ=:q75.awebp?rk3s=f64ab15b&x-expires=1742717246&x-signature=66sHr6a9Mxob0CaW2jkFD%2Fk3q9c%3D)

### 【备忘】删除部署

强制删除，如果遇到一直pull镜像可以删除

```sql
sql代码解读复制代码

kubectl delete deployment --all -n nginx
kubectl delete pod --all --force -n nginx
kubectl delete services --all --force -n nginx
```

