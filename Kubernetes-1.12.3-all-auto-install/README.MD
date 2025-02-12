# Kubernetes-1.12.3-all-auto-install

### 项目介绍
个人整理的Centos7.x + Kubernetes-1.12.3 + Dashboard-1.8.3 无 CVE-2018-1002105 漏洞的master,node节点全自动快速一键安装部署文件，适用于测试环境，生产环境的快速安装部署

### 参考文档
https://kubernetes.io/docs/setup/independent/create-cluster-kubeadm/

## master节点安装准备工作

1. 配置好centos的网络环境，使其可连接互联网，用于下载安装文件
2. 用root用户登录centos7,复制本工程中的所有*.sh,*.ymal文件到/root/目录下
3. 修改*.sh的文件权限：

```
chmod +777 /root/*.sh
```
4. 执行以下命令，替换*.sh中的ip为你centos7的ip地址

```
# 修改替换下面的your_master_centos_ip为你的master_centos的ip
sed -i "s/192.168.119.212/your_master_centos_ip/g" /root/*.sh
```

## master节点安装教程

1. 执行node_kubeadm_init.sh,安装kubernetes 1.12.3环境

```
sh /root/node_kubeadm_init.sh
```

2. 执行node_kubeadm_install.sh,安装kubernetes-dashboard-1.8.3管理UI

```
sh /root/node_kubeadm_install.sh
```
3. 全部完成后，打开浏览器：访问 ：https://your_centos_ip:30001，使用token登录，token查看方法如下：


```
#执行命令，获取所有密钥列表：
kubectl -n kube-system get secret
#执行命令，获取指定key的token:
kubectl -n kube-system describe secret kubernetes-dashboard-admin-token-* #{上条命令输出的结果中复制的类似kubernetes-dashboard-admin-token-skhfh的key字符串到这里替换}
#复制token数据到登录框内登录即可登录
```

## -----------------------------------------------------------------------
## ---至此单节点的Kubernetes安装完成，如果要加入新节点，看下面
## -----------------------------------------------------------------------



## node节点加入准备工作

1. 配置好centos的网络环境，使其可连接互联网，用于下载安装文件
2. 用root用户登录centos7,复制本工程中的node_kubeadm_join.sh文件到/root/目录下
3. 修改*.sh的文件权限：

```
chmod +777 /root/*.sh
```
4. 执行以下命令，替换*.sh中的ip为你centos7的ip地址

```
# 修改替换下面的your_master_centos_ip为你的master_centos的ip
sed -i "s/192.168.119.212/your_master_centos_ip/g" /root/*.sh
# 修改替换下面的your_node_centos_ip为你的node_centos的ip
sed -i "s/192.168.168.145/your_node_centos_ip/g" /root/*.sh
# 修改替换下面的your_node_centos_host为你的node_centos的host,格式如：node-192-168-168-145,用ip值，将.替换为-
sed -i "s/node-192-168-168-145/your_node_centos_host/g" /root/*.sh
# 修改替换下面的your_join_token为master的加入token
# 查看master加入token方法：在master节点执行：kubectl token list,获取未过期的token
# 在master新建token方法：在master节点执行：kubectl create token
sed -i "s/join_token/your_join_token/g" /root/*.sh
```

## node节点加入教程

1. 执行node_kubeadm_join.sh,加入新节点

```
sh /root/node_kubeadm_join.sh
```
3. 全部完成后，打开浏览器：访问 ：https://your_master_centos_ip:30001，查看节点准备情况。节点准备需要一点时间。



