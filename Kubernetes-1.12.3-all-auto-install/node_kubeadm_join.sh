echo "--------修改hosts--------"
cat <<EOF >/etc/hosts
192.168.168.145 node-192-168-168-145
EOF

systemctl restart network
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
yum makecache fast && yum -y install docker-ce-18.06.1.ce

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
  ],
  "hosts":[
    "unix:///var/run/docker.sock",
    "tcp://0.0.0.0:2375"
  ],
  "graph": "/data/docker",
  "registry-mirrors": ["https://sqygw205.mirror.aliyuncs.com","http://docker.work.net"],
  "insecure-registries": ["192.168.119.212","docker.work.net"]
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

swapoff -a
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
echo "1" > /proc/sys/net/ipv4/ip_forward


# 下载k8s.1.12.3所需要的镜像列表
echo 'docker pull registry.cn-hangzhou.aliyuncs.com/google_containers/kube-proxy-amd64:v1.12.3
docker pull registry.cn-hangzhou.aliyuncs.com/google_containers/pause:3.1

docker tag registry.cn-hangzhou.aliyuncs.com/google_containers/pause:3.1 k8s.gcr.io/pause:3.1
docker tag registry.cn-hangzhou.aliyuncs.com/google_containers/kube-proxy-amd64:v1.12.3 k8s.gcr.io/kube-proxy:v1.12.3' > ~/down-images.sh

chmod +777 ~/down-images.sh
sh ~/down-images.sh

# 执行节点加入操作
# 示例： kubeadm join 192.168.119.212:6443 --token jrk73b.m6ly1m4pz5g7ymbm --discovery-token-ca-cert-hash sha256:18c361e1e5031ab1fb0c195b3dff6b2f3557c98db621cf34077afe66845e40ab
# 下面的join_token要替换与具体的主节点的token , 主节点执行命令：kubeadm token list 查看可用的token列表，主节点创建新token命令：kubeadm token create
kubeadm join 192.168.119.212:6443 --token join_token --discovery-token-ca-cert-hash sha256:18c361e1e5031ab1fb0c195b3dff6b2f3557c98db621cf34077afe66845e40ab



