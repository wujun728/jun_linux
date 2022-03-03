# [kubernetes 安装(全)](https://www.cnblogs.com/cainiaoit/p/8581123.html)

\#http://blog.csdn.net/zhuchuangang/article/details/76572157
\#https://kubernetes.io/docs/setup/independent/create-cluster-kubeadm/
\#所有机器
\#https://docs.docker.com/engine/installation/linux/docker-ce/centos/#install-using-the-repository
\#安装docker,安装的版本取决于kubernetes支持docker的版本
\#到这上面下载https://yum.dockerproject.org/repo/main/centos/7/Packages/
sudo systemctl start docker
\#测试。出现Hello from Docker!
sudo docker run hello-world

\#####################################

\##################################
\#https://coreos.com/etcd/docs/latest/
\#https://github.com/coreos/etcd/
\#安装etcd
\#准备
openssl genrsa -out IE.key 2048
openssl req -new -key IE.key -out IE.csr
openssl x509 -req -in IE.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out IE.crt -days 5000
openssl pkcs12 -export -clcerts -in IE.crt -inkey IE.key -out IE.p12
openssl genrsa -out IE.key 2048
openssl req -new -subj "/C=CN/ST=GuangDong/L=ShenZhen/O=system:masters/CN=admin" -key IE.key -out IE.csr
openssl x509 -req -in IE.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out IE.crt -days 5000
openssl pkcs12 -export -clcerts -in IE.crt -inkey IE.key -out IE.p12
\#配置服务
tar xf etcd.tar.gz
cd etcd
cp etcd etcdctl /usr/bin
cat << EOF > /usr/lib/systemd/system/etcd.service
[unit]
Description=Etcd Server
After=network.target

[Service]
Type=simple
WorkingDirectory=/var/lib/etcd/
EnvironmentFile=/etc/etcd/etcd.conf
ExecStart=/usr/bin/etcd $ETCD_CMD

[Install]
WantedBy=multi-user.target
EOF
cat << EOF > /etc/etcd/etcd.conf
ETCD_CMD="--listen-client-urls http://0.0.0.0:2379 --advertise-client-urls http://0.0.0.0:2379 "
EOF
systemctl daemon-reload
systemctl enable etcd.service
systemctl start etcd.service
systemctl status etcd.service
\#创建网络
etcdctl set /coreos.com/network/config '{ "Network":"10.1.0.0/16" }'
\#验证
etcdctl cluster-health







\#member 8e9e05c52164694d is healthy: got healthy result from http://localhost:2379
\###################################
\#准备
\#hosts
192.168.1.1 master
192.168.1.2 minion-1
192.168.1.3 minion-2
\#下载,并解压
https://github.com/kubernetes/kubernetes/releases/tag/v1.7.5
cd kubernetes
\#下载kubernetes-server-linux-amd64.tar.gz
sh cluster/get-kube-binaries.sh
cd server
tar xf kubernetes-server-linux-amd64.tar.gz
cd server/bin/
\#准备证书
mkdir ca
cd ca
openssl genrsa -out ca.key 2048
openssl req -x509 -new -nodes -key ca.key -subj "/C=CN/ST=GuangDong/L=ShenZhen/O=system:masters/CN=test.com" -days 5000 -out ca.crt
openssl genrsa -out server.key 2048
\#配置master_ssl.cnf
cat << EOF > master_ssl.cnf
[req]
req_extensions = v3_req
distinguished_name = req_distinguished_name
[req_distinguished_name]
[ v3_req ]
basicConstraints= CA:FALSE
keyUsage = nonRepudiation, digitalSignature, keyEncipherment
subjectAltName= @alt_names
[alt_names]
DNS.1 = kubernetes
DNS.2 = kubernetes.default
DNS.3 = kubernetes.default.svc
DNS.4 = kubernetes.default.svc.cluster.local
DNS.5 = master
IP.1 = 169.169.0.1
IP.2 = 192.168.1.1
EOF
openssl req -new -key server.key -subj "/C=CN/ST=GuangDong/L=ShenZhen/O=system:masters/CN=master" -config master_ssl.cnf -out server.csr
openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -days 5000 -extensions v3_req -extfile master_ssl.cnf -out server.crt
\#全部执行完有6个文件复制到一个路径(如：/etc/kubernetes/crt/)
\#设置kube-controller-manager证书
openssl genrsa -out cs_client.key 2048
openssl req -new -key cs_client.key -subj "/C=CN/ST=GuangDong/L=ShenZhen/O=system:masters/CN=master" -out cs_client.csr
openssl x509 -req -in cs_client.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out cs_client.crt -days 5000
\#创建kubeconfig文件
cat << EOF > /etc/kubernetes/kubeconfig
apiVersion: v1
kind: Config
users:
\- name: controllermanager
 user:
  client-certificate: /etc/kubernetes/crt/cs_client.crt
  client-key: /etc/kubernetes/crt/cs_client.key
clusters:
\- name: local
 cluster:
  certificate-authority: /etc/kubernetes/crt/ca.crt
contexts:
\- context:
  cluster: local
  user: controllermanager
 name: my-context
current-context: my-context
EOF

\###################################
\#安装kube-apiserver
cp ../kube-apiserver /usr/bin
cat << EOF > /usr/lib/systemd/system/kube-apiserver.service
[Unit]
Description=Kubernetes API Server
Documentation=https://github.com/GoogleCloudPlatform/kubernetes
After=etcd.service
Wants=etcd.service

[Service]
EnvironmentFile=/etc/kubernetes/apiserver
ExecStart=/usr/bin/kube-apiserver $KUBE_API_ARGS
Restart=on-failure
Type=notify
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target
EOF

\#配置文件
cat << EOF > /etc/kubernetes/apiserver
KUBE_API_ARGS="--etcd_servers=http://127.0.0.1:2379 --insecure-bind-address=0.0.0.0 \
--service-cluster-ip-range=169.169.0.0/16 \
--service-node-port-range=1-65535 \
--admission-control=NamespaceLifecycle,LimitRanger,SecurityContextDeny,ServiceAccount,ResourceQuota \
--logtostderr=false --log-dir=/var/log/kubernetes --v=2 \
--client_ca_file=/etc/kubernetes/crt/ca.crt \
--tls-private-key-file=/etc/kubernetes/crt/server.key \
--tls-cert-file=/etc/kubernetes/crt/server.crt \
--insecure-port=0 \
--secure-port=8080"
EOF

\######################################
\#安装kube-controller-manager
cp ../kube-controller-manager /usr/bin
cat << EOF > /usr/lib/systemd/system/kube-controller-manager.service
[Unit]
Description=Kubernetes Controller Manager
Documentation=https://github.com/GoogleCloudPlatform/kubernetes
After=kube-apiserver.service
Requires=kube-apiserver.service

[Service]
EnvironmentFile=/etc/kubernetes/controller-manager
ExecStart=/usr/bin/kube-controller-manager $KUBE_CONTROLLER_MANAGER_ARGS
Restart=on-failure
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target
EOF
\#配置
cat << EOF >/etc/kubernetes/controller-manager
KUBE_CONTROLLER_MANAGER_ARGS="--master=https://192.168.1.1:8080 --logtostderr=false --log-dir=/var/log/kubernetes --v=2 --service_account_private_key_file=/etc/kubernetes/crt/server.key --root-ca-file=/etc/kubernetes/crt/ca.crt --kubeconfig=/etc/kubernetes/kubeconfig"
EOF

\##########################################
\#安装kube-scheduler
cp ../kube-scheduler /usr/bin
cat << EOF > /usr/lib/systemd/system/kube-scheduler.service
[Unit]
Description=Kubernetes Scheduler
Documentation=https://github.com/GoogleCloudPlatform/kubernetes
After=kube-apiserver.service
Requires=kube-apiserver.service

[Service]
EnvironmentFile=/etc/kubernetes/scheduler
ExecStart=/usr/bin/kube-scheduler $KUBE_SCHEDULER_ARGS
Restart=on-failure
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target
EOF
\#配置
cat << EOF > /etc/kubernetes/scheduler
KUBE_SCHEDULER_ARGS="--master=https://192.168.1.1:8080 --logtostderr=false \
--log-dir=/var/log/kubernetes --v=2 \
--kubeconfig=/etc/kubernetes/kubeconfig \
--service-cluster-ip-range=169.169.0.0/16"
EOF

\#启动
systemctl daemon-reload
service="kube-apiserver kube-apiserver kube-scheduler"
for i in $service
do
   systemctl enable $i
   systemctl restart $i
   systemctl status $i
done

\############################################
\#配置节点
\#准备
\#https://github.com/kubernetes/kubernetes/releases/tag/v1.7.5
\#下载kubernetes-server-linux-amd64.tar.gz
cd kubernetes
sh cluster/get-kube-binaries.sh
cd server
tar xf kubernetes-server-linux-amd64.tar.gz
cd server/bin/
\#创建证书
mkdir ca
cd ca
\#将master的ca.crt和ca.key复制到节点上
openssl genrsa -out kubelet_client.key 2048
openssl req -new -key kubelet_client.key -subj "/C=CN/ST=GuangDong/L=ShenZhen/O=system:masters/CN=218.71.143.140" -out kubelet_client.csr
openssl x509 -req -in kubelet_client.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out kubelet_client.crt -days 5000
\#创建kubeconfig文件
cat << EOF > /etc/kubernetes/kubeconfig
apiVersion: v1
kind: Config
users:
\- name: kubelet
 user:
  client-certificate: /etc/kubernetes/crt/kubelet_client.crt
  client-key: /etc/kubernetes/crt/kubelet_client.key
clusters:
\- name: local
 cluster:
  certificate-authority: /etc/kubernetes/crt/ca.crt
contexts:
\- context:
  cluster: local
  user: kubelet
 name: my-context
current-context: my-context
EOF

\################################
\#安装kubelet
cp ../kubelet /usr/bin/
cat << EOF > /usr/lib/systemd/system/kubelet.service
[Unit]
Description=Kubernetes Kubelet Server
Documentation=https://github.com/GoogleCloudPlatform/kubernetes
After=docker.service
Requires=docker.service

[Service]
WorkingDirectory=/var/lib/kubelet
EnvironmentFile=/etc/kubernetes/kubelet
ExecStart=/usr/bin/kubelet $KUBELET_ARGS
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF
cat << EOF >/etc/kubernetes/kubelet
KUBELET_ARGS="--api-servers=https://192.168.1.1:8080 --hostname-override=minion-2 --logtostderr=false \
--log-dir=/var/log/kubernetes --v=2 \
--kubeconfig=/etc/kubernetes/kubeconfig \
--root-dir=/data/kubelet \
--cluster-dns=169.169.0.10"
EOF

\#安装kube-proxy
cp ../kube-proxy /usr/bin
cat << EOF >/usr/lib/systemd/system/kube-proxy.service
[Unit]
Description=Kubernetes Kube Proxy Server
Documentation=https://github.com/GoogleCloudPlatform/kubernetes
After=network.target
Requires=network.service

[Service]
EnvironmentFile=/etc/kubernetes/proxy
ExecStart=/usr/bin/kube-proxy $KUBE_PROXY_ARGS
Restart=on-failure
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target
EOF
cat << EOF >/etc/kubernetes/proxy
KUBE_PROXY_ARGS="--master=https://192.168.1.1:8080 \
--logtostderr=false --log-dir=/var/log/kubernetes --v=2 \
--kubeconfig=/etc/kubernetes/kubeconfig \
--cluster-cidr=169.169.0.0/16"
EOF
\#启动
systemctl daemon-reload
service="kubelet.service kube-proxy.service"
for i in $service
do
systemctl enable $i
systemctl restart $i
systemctl status $i
done

\#flannel
\#所有master和node都安装
\#下载https://github.com/coreos/flannel/releases
\#解压并把flanneld和mk-codker-opts.sh复制到/usr/bin
\#配置服务
cp mk-docker-opts.sh flanneld /usr/bin/
cat << EOF > /usr/lib/systemd/system/flanneld.service
[Unit]
Description=flanneld overlay address etcd agent
After=network.target
Before=docker.service

[Service]
Type=notify
EnvironmentFile=/etc/sysconfig/flannel
ExecStart=/usr/bin/flanneld -etcd-endpoints=${FLANNEL_ETCD} $FLANNEL_OPTIONS

[Install]
RequiredBy=docker.service
WantedBy=multi-user.target
EOF
\#创建文件
cat << EOF > /etc/sysconfig/flannel
FLANNEL_ETCD="http://192.168.1.1:2379"
FLANNEL_ETCD_KEY="/coreos.com/network"
EOF
\#停止docker
systemctl daemon-reload
systemctl stop docker
systemctl start flanneld
\#替换docker ip
mk-docker-opts.sh -i
source /run/flannel/subnet.env
ifconfig docker0 ${FLANNEL_SUBNET}
\#修改docker
mk-docker-opts.sh -d /etc/docker/docker_opts.env -c
\#/usr/lib/systemd/system/docker.service
   \#修改，修改了存储目录和启动方式
   ExecStart=/usr/bin/dockerd $DOCKER_OPTS --graph=/data/docker
   \#新增
   EnvironmentFile=/etc/docker/docker_opts.env
\#验证
ip addr
\#启动docker
systemctl daemon-reload
systemctl restart docker
\#etcd验证
etcdctl ls /coreos.com/network/subnets
\#ping验证，通过etcd查看到的网段
ping 10.1.50.1
ping 10.1.46.1
\#docker禁止了转发，导致创建的pod无法跨主机互通
iptables -P FORWARD ACCEPT



\######################################
\#生成windows证书,将生成的证书IE.p12导入到IE个人证书
\#http://www.jianshu.com/p/045f95c008a0
openssl genrsa -out IE.key 2048
openssl req -new -subj "/C=CN/ST=GuangDong/L=ShenZhen/O=system:masters/CN=admin" -key IE.key -out IE.csr
openssl x509 -req -in IE.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out IE.crt -days 5000
openssl pkcs12 -export -clcerts -in IE.crt -inkey IE.key -out IE.p12


\##################################
\#UI
\#下载配置
wget https://rawgit.com/kubernetes/dashboard/master/src/deploy/kubernetes-dashboard.yaml
kubectl create -f kubernetes-dashboard.yaml
\#查看安装状态
kubectl get pods --all-namespaces
\#访问,将前面的IE证书导入
https://master.abc.com/ui

\##################################
\#DNS
\#cd kubernetes/cluster/addons/dns
\#修改transforms2sed.sed里的$DNS_SERVER_IP和$DNS_DOMAIN替换成169.169.0.10,和cluster.local
\#生成yuml文件
sed -e 'a/$DNS_SERVER_IP/169.169.0.10/g' -e 's/$DNS_DOMAIN/cluster.local/g' transforms2sed.sed
sed -f transforms2sed.sed kubedns-svc.yaml.base > kubedns-svc.yaml
sed -f transforms2sed.sed kubedns-controller.yaml.base > kubedns-controller.yaml
kubectl create -f ../dns
\#DNS自动扩容
kubectl create -f ../dns-horizontal-autoscaler/dns-horizontal-autoscaler.yaml
\#验证,可在UI上查看也可执行
kubectl get pods --all-namespaces

\####################################
\#监控工具
\#当前最新版本 heapster https://github.com/kubernetes/heapster/archive/v1.5.0-beta.0.tar.gz
\#修改 influxdb/grafana.yaml
\#删除
    \- name: GF_AUTH_BASIC_ENABLED
     value: "false"
    \- name: GF_AUTH_ANONYMOUS_ORG_ROLE
     value: Admin
\#修改,开启认证
    \- name: GF_AUTH_ANONYMOUS_ENABLED
     value: "false"
\#修改
 type: NodePort
 ports:
 \- port: 80
  targetPort: 3000
  nodePort: 3001
\#修改influxdb/heapster.yaml
\- --source=kubernetes:https://kubernetes.default.svc.cluster.local
\- --sink=influxdb:http://monitoring-influxdb.kube-system.svc.cluster.local:8086
\#创建
kubectl create -f deploy/kube-config/influxdb/
kubectl create -f deploy/kube-config/rbac/heapster-rbac.yaml
\#访问
kubernetes-dashboard 也可以看到等一会出现图形了
http://nodeip:3001 账号密码admin,也可以查看

\############################################
\#docker环境修改,由于被墙了所以无法下载谷歌的软件,需要先下载到仓库或FQ
\#或者直接到服务器上使用FQ软件
\#将修改版的FQ软件上传到服务器
\#3128FQ软件的端口
iptables -A INPUT -s 127.0.0.1 -p tcp --dport '3128' -j ACCEPT
iptables -A INPUT -p tcp --dport '3128' -j DROP
\#启动
\#修改启动参数
vi /usr/lib/systemd/system/docker.service
[Service]
Environment="HTTP_PROXY=http://127.0.0.1:3128"
ExecStart=/usr/bin/dockerd --insecure-registry gcr.io
systemctl daemon-reload
systemctl start docker.service
systemctl status docker.service

\##############################
\#kubectl 使用,存在~/.kube/config里,删除即可清空
kubectl config set-cluster default-cluster --server=https://master:8080 --certificate-authority=/etc/kubernetes/crt/ca.crt
kubectl config set-credentials default-admin --certificate-authority=/etc/kubernetes/crt/ca.crt --client-key=/etc/kubernetes/crt/cs_client.key --client-certificate=/etc/kubernetes/crt/cs_client.crt
kubectl config set-context default-system --cluster=default-cluster --user=default-admin
kubectl config use-context default-system
\#kubectl --server https://master:443 --certificate-authority /etc/kubernetes/crt/ca.crt --client-certificate /etc/kubernetes/crt/cs_client.crt --client-key /etc/kubernetes/crt/cs_client.key get nodes
kubectl get nodes

\############################################
\#所有节点
\#glusterfs
\#http://www.cnblogs.com/jicki/p/5801712.html
\#https://jimmysong.io/blogs/kubernetes-with-glusterfs/
yum install centos-release-gluster
yum install -y glusterfs glusterfs-server glusterfs-fuse glusterfs-rdma
\# 创建 glusterfs 目录
mkdir /data/glusterd
sed -i 's#var/lib#dara#g' /etc/glusterfs/glusterd.vol
\# 启动 glusterfs
systemctl start glusterd.service
\# 设置开机启动
systemctl enable glusterd.service
\#查看状态
systemctl status glusterd.service
\#开放端口,只对节点IP开放
ip=192.168.1.1,192.168.1.2,192.168.1.3
for i in $ip
do
   iptables -I INPUT -s $i -p tcp -m multiport --dport 24007,49152 -j ACCEPT
done

\#创建存储目录
mkdir /data/gfs_data
\#添加节点,在master主机上执行
gluster peer probe minion-1
gluster peer probe minion-2
\#查看状态
gluster peer status
\#允许所有
\#gluster volume reset disp_vol auth.allow
\#限制IP
gluster volume set disp_vol auth.allow 192.168.1.1,192.168.1.2,192.168.1.3
\#创建复制卷,副本数为3
gluster volume create test-volume replica 3 transport tcp master:/data/gfs_data minion-1:/data/gfs_data minion-2:/data/gfs_data
\#调优，缓存过大可能突然重启断电等情况导致数据丢失
\#启动卷
gluster volume start test-volume
\#查看卷状态
gluster volume info
\#设置配额
gluster volume quota test-volume enable
gluster volume quota test-volume limit-usage / 300GB
\#设置缓存
gluster volume set test-volume performance.cache-size 2GB
\#设置io线程
gluster volume set test-volume performance.io-thread-count 16
\#设置网络检测时间
gluster volume set test-volume network.ping-timeout 10
\#设置写缓冲大小
gluster volume set test-volume performance.write-behind-window-size 512MB
\#修改addresses ip每一个一组,port改为24007
\#kubectl apply更新
\#配置glusterfs节点ip和端口
kubectl apply -f ./kubernetes/examples/volumes/glusterfs/glusterfs-endpoints.json
\#配置集群端口
kubectl apply -f ./kubernetes/examples/volumes/glusterfs/glusterfs-service.json
\#kubectl apply -f demo.yum,添加了下面两段,挂载到/data目录,安装好demo.yaml后可df -h查看data目录是否挂载了300G
\#在yaml的containers里添加
"volumes": [
       "volumeMounts": [
         {
          "mountPath": "/data",
           "name": "glusterfdata"
         }
       ]
     }
\#在yaml的containers下面添加
"volumes": [
       {
         "name": "glusterfdata",
         "glusterfs": {
           "endpoints": "glusterfs-cluster",
           "path": "test-volume",
           "readOnly": false
         }
       }
     ],
\#也可直接挂载的物理主机
mount.glusterfs 192.168.1.1:/test-volume /data/mnt
\#创建pv
cat << EOF > glusterfs-pv.yaml
apiVersion: v1
kind: PersistentVolume
metadata:
 name: gluster-disk-1
spec:
 capacity:
  storage: 300Gi
 accessModes:
  \- ReadWriteMany
 glusterfs:
  endpoints: "glusterfs-cluster"
  path: "test-volume"
  readOnly: false
EOF
kubectl apply -f glusterfs-pv.yaml
kubectl get pv
\#创建PVC
cat << EOF>glusterfs-pvc.yaml
kind: PersistentVolumeClaim
apiVersion: v1
metadata:
 name: glusterfs-disk-1
spec:
 accessModes:
  \- ReadWriteMany
 resources:
  requests:
   storage: 300Gi
EOF
kubectl apply -f glusterfs-pvc.yaml
kubectl get pvc
kubect apply demo.yaml
\################################
\#运行centos镜像
\#运行命令填 /sbin/init,运行参数填2

\#######################################

\#错误
   error: failed to run Kubelet: failed to create kubelet: misconfiguration: kubelet cgroup driver: "systemd" is different from docker cgroup driver: "cgroupfs"
   \#检查docker
   docker info | grep Cgr
   \#修改/etc/systemd/system/kubelet.service.d/10-kubeadm.conf里的cgroup与docker的cgroup一致
   \#执行
   systemctl daemon-reload
   
   服务无法启动但是检查了配置都没问题
   \#手动启动服务，检查端口
   
可以使用如下的命令创建一个用于客户端认证的证书

openssl req
-new
-nodes \ -x509
-subj "/C=CN/ST=GuangDong/L=ShenZhen/O=HuaWei/OU=PaaS/CN=batman"
-days 3650
-keyout 私钥.key
-out 证书.crt

说明： /C 表示国家只能为两个字母的国家缩写，例如CN，US等 /ST 表示州或者省份 /L 表示城市或者地区 /O 表示组织机构名称 /OU 表示组织机构内的部门或者项目名称 /CN 表示公用名，如果用来作为SSL证书则应该填入域名或者子域名， 如果作为客户端认证证书则可以填入期望的用户名 为API Server指定要应用的客户端认证证书 将上一步创建的证书文件拷贝到API Server所在的主机，然后通过启动参数--client-ca-file将证书文件的路径传递给API Server。