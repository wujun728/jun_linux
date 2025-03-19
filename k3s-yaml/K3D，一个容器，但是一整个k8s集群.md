# K3D，一个容器，但是一整个k8s集群

你可能需要一个快速启动和销毁的 k8s 集群；你可能在资源受限的环境中运行 k8s 集群；你可能是一个完全的初学者，觉得搭建完整的 k8s 套件太难。那么这篇短文可能可以帮到你。

## 各种丐版 k8s 集群

你可能见过各种丐版的 k8s 集群部署方案，比如：K3S、K3d、Kind、MicroK8S、Minikube、Docker Desktop。而今天要写的是其中之一：K3d。

为什么选择 k3d 呢，因为笔者在一个非常特殊的环境中使用 k8s：

1. 这是一个 x86 的 openwrt 软路由系统，已经内置了 docker。除了 k3d，其他的方案都因为各种原因而失败了。当然普通的 PC 以上方案都是可以的。而 k3d 几乎也是最简单的。
2. 笔者打算在这个软路由上安装自己平时要用到的各种中间件，比如 nexus oss、jenkins 等等 。
3. 考虑到这个环境可能需要做备份和重建，因此需要考虑一个快速启动和销毁的 k8s 集群。后续在加上 argo-cd 等技术，可以实现一个完整的 k8s 集群的备份和恢复。

## 使用 k3d 之前的准备

1. 你需要一个 docker 环境。（必要）

## 开始安装 k3d

方法 1，你可以选择使用官方提供的脚本进行安装：

```bash
bash

代码解读
复制代码wget -q -O - https://raw.githubusercontent.com/k3d-io/k3d/main/install.sh | bash
```

方法 2，你也可以直接下载二进制文件，然后加入到 PATH 即可：[github.com/k3d-io/k3d/…](https://link.juejin.cn/?target=https%3A%2F%2Fgithub.com%2Fk3d-io%2Fk3d%2Freleases)

如果从 github 下载对你的网络来说是一种困难，你可以选择 [k3d](https://link.juejin.cn/?target=https%3A%2F%2Fnewbe.pro%2FMirrors%2FMirrors-k3d%2F)[1](https://link.juejin.cn/?target=) 或者 [FastGithub](https://link.juejin.cn/?target=https%3A%2F%2Fnewbe.pro%2FMirrors%2FMirrors-FastGithub%2F)[2](https://link.juejin.cn/?target=)

## 创建一个 k3d.yml 文件

k3d.yml 是用户在创建 k3d 集群时使用的配置文件。这是一个范例的配置文件：

```yaml
yaml代码解读复制代码apiVersion: k3d.io/v1alpha4
kind: Simple
metadata:
  name: k3s-default
servers: 1 # same as `--servers 1`
agents: 2 # same as `--agents 2`
image: docker.io/rancher/k3s:v1.25.6-k3s1
kubeAPI: # same as `--api-port myhost.my.domain:6445` (where the name would resolve to 127.0.0.1)
  host: '127.0.0.1' # important for the `server` setting in the kubeconfig
  # hostIP: "192.168.1.200" # where the Kubernetes API will be listening on
  hostPort: '6445' # where the Kubernetes API listening port will be mapped to on your host system
ports:
  - port: 80:80 # same as `--port '8080:80@loadbalancer'`
    nodeFilters:
      - loadbalancer
options:
  k3d: # k3d runtime settings
    wait: true # wait for cluster to be usable before returining; same as `--wait` (default: true)
    timeout: '60s' # wait timeout before aborting; same as `--timeout 60s`
    disableLoadbalancer: false # same as `--no-lb`
    disableImageVolume: false # same as `--no-image-volume`
    disableRollback: false # same as `--no-Rollback`
    loadbalancer:
      configOverrides:
        - settings.workerConnections=2048
  k3s: # options passed on to K3s itself
    extraArgs: # additional arguments passed to the `k3s server|agent` command; same as `--k3s-arg`
      - arg: '--tls-san=127.0.0.1 --tls-san=ks.newbe.io'
        nodeFilters:
          - server:*
  kubeconfig:
    updateDefaultKubeconfig: true # add new cluster to your default Kubeconfig; same as `--kubeconfig-update-default` (default: true)
    switchCurrentContext: true # also set current-context to the new cluster's context; same as `--kubeconfig-switch-context` (default: true)
registries: # define how registries should be created or used
  config:
    | # define contents of the `registries.yaml` file (or reference a file); same as `--registry-config /path/to/config.yaml`
    mirrors:
      "docker.io":
        endpoint:
          - "https://mirror.ccs.tencentyun.com"
```

## 创建一个 k3d 集群

有了配置文件，现在就可以创建一个 k3d 集群了：

```lua
lua

代码解读
复制代码k3d cluster create --config k3d.yml
```

> **可发帖可群聊的技术交流方式已经上线，欢迎通过链接，加入我们一起讨论。 [www.newbe.pro/links/](https://link.juejin.cn/?target=https%3A%2F%2Fwww.newbe.pro%2Flinks%2F)**

运行结果大致如下：

```ini
ini代码解读复制代码root@OpenWrt:/mnt/sda1/workspace# ./k3d cluster create --config k3d.yml
INFO[0000] Using config file k3d.yml (k3d.io/v1alpha4#simple)
INFO[0000] portmapping '80:80' targets the loadbalancer: defaulting to [servers:*:proxy agents:*:proxy]
INFO[0000] Prep: Network
INFO[0000] Created network 'k3d-k3s-default'
INFO[0000] Created image volume k3d-k3s-default-images
INFO[0000] Starting new tools node...
INFO[0000] Starting Node 'k3d-k3s-default-tools'
INFO[0001] Creating node 'k3d-k3s-default-server-0'
INFO[0001] Creating node 'k3d-k3s-default-agent-0'
INFO[0001] Creating node 'k3d-k3s-default-agent-1'
INFO[0001] Creating LoadBalancer 'k3d-k3s-default-serverlb'
INFO[0001] Using the k3d-tools node to gather environment information
INFO[0001] HostIP: using network gateway 172.18.0.1 address
INFO[0001] Starting cluster 'k3s-default'
INFO[0001] Starting servers...
INFO[0001] Starting Node 'k3d-k3s-default-server-0'
INFO[0006] Starting agents...
INFO[0007] Starting Node 'k3d-k3s-default-agent-0'
INFO[0007] Starting Node 'k3d-k3s-default-agent-1'
INFO[0010] Starting helpers...
INFO[0010] Starting Node 'k3d-k3s-default-serverlb'
INFO[0017] Injecting records for hostAliases (incl. host.k3d.internal) and for 4 network members into CoreDNS configmap...
INFO[0019] Cluster 'k3s-default' created successfully!
INFO[0019] You can now use it like this:
kubectl cluster-info
```

这样我们就得到了一个 k3d 集群，其中包含了一个 master 节点和两个 worker 节点。

## 获取 kubeconfig

k3d 集群创建成功后，我们可以通过 k3d 命令获取 kubeconfig 文件：

```sql
sql

代码解读
复制代码k3d kubeconfig get --all
```

将 kubeconfig 配置好，就可以使用 kubectl 命令操作 k3d 集群了。

```arduino
arduino

代码解读
复制代码kubectl get nodes
scss代码解读复制代码NAME                       STATUS   ROLES                  AGE   VERSION
k3d-k3s-default-server-0   Ready    control-plane,master   38m   v1.25.6+k3s1
k3d-k3s-default-agent-1    Ready    <none>                 38m   v1.25.6+k3s1
k3d-k3s-default-agent-0    Ready    <none>                 38m   v1.25.6+k3s1
```

> **可发帖可群聊的技术交流方式已经上线，欢迎通过链接，加入我们一起讨论。 [www.newbe.pro/links/](https://link.juejin.cn/?target=https%3A%2F%2Fwww.newbe.pro%2Flinks%2F)**

## 部署一个应用

我们可以通过 kubectl 命令部署一个应用，比如 nginx：

```ini
ini代码解读复制代码kubectl create deployment nginx --image=nginx
kubectl create service clusterip nginx --tcp=80:80
kubectl apply -f thatfile.yaml
```

其中 thatfile.yaml 内容如下：

```yaml
yaml代码解读复制代码apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: nginx
  annotations:
    ingress.kubernetes.io/ssl-redirect: 'false'
spec:
  rules:
    - http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: nginx
                port:
                  number: 80
```

使用 curl 命令访问 nginx 服务：

```arduino
arduino

代码解读
复制代码curl http://localhost
```

这样我们就完成了一个 k3d 集群的创建和应用部署。

## 总结

k3d 是一个非常好用的 k3s 集群管理工具，它可以帮助我们快速创建一个 k3s 集群，方便我们进行开发和测试。后续我们还会介绍如何使用通过其他的一些配套工具，使得我们的开发和测试更加方便。

## 参考资料

- [k3d](https://link.juejin.cn/?target=https%3A%2F%2Fk3d.io%2F%2F)[3](https://link.juejin.cn/?target=)
- [exposing_services](https://link.juejin.cn/?target=https%3A%2F%2Fk3d.io%2Fv5.4.6%2Fusage%2Fexposing_services%2F)[4](https://link.juejin.cn/?target=)
- [K3d vs k3s vs Kind vs Microk8s vs Minikube](https://link.juejin.cn/?target=https%3A%2F%2Fthechief.io%2Fc%2Feditorial%2Fk3d-vs-k3s-vs-kind-vs-microk8s-vs-minikube%2F)[5](https://link.juejin.cn/?target=)
- [k3d 入门：在 Docker 中运行 k3s](https://link.juejin.cn/?target=https%3A%2F%2Fwww.cnblogs.com%2Fhaogj%2Fp%2F16397876.html)[6](https://link.juejin.cn/?target=)

**感谢您的阅读，如果您觉得本文有用，请点赞、关注和转发。**

- 本文作者： [newbe36524](https://link.juejin.cn/?target=https%3A%2F%2Fwww.newbe.pro%2F)
- 本文链接： [www.newbe.pro/Others/0x01…](https://link.juejin.cn/?target=https%3A%2F%2Fwww.newbe.pro%2FOthers%2F0x01A-one-container-but-an-entire-k8s-cluster%2F)
- 版权声明： 本博客所有文章除特别声明外，均采用 BY-NC-SA 许可协议。转载请注明出处！

------

1. [newbe.pro/Mirrors/Mir…](https://link.juejin.cn/?target=https%3A%2F%2Fnewbe.pro%2FMirrors%2FMirrors-k3d%2F%5B%E2%86%A9)]()
2. [newbe.pro/Mirrors/Mir…](https://link.juejin.cn/?target=https%3A%2F%2Fnewbe.pro%2FMirrors%2FMirrors-FastGithub%2F%5B%E2%86%A9)]()
3. [k3d.io/[↩](https://link.juejin.cn/?target=https%3A%2F%2Fk3d.io%2F%5B%E2%86%A9)]()
4. [k3d.io/v5.4.6/usag…](https://link.juejin.cn/?target=https%3A%2F%2Fk3d.io%2Fv5.4.6%2Fusage%2Fexposing_services%2F%5B%E2%86%A9)]()
5. [thechief.io/c/editorial…](https://link.juejin.cn/?target=https%3A%2F%2Fthechief.io%2Fc%2Feditorial%2Fk3d-vs-k3s-vs-kind-vs-microk8s-vs-minikube%2F%5B%E2%86%A9)]()
6. [www.cnblogs.com/haogj/p/163…](https://link.juejin.cn/?target=https%3A%2F%2Fwww.cnblogs.com%2Fhaogj%2Fp%2F16397876.html%5B%E2%86%A9)]()