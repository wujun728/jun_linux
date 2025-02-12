cat <<EOF > /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=http://mirrors.aliyun.com/kubernetes/yum/repos/kubernetes-el7-x86_64
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=http://mirrors.aliyun.com/kubernetes/yum/doc/yum-key.gpg http://mirrors.aliyun.com/kubernetes/yum/doc/rpm-package-key.gpg
exclude=kube*
EOF

## Install prerequisites.
yum install -y yum-utils device-mapper-persistent-data lvm2 

## Add docker repository.
yum-config-manager -y --add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo

## Install docker.
yum clean all && yum makecache && yum -y install docker-ce-18.06.1.ce

## Create /etc/docker directory.
mkdir /etc/docker

# Setup daemon.
cat > /etc/docker/daemon.json <<EOF
{
  "exec-opts": ["native.cgroupdriver=systemd"],
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "100m"
  },
  "storage-driver": "overlay2",
  "storage-opts": [
    "overlay2.override_kernel_check=true"
  ]
}
{
  "graph": "/data/docker",
  "registry-mirrors": ["https://sqygw205.mirror.aliyuncs.com"]
}
EOF

mkdir -p /etc/systemd/system/docker.service.d

# Restart docker.
systemctl daemon-reload
systemctl enable docker
systemctl restart docker
systemctl status docker

systemctl disable firewalld
systemctl stop firewalld

# Set SELinux in permissive mode (effectively disabling it)
# 将 SELinux 设置为 permissive 模式(将其禁用)
setenforce 0
sed -i 's/^SELINUX=.*$/SELINUX=permissive/' /etc/selinux/config

yum install -y kubelet-1.12.3 kubeadm-1.12.3 kubectl-1.12.3 --disableexcludes=kubernetes

systemctl enable kubelet && systemctl start kubelet

cat <<EOF >  /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
EOF
sysctl --system

# 下载k8s.1.12.3所需要的镜像列表
echo 'docker pull registry.cn-hangzhou.aliyuncs.com/google_containers/kube-apiserver-amd64:v1.12.3
docker pull registry.cn-hangzhou.aliyuncs.com/google_containers/kube-controller-manager-amd64:v1.12.3
docker pull registry.cn-hangzhou.aliyuncs.com/google_containers/kube-scheduler-amd64:v1.12.3
docker pull registry.cn-hangzhou.aliyuncs.com/google_containers/kube-proxy-amd64:v1.12.3
docker pull registry.cn-hangzhou.aliyuncs.com/google_containers/etcd-amd64:3.2.24
docker pull registry.cn-hangzhou.aliyuncs.com/google_containers/pause:3.1
docker pull registry.cn-hangzhou.aliyuncs.com/google_containers/coredns:1.2.2
docker pull registry.cn-hangzhou.aliyuncs.com/google_containers/coredns:1.2.3
docker pull registry.cn-hangzhou.aliyuncs.com/google_containers/coredns:1.2.4

docker tag registry.cn-hangzhou.aliyuncs.com/google_containers/pause:3.1 k8s.gcr.io/pause:3.1
docker tag registry.cn-hangzhou.aliyuncs.com/google_containers/coredns:1.2.2 k8s.gcr.io/coredns:1.2.2
docker tag registry.cn-hangzhou.aliyuncs.com/google_containers/coredns:1.2.3 k8s.gcr.io/coredns:1.2.3
docker tag registry.cn-hangzhou.aliyuncs.com/google_containers/coredns:1.2.4 k8s.gcr.io/coredns:1.2.4
docker tag registry.cn-hangzhou.aliyuncs.com/google_containers/etcd-amd64:3.2.24 k8s.gcr.io/etcd:3.2.24
docker tag registry.cn-hangzhou.aliyuncs.com/google_containers/kube-scheduler-amd64:v1.12.3 k8s.gcr.io/kube-scheduler:v1.12.3
docker tag registry.cn-hangzhou.aliyuncs.com/google_containers/kube-controller-manager-amd64:v1.12.3 k8s.gcr.io/kube-controller-manager:v1.12.3
docker tag registry.cn-hangzhou.aliyuncs.com/google_containers/kube-apiserver-amd64:v1.12.3 k8s.gcr.io/kube-apiserver:v1.12.3
docker tag registry.cn-hangzhou.aliyuncs.com/google_containers/kube-proxy-amd64:v1.12.3 k8s.gcr.io/kube-proxy:v1.12.3' > ~/down-images.sh

chmod +777 ~/down-images.sh
sh ~/down-images.sh


sysctl net.bridge.bridge-nf-call-iptables=1
kubeadm init --kubernetes-version=1.12.3 --pod-network-cidr=10.244.0.0/16 --apiserver-advertise-address=192.168.119.212

mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
# 重要：必须安装一个pod网络附加扩展组件 ，我选择安装flanneld网络组件
kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
# 注意：备份类似以下格式的输出内容：用于节点加入使用
# kubeadm join 192.168.119.212:6443 --token qknvfe.v02ypyxnjvzjjzcs --discovery-token-ca-cert-hash sha256:18c361e1e5031ab1fb0c195b3dff6b2f3557c98db621cf34077afe66845e40ab
# 如生成的初始token无法使用，执行以下命令重新生成一个
# kubeadm token create --print-join-command
# 至此主节点k8s安装完成，你可以安装部署pod,或者其它扩展组件



