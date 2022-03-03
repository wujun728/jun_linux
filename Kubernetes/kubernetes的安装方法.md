## [kubernetes的安装方法](https://www.cnblogs.com/zhaojiedi1992/p/zhaojiedi_liunx_53_kubernates_install.html)

## 背景

自己学习k8s集群，无奈屌丝一枚，没钱配置vpn服务，安装k8s花费的时间太久了。为了小伙伴们可以快速安装k8s，我花了点时间整理了这篇博客，提供一个不用FQ就可以愉快安装k8s集群的方法。

## 主机环境

### 主机、IP规划和网络规划

| HOSTNAME | IP        |
| -------- | --------- |
| master   | 10.8.3.91 |
| node1    | 10.8.3.81 |
| node2    | 10.8.3.82 |

k8s的pod网络采用 10.244.0.0/16 ，网络组件选择flannel，k8s版本选择v1.11.3。

### 主机名设置

这里使用centos7的hostnamectl设置主机名字， centos其他版本参考： https://www.cnblogs.com/zhaojiedi1992/p/zhaojiedi_linux_043_hostname.html

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

```
#master节点
hostnamectl  set-hostname  master && exec bash 
#node1节点
hostnamectl  set-hostname  node1 && exec bash 
#node2节点
hostnamectl  set-hostname  node2 && exec bash 
```

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

### hosts文件设置

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

```
[root@master ~]# vim /etc/hosts 
# 添加如下3行 
10.4.3.91 master 
10.4.3.81 node1 
10.4.3.82 node2
# 其他的2个node节点也需要同样操作
```

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

### 防火墙和selinux设置

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

```
[root@master ~]# sed -i "s/^SELINUX\=enforcing/SELINUX\=disabled/g" /etc/selinux/config
[root@master ~]# setenforce 0 
setenforce: SELinux is disabled
[root@master ~]# systemctl stop firewalld 
[root@master ~]# systemctl disable firewalld
# 其他的2个node节点也需要同样操作
```

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

### 内核参数开启

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

```
[root@master k8s_images]# echo "net.bridge.bridge-nf-call-ip6tables = 1" >>/etc/sysctl.conf 
[root@master k8s_images]# echo "net.bridge.bridge-nf-call-iptables = 1" >> /etc/sysctl.conf
[root@master k8s_images]# echo "net.ipv4.ip_forward=1" >> /etc/sysctl.conf 
[root@master k8s_images]# sysctl -p
sysctl: cannot stat /proc/sys/net/bridge/bridge-nf-call-ip6tables: No such file or directory 
sysctl: cannot stat /proc/sys/net/bridge/bridge-nf-call-iptables: No such file or directory #加载模块
[root@master k8s_images]# modprobe br_netfilter
[root@master k8s_images]# echo "modprobe br_netfilter" >> /etc/rc.local
#再次重载下
[root@master k8s_images]# sysctl -p 
# 其他的2个node节点也需要同样操作
```

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

###  仓库准备

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

```
# 备份旧的repo[root@master ~]# cd /etc/yum.repos.d/
[root@master yum.repos.d]# ls
CentOS-Base.repo  CentOS-Debuginfo.repo  CentOS-Media.repo    CentOS-Vault.repo
CentOS-CR.repo    CentOS-fasttrack.repo  CentOS-Sources.repo
[root@master yum.repos.d]# mkdir bak
[root@master yum.repos.d]# mv *.repo bak
[root@master yum.repos.d]# ls
bak# 下载base,epel
[root@master yum.repos.d]# curl -o /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo
[root@master yum.repos.d]# wget -O /etc/yum.repos.d/epel.repo http://mirrors.aliyun.com/repo/epel-7.repo
# 下载k8s repo
[root@master yum.repos.d]# cat <<EOF > /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://mirrors.aliyun.com/kubernetes/yum/repos/kubernetes-el7-x86_64/
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://mirrors.aliyun.com/kubernetes/yum/doc/yum-key.gpg https://mirrors.aliyun.com/kubernetes/yum/doc/rpm-package-key.gpg
EOF
# 其他的2个node节点也需要同样操作
```

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

## 安装k8s

### docker和k8s软件安装

```
[root@master yum.repos.d]# yum install docker kubelet kubeadm kubectl
[root@master yum.repos.d]# systemctl enable docker && systemctl restart docker 
[root@master yum.repos.d]# systemctl enable kubelet && systemctl start kubelet  
# 其他的2个node节点也需要同样操作
```

### docker加速配置

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

```

sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json <<-'EOF'
{
  "registry-mirrors": ["https://mew8i5li.mirror.aliyuncs.com"]
}
EOF
sudo systemctl daemon-reload
sudo systemctl restart docker
# 其他的2个node节点也需要同样操作
```

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

### 曲线下载k8s所需的镜像

这个我是在dockerhub上面的自动构建，原理就是拉去构建的镜像，给这个镜像打tag为k8s.gcr.io的tag，这样我们在初始化集群的时候就不会再去国外拉取镜像文件。

我的dockerhub：[https://hub.docker.com/r/zhaojiedi1992](https://hub.docker.com/r/zhaojiedi1992/)

我的github仓库：https://github.com/zhaojiedi1992/k8s_images

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

```
[root@master ~]# cd /root
[root@master ~]# mkdir git
[root@master ~]# cd git/
[root@master git]# git clone https://github.com/zhaojiedi1992/k8s_images.git
[root@master git]# cd k8s_images/
[root@master k8s_images]# ls
create_script.sh                      pull_image_from_dockerhub_v1.10.6.sh  README.md  v1.10.6
pull_image_from_dockerhub.template    pull_image_from_dockerhub_v1.10.7.sh  tmp.txt    v1.10.7
pull_image_from_dockerhub_v1.10.0.sh  pull_image_from_dockerhub_v1.10.8.sh  v1.10.0    v1.10.8
pull_image_from_dockerhub_v1.10.1.sh  pull_image_from_dockerhub_v1.11.0.sh  v1.10.1    v1.11
pull_image_from_dockerhub_v1.10.2.sh  pull_image_from_dockerhub_v1.11.1.sh  v1.10.2    v1.11.0
pull_image_from_dockerhub_v1.10.3.sh  pull_image_from_dockerhub_v1.11.2.sh  v1.10.3    v1.11.1
pull_image_from_dockerhub_v1.10.4.sh  pull_image_from_dockerhub_v1.11.3.sh  v1.10.4    v1.11.2
pull_image_from_dockerhub_v1.10.5.sh  pull_image_from_dockerhub_v1.11.sh    v1.10.5    v1.11.3
[root@master k8s_images]# chmod a+x *.sh

# 查看安装的k8s版本对应需要的镜像
[root@master k8s_images]# kubeadm config images list --kubernetes-version=v1.11.3
k8s.gcr.io/kube-apiserver-amd64:v1.11.3
k8s.gcr.io/kube-controller-manager-amd64:v1.11.3
k8s.gcr.io/kube-scheduler-amd64:v1.11.3
k8s.gcr.io/kube-proxy-amd64:v1.11.3
k8s.gcr.io/pause:3.1
k8s.gcr.io/etcd-amd64:3.2.18
k8s.gcr.io/coredns:1.1.3

# 查看脚本的镜像和需要拉去的是否一致。
[root@master k8s_images]# cat ./pull_image_from_dockerhub_v1.11.3.sh 
#!/bin/bash
gcr_name=k8s.gcr.io
myhub_name=zhaojiedi1992
# define images 
images=(
    kube-apiserver-amd64:v1.11.3
    kube-controller-manager-amd64:v1.11.3
    kube-scheduler-amd64:v1.11.3
    kube-proxy-amd64:v1.11.3
    pause:3.1
    etcd-amd64:3.2.18
    coredns:1.1.3
)
for image in ${images[@]}; do 
    docker pull $myhub_name/$image
    docker tag $myhub_name/$image $gcr_name/$image
    docker rmi $myhub_name/$image
done

# 确认上面的无错误，开始下载。
[root@master k8s_images]# ./pull_image_from_dockerhub_v1.11.3.sh 
[root@master k8s_images]# docker image ls 
REPOSITORY TAG IMAGE ID CREATED SIZE
k8s.gcr.io/pause 3.1 24440bb35d05 About an hour ago 742 kB
k8s.gcr.io/kube-proxy-amd64 v1.11.3 763b3c45ccd2 4 hours ago 97.8 MB
k8s.gcr.io/kube-scheduler-amd64 v1.11.3 8434ffab1549 5 hours ago 56.8 MB
k8s.gcr.io/kube-controller-manager-amd64 v1.11.3 3b0d0349c534 5 hours ago 155 MB
k8s.gcr.io/kube-apiserver-amd64 v1.11.3 306b76250de9 6 hours ago 187 MB
k8s.gcr.io/coredns 1.1.3 6b777875393d 6 hours ago 45.6 MB
k8s.gcr.io/etcd-amd64 3.2.18 7dc1bb5c1af1 6 hours ago 219 MB
# 其他的2个node节点也需要同样操作
```

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

### 初始化k8s

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

```
[root@master k8s_images]#  kubeadm  init --pod-network-cidr=10.244.0.0/16 --kubernetes-version=v1.11.3
省略大量输出
Your Kubernetes master has initialized successfully!

To start using your cluster, you need to run the following as a regular user:

mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config

You should now deploy a pod network to the cluster.
Run "kubectl apply -f [podnetwork].yaml" with one of the options listed at:
https://kubernetes.io/docs/concepts/cluster-administration/addons/

You can now join any number of machines by running the following on each node
as root:

kubeadm join 10.4.3.91:6443 --token 1ccx3e.jwbm8pbaq1awiz2z --discovery-token-ca-cert-hash sha256:838517f2d09d04d8ab1d736466311e32db26d2c5a9286fec37204b2de7923a67
```

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

### 客户端设置

这里kubectl客户端的配置设置，我们直接设置到主节点上面来。

```
[root@master k8s_images]# mkdir -p $HOME/.kube
[root@master k8s_images]# sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
cp: overwrite ‘/root/.kube/config’? y
[root@master k8s_images]# sudo chown $(id -u):$(id -g) $HOME/.kube/config
[root@master k8s_images]# echo " kubeadm join 10.4.3.91:6443 --token 1ccx3e.jwbm8pbaq1awiz2z --discovery-token-ca-cert-hash sha256:838517f2d09d04d8ab1d736466311e32db26d2c5a9286fec37204b2de7923a67" >/root/k8s.json
```

### 安装flannel网络组件

```
[root@master k8s_images]# kubectl  apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
```

### node1加入集群

```
[root@node1 k8s_images]#  kubeadm join 10.4.3.91:6443 --token 1ccx3e.jwbm8pbaq1awiz2z --discovery-token-ca-cert-hash sha256:838517f2d09d04d8ab1d736466311e32db26d2c5a9286fec37204b2de7923a67 
```

这个命令来自与主节点初始化的时候的输出，上面已经保存到主节点的/root/k8s.json。

### 查看集群状态

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

```
[root@master k8s_images]# kubectl get nodes 
NAME      STATUS    ROLES     AGE       VERSION
master    Ready     master    17m       v1.11.3
node1     Ready     <none>    8m        v1.11.3
[root@master k8s_images]# kubectl get pod -n kube-system 
NAME                             READY     STATUS    RESTARTS   AGE
coredns-78fcdf6894-5zr25         1/1       Running   0          17m
coredns-78fcdf6894-82v6w         1/1       Running   0          17m
etcd-master                      1/1       Running   0          7m
kube-apiserver-master            1/1       Running   0          7m
kube-controller-manager-master   1/1       Running   0          7m
kube-flannel-ds-amd64-5s962      1/1       Running   0          4m
kube-flannel-ds-amd64-s2t5b      1/1       Running   0          4m
kube-proxy-ccvdd                 1/1       Running   0          17m
kube-proxy-p2fbl                 1/1       Running   0          8m
kube-scheduler-master            1/1       Running   0          7m
```

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

这个状态需要等一段时间才能全是Running。好了，k8s集群就安装完毕了。

更多k8s.io的镜像可以从[https://hub.docker.com/u/anjia0532/ ](https://hub.docker.com/u/anjia0532/ )这个地方找找。

标签: [k8s](https://www.cnblogs.com/zhaojiedi1992/tag/k8s/)