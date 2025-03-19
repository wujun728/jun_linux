# [基于k3s部署Nginx、MySQL、PHP和Redis的详细教程](https://segmentfault.com/a/1190000046217804)

![头图](https://segmentfault.com/img/bVdh5wn?spec=cover)

### **先决条件**

- 一台Linux服务器（或本地虚拟机），建议Ubuntu/CentOS
- 基础命令行操作能力
- 确保服务器有至少2GB内存和10GB磁盘空间

------

### **1. 安装k3s（极简Kubernetes）**

#### **1.1 一键安装**

```bash
# 用root用户或sudo权限执行以下命令
curl -sfL https://get.k3s.io | sh -
```

**解释**：

- `k3s` 是一个轻量级Kubernetes发行版，专为资源有限的环境设计
- 这条命令会自动下载并安装k3s，默认使用`containerd`作为容器运行时

#### **1.2 验证安装**

```bash
# 检查k3s服务状态
sudo systemctl status k3s

# 查看节点（此时应显示一个节点）
sudo kubectl get nodes
```

**可能遇到的问题**：

- 如果提示`kubectl command not found`，尝试退出终端重新登录

------

### **2. 部署MySQL数据库**

#### **2.1 创建存储卷（保存数据库数据）**

创建文件 `mysql-pvc.yaml`：

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mysql-pvc
spec:
  accessModes:
    - ReadWriteOnce  # 存储卷只能被一个节点挂载
  resources:
    requests:
      storage: 1Gi   # 申请1GB存储空间
```

应用配置：

```bash
sudo kubectl apply -f mysql-pvc.yaml
```

#### **2.2 设置数据库密码（安全存储）**

```bash
# 创建一个名为mysql-secret的密钥，密码为yourpassword（自行修改）
sudo kubectl create secret generic mysql-secret --from-literal=password=yourpassword
```

#### **2.3 部署MySQL**

创建文件 `mysql-deployment.yaml`：

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mysql-deployment
spec:
  replicas: 1  # 只运行1个副本
  selector:
    matchLabels:
      app: mysql
  template:
    metadata:
      labels:
        app: mysql
    spec:
      containers:
      - name: mysql
        image: mysql:5.7  # 使用MySQL 5.7镜像
        ports:
        - containerPort: 3306
        env:
        - name: MYSQL_ROOT_PASSWORD  # 从密钥读取密码
          valueFrom:
            secretKeyRef:
              name: mysql-secret
              key: password
        volumeMounts:
        - mountPath: /var/lib/mysql  # 挂载存储卷到容器内目录
          name: mysql-storage
      volumes:
      - name: mysql-storage
        persistentVolumeClaim:
          claimName: mysql-pvc  # 使用之前创建的存储卷
---
apiVersion: v1
kind: Service
metadata:
  name: mysql-service
spec:
  selector:
    app: mysql
  ports:
    - protocol: TCP
      port: 3306     # 服务对外暴露的端口
      targetPort: 3306  # 容器内部端口
  type: ClusterIP  # 仅集群内部访问
```

应用配置：

```bash
sudo kubectl apply -f mysql-deployment.yaml
```

**验证MySQL是否运行**：

```bash
sudo kubectl get pods  # 查看状态是否为Running
```

------

### **3. 部署Redis缓存**

#### **3.1 创建存储卷（保存Redis数据）**

创建文件 `redis-pvc.yaml`：

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: redis-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
```

应用配置：

```bash
sudo kubectl apply -f redis-pvc.yaml
```

#### **3.2 部署Redis**

创建文件 `redis-deployment.yaml`：

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: redis
  template:
    metadata:
      labels:
        app: redis
    spec:
      containers:
      - name: redis
        image: redis:alpine  # 轻量级Redis镜像
        ports:
        - containerPort: 6379
        volumeMounts:
        - mountPath: /data  # Redis数据存储目录
          name: redis-storage
      volumes:
      - name: redis-storage
        persistentVolumeClaim:
          claimName: redis-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: redis-service
spec:
  selector:
    app: redis
  ports:
    - protocol: TCP
      port: 6379
      targetPort: 6379
  type: ClusterIP
```

应用配置：

```bash
sudo kubectl apply -f redis-deployment.yaml
```

------

### **4. 部署PHP应用**

#### **4.1 创建PHP服务**

创建文件 `php-deployment.yaml`：

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: php-deployment
spec:
  replicas: 2  # 运行2个副本提高可用性
  selector:
    matchLabels:
      app: php
  template:
    metadata:
      labels:
        app: php
    spec:
      containers:
      - name: php
        image: php:7.4-fpm  # PHP-FPM镜像
        env:
        - name: MYSQL_HOST
          value: "mysql-service"  # 通过服务名连接MySQL
        - name: REDIS_HOST
          value: "redis-service"  # 通过服务名连接Redis
        volumeMounts:
        - mountPath: /var/www/html  # PHP代码目录
          name: php-code
      volumes:
      - name: php-code
        emptyDir: {}  # 临时存储（生产环境需替换为持久化存储）
```

应用配置：

```bash
sudo kubectl apply -f php-deployment.yaml
```

------

### **5. 部署Nginx反向代理**

#### **5.1 配置Nginx**

创建文件 `nginx-config.yaml`：

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: nginx-config
data:
  nginx.conf: |
    server {
        listen 80;
        root /var/www/html;  # PHP代码目录
        index index.php;

        location / {
            try_files $uri $uri/ /index.php$is_args$args;
        }

        location ~ .php$ {
            fastcgi_pass php-service:9000;  # 转发请求到PHP服务
            include fastcgi_params;
            fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        }
    }
```

应用配置：

```bash
sudo kubectl apply -f nginx-config.yaml
```

#### **5.2 部署Nginx**

创建文件 `nginx-deployment.yaml`：

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 2
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:alpine
        ports:
        - containerPort: 80
        volumeMounts:
        - mountPath: /etc/nginx/conf.d  # 挂载配置文件
          name: nginx-config
        - mountPath: /var/www/html     # 共享PHP代码目录
          name: php-code
      volumes:
      - name: nginx-config
        configMap:
          name: nginx-config  # 使用ConfigMap中的配置
      - name: php-code
        emptyDir: {}
---
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  selector:
    app: nginx
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
  type: NodePort  # 通过节点IP+端口访问
```

应用配置：

```bash
sudo kubectl apply -f nginx-deployment.yaml
```

------

### **6. 访问应用**

#### **6.1 查看服务端口**

```bash
sudo kubectl get svc nginx-service
```

输出示例：

```java
NAME            TYPE       CLUSTER-IP     PORT(S)        AGE
nginx-service   NodePort   10.43.123.45   80:30007/TCP   5m
```

- `30007` 是外部访问端口（随机分配）

#### **6.2 通过浏览器访问**

- 如果部署在本地虚拟机：

  ```javascript
  http://localhost:30007
  ```

- 如果部署在云服务器：

  ```javascript
  http://<服务器公网IP>:30007
  ```

------

### **7. 补充说明**

#### **7.1 如何上传PHP代码？**

1. **临时测试**：进入PHP容器手动创建文件

   ```bash
   sudo kubectl exec -it <php-pod名称> -- bash
   echo "<?php phpinfo(); ?>" > /var/www/html/index.php
   ```

2. **正式部署**：

   - 将代码打包到Docker镜像中
   - 或使用持久化存储（如NFS）

#### **7.2 常用命令**

```bash
# 查看所有资源状态
sudo kubectl get pods,svc,pvc

# 查看Pod日志（替换<pod-name>）
sudo kubectl logs -f <pod-name>

# 删除部署
sudo kubectl delete -f <文件名>.yaml
```

#### **7.3 遇到问题怎么办？**

- 检查Pod状态：

  ```bash
  sudo kubectl describe pod <pod-name>
  ```

- 检查服务是否正常：

  ```bash
  sudo kubectl port-forward svc/nginx-service 8080:80
  # 然后访问 http://localhost:8080
  ```