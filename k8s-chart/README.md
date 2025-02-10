# k8s-chart

#### 介绍
本库为 [k8s-gateway](https://gitee.com/shinstein/k8s-gateway)、[k8s-order](https://gitee.com/shinstein/k8s-order)、[k8s-user](https://gitee.com/shinstein/k8s-user)、[k8s-product](https://gitee.com/shinstein/k8s-product)项目的helm包，还包括为这4个项目创建的ingress资源文件

#### 软件架构
k8s v1.25.4 + containerd v1.6.10 + helm v3.13.1

k8s集群节点信息
| Node                  | OS | Memory | CPU | Disk |
|-----------------------|----|--------|-----|------|
| master-192.168.62.152 |CentOS Linux release 7.8.2003 (Core) |    4Gi    |  4C   |   20Gi   |
| node1-192.168.62.153 |CentOS Linux release 7.8.2003 (Core) |    3Gi    | 4C   |   20Gi |
| node2-192.168.62.154 |CentOS Linux release 7.8.2003 (Core)|    3Gi    |  4C   |   20Gi |
| node3-192.168.62.155 |CentOS Linux release 7.8.2003 (Core)|     3Gi   |  4C   |   20Gi |


全部部署完成后节点资源使用情况
```sh
[root@master ~]# kubectl top no
NAME     CPU(cores)   CPU%   MEMORY(bytes)   MEMORY%   
master   159m         3%     1414Mi          38%       
node1    152m         3%     1686Mi          62%       
node2    139m         3%     1614Mi          60%       
node3    159m         3%     1847Mi          68%       
[root@master ~]# 
```

所有业务均采用一个副本，可在chart包的values.yaml中进行修改
```sh
[root@master ~]# kubectl get po |grep -E 'order|product|user|gateway'
gateway-5b85d68c74-rrkm6                    1/1     Running     0              10h
order-5997b57f5c-grjjp                      1/1     Running     0              4h51m
product-c8bc49798-949vn                     1/1     Running     0              4h47m
user-6bf9c85f7f-hcjgp                       1/1     Running     0              34h
[root@master ~]# 
```

#### 安装教程

1.  在安装本库中的4个chart包前先[安装k8s集群](https://hushed-sardine-f46.notion.site/k8s-2-5-4-7d9a8e1a9950464e888913c08e28c2a2?pvs=4)、基础组件（本地存储 [local-path-provisioner](https://gitee.com/shinstein/local-path-provisioner)、[metrics-server](https://gitee.com/shinstein/metrics-server)、[metallb](https://gitee.com/shinstein/k8s-metallb)、[ingress-nginx](https://gitee.com/shinstein/k8s-ingress)）、中间件([mysql](https://gitee.com/shinstein/k8s-mysql)、[redis](https://gitee.com/shinstein/k8s-redis)、[rabbitmq](https://gitee.com/shinstein/k8s-rabbitmq))、私有制品库[harbor](https://hushed-sardine-f46.notion.site/Harbor-2-9-0-4f1f928c97374777a4031d2d15162671?pvs=4)（如果需要的话） 
2.  在私有harbor机器上 拉取 [k8s-gateway](https://gitee.com/shinstein/k8s-gateway)、[k8s-order](https://gitee.com/shinstein/k8s-order)、[k8s-user](https://gitee.com/shinstein/k8s-user)、[k8s-product](https://gitee.com/shinstein/k8s-product)代码（库中的build.sh中配置的是我自己的本地私有harbor,根据实际情况修改制品库地址和令牌等）执行以下步骤即可完成构建并推送制品到私有harbor库
```sh
# 以k8s-gateway库为例
git clone https://gitee.com/shinstein/k8s-gateway.git

cd k8s-gateway

chmod +x build.sh

./build.sh gateway
```
3. 下载本库
```sh
git clone https://gitee.com/shinstein/k8s-chart.git
```

4.  修改helm的chart中的镜像
```sh
vim gateway/values.yaml
```
5. 安装/更新
```sh
# 渲染chart (可以不执行)
helm template gateway > gateway.yaml

# 安装
helm upgrade -i gateway gateway
```

6. 安装ingress

ingress 执行完后需要在本地机器上配置 hosts 以完成访问
```sh
kubectl apply -f app-ingress.yaml
```

7. 访问接口

在本机上配置host, `192.168.62.100` 为 metallb分配的lb的ip，使用 `app.zw.com`访问应用，使用 `mq.zw.com` 登录rabbitmq 用户名/密码：admin/admin123
```sh
192.168.62.100 app.zw.com
192.168.62.100 mq.zw.com
```

用户注册 - request

```sh
curl --request POST \
  --url http://app.zw.com/register \
  --header 'content-type: application/json' \
  --data '{
    "name": "Tom2"
}'
```
用户注册 - response
```yaml
{
	"code": 200,
	"message": null,
	"data": {
		"user": {
			"id": 4,
			"name": "Tom2"
		},
		"token": "eyJhbGciOiJIUzI1NiJ9.eyJpZCI6NCwibmFtZSI6IlRvbTIifQ.7EBZPOSD9Bcu65ip31HJlQMjTlaVMkybYk96nfCRmz0"
	}
}
```


用户登录 - request
```sh
curl --request POST \
  --url http://app.zw.com/login \
  --header 'content-type: application/json' \
  --data '{
    "name": "Tom2"
}'
```
用户登录 - response
```yaml
{
	"code": 200,
	"message": null,
	"data": {
		"user": {
			"id": 4,
			"name": "Tom2"
		},
		"token": "eyJhbGciOiJIUzI1NiJ9.eyJpZCI6NCwibmFtZSI6IlRvbTIifQ.7EBZPOSD9Bcu65ip31HJlQMjTlaVMkybYk96nfCRmz0"
	}
}
```


增加商品 - request
```sh
curl --request POST \
  --url http://app.zw.com/product/add \
  --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiJ9.eyJpZCI6NCwibmFtZSI6IlRvbTIifQ.7EBZPOSD9Bcu65ip31HJlQMjTlaVMkybYk96nfCRmz0' \
  --header 'content-type: application/json' \
  --data '{
    "name": "袜子",
    "price": 2.34,
    "stock": 100
}'
```
增加商品 - response
```yaml
{
	"code": 200,
	"message": null,
	"data": {
		"id": 2,
		"name": "袜子",
		"price": 2.34,
		"stock": 100
	}
}
```


添加订单 - request
```sh
curl --request POST \
  --url http://app.zw.com/order/add \
  --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiJ9.eyJpZCI6NCwibmFtZSI6IlRvbTIifQ.7EBZPOSD9Bcu65ip31HJlQMjTlaVMkybYk96nfCRmz0' \
  --header 'content-type: application/json' \
  --data '{
    "productId": 2,
    "number": 2
}'
```
添加订单 - response
```yaml
{
	"code": 200,
	"message": null,
	"data": null
}
```


查询当前用户所有订单 - request
```sh
curl --request GET \
  --url http://app.zw.com/order/list \
  --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiJ9.eyJpZCI6NCwibmFtZSI6IlRvbTIifQ.7EBZPOSD9Bcu65ip31HJlQMjTlaVMkybYk96nfCRmz0'
```
查询当前用户所有订单 - response
```yaml
{
	"code": 200,
	"message": null,
	"data": [
		{
			"id": 2,
			"userId": 4,
			"user": {
				"id": 4,
				"name": "Tom2"
			},
			"product": {
				"id": 2,
				"name": "袜子",
				"price": 2.34,
				"stock": 93
			},
			"productId": 2,
			"number": 12
		},
		{
			"id": 3,
			"userId": 4,
			"user": {
				"id": 4,
				"name": "Tom2"
			},
			"product": {
				"id": 2,
				"name": "袜子",
				"price": 2.34,
				"stock": 93
			},
			"productId": 2,
			"number": 10
		},
		{
			"id": 4,
			"userId": 4,
			"user": {
				"id": 4,
				"name": "Tom2"
			},
			"product": {
				"id": 2,
				"name": "袜子",
				"price": 2.34,
				"stock": 93
			},
			"productId": 2,
			"number": 3
		},
		{
			"id": 5,
			"userId": 4,
			"user": {
				"id": 4,
				"name": "Tom2"
			},
			"product": {
				"id": 2,
				"name": "袜子",
				"price": 2.34,
				"stock": 93
			},
			"productId": 2,
			"number": 4
		},
		{
			"id": 6,
			"userId": 4,
			"user": {
				"id": 4,
				"name": "Tom2"
			},
			"product": {
				"id": 2,
				"name": "袜子",
				"price": 2.34,
				"stock": 93
			},
			"productId": 2,
			"number": 5
		},
		{
			"id": 7,
			"userId": 4,
			"user": {
				"id": 4,
				"name": "Tom2"
			},
			"product": {
				"id": 1,
				"name": "鞋子",
				"price": 25.34,
				"stock": 92
			},
			"productId": 1,
			"number": 6
		},
		{
			"id": 8,
			"userId": 4,
			"user": {
				"id": 4,
				"name": "Tom2"
			},
			"product": {
				"id": 1,
				"name": "鞋子",
				"price": 25.34,
				"stock": 92
			},
			"productId": 1,
			"number": 2
		},
		{
			"id": 9,
			"userId": 4,
			"user": {
				"id": 4,
				"name": "Tom2"
			},
			"product": {
				"id": 2,
				"name": "袜子",
				"price": 2.34,
				"stock": 93
			},
			"productId": 2,
			"number": 2
		}
	]
}
```


查询所有订单 - request
```sh
curl --request GET \
  --url http://app.zw.com/order/all \
  --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiJ9.eyJpZCI6NCwibmFtZSI6IlRvbTIifQ.7EBZPOSD9Bcu65ip31HJlQMjTlaVMkybYk96nfCRmz0'
```
查询所有订单 - response
```json
{
	"code": 200,
	"message": null,
	"data": [
		{
			"id": 1,
			"userId": 3,
			"user": {
				"id": 3,
				"name": "Tom1"
			},
			"product": {
				"id": 1,
				"name": "鞋子",
				"price": 25.34,
				"stock": 100
			},
			"productId": 1,
			"number": 2
		},
		{
			"id": 2,
			"userId": 4,
			"user": {
				"id": 4,
				"name": "Tom2"
			},
			"product": {
				"id": 2,
				"name": "袜子",
				"price": 2.34,
				"stock": 100
			},
			"productId": 2,
			"number": 12
		}
	]
}
```

#### 使用说明

1.  本套k8s环境使用containerd作为 CRI，如果想像本例一样使用私有harbor仓库，需要在集群各个节点上修改containerd的配置文件，增加跳过私有harbor的证书校验配置,其中 `192.168.62.150` 为私有harbor仓库地址，改完重启containerd
```sh
vim /etc/containerd/config.toml

...
    [plugins."io.containerd.grpc.v1.cri".registry]

      [plugins."io.containerd.grpc.v1.cri".registry.configs]
        [plugins."io.containerd.grpc.v1.cri".registry.configs."192.168.62.150".tls]
          insecure_skip_verify = true

      [plugins."io.containerd.grpc.v1.cri".registry.mirrors]
        [plugins."io.containerd.grpc.v1.cri".registry.mirrors."docker.io"]
          endpoint = ["https://bqr1dr1n.mirror.aliyuncs.com"]
        [plugins."io.containerd.grpc.v1.cri".registry.mirrors."192.168.62.150"]
          endpoint = ["http://192.168.62.150"]
```

   

