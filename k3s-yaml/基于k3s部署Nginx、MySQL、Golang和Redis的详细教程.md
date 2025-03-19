# 基于k3s部署Nginx、MySQL、Golang和Redis的详细教程



### **1. 安装k3s集群**

#### **1.1 安装k3s（单节点快速体验）**

```bash
bash代码解读复制代码# 使用root用户或sudo执行
curl -sfL https://get.k3s.io | sh -

# 验证安装
sudo kubectl get nodes  # 应显示一个节点状态为Ready
sudo systemctl status k3s
```

#### **1.2 设置kubectl快捷方式（可选）**

```bash
bash代码解读复制代码mkdir -p ~/.kube
sudo cp /etc/rancher/k3s/k3s.yaml ~/.kube/config
sudo chown $USER ~/.kube/config
export KUBECONFIG=~/.kube/config
```

------

### **2. 部署MySQL数据库**

#### **2.1 创建持久化存储卷（PVC）**

```yaml
yaml代码解读复制代码# mysql-pvc.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mysql-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 2Gi  # 生产环境建议5Gi以上
bash

代码解读
复制代码kubectl apply -f mysql-pvc.yaml
```

#### **2.2 创建数据库密码Secret**

```bash
bash代码解读复制代码kubectl create secret generic mysql-secret \
  --from-literal=root_password=your_secure_password \
  --from-literal=database=appdb
```

#### **2.3 部署MySQL**

```yaml
yaml代码解读复制代码# mysql-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mysql-deployment
spec:
  replicas: 1
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
          image: mysql:8.0
          env:
            - name: MYSQL_ROOT_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: mysql-secret
                  key: root_password
            - name: MYSQL_DATABASE
              valueFrom:
                secretKeyRef:
                  name: mysql-secret
                  key: database
          ports:
            - containerPort: 3306
          volumeMounts:
            - mountPath: /var/lib/mysql
              name: mysql-data
      volumes:
        - name: mysql-data
          persistentVolumeClaim:
            claimName: mysql-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: mysql-service
spec:
  selector:
    app: mysql
  ports:
    - port: 3306
      targetPort: 3306
  type: ClusterIP
bash

代码解读
复制代码kubectl apply -f mysql-deployment.yaml
```

------

### **3. 部署Redis缓存**

#### **3.1 创建Redis持久化存储**

```yaml
yaml代码解读复制代码# redis-pvc.yaml
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
bash

代码解读
复制代码kubectl apply -f redis-pvc.yaml
```

#### **3.2 部署Redis**

```yaml
yaml代码解读复制代码# redis-deployment.yaml
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
          image: redis:alpine
          ports:
            - containerPort: 6379
          volumeMounts:
            - mountPath: /data
              name: redis-data
          command: ["redis-server", "--appendonly yes"]  # 启用持久化
      volumes:
        - name: redis-data
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
    - port: 6379
      targetPort: 6379
  type: ClusterIP
bash

代码解读
复制代码kubectl apply -f redis-deployment.yaml
```

------

### **4. 部署Golang应用**

#### **4.1 准备Golang Docker镜像**

1. 创建示例Golang应用 `main.go`：

   ```go
   go代码解读复制代码package main
   
   import (
       "fmt"
       "net/http"
       "database/sql"
       _ "github.com/go-sql-driver/mysql"
       "github.com/redis/go-redis/v9"
   )
   
   func handler(w http.ResponseWriter, r *http.Request) {
       // 连接MySQL
       db, _ := sql.Open("mysql", "root:${MYSQL_ROOT_PASSWORD}@tcp(mysql-service:3306)/${MYSQL_DATABASE}")
       defer db.Close()
       
       // 连接Redis
       rdb := redis.NewClient(&redis.Options{Addr: "redis-service:6379"})
       defer rdb.Close()
       
       fmt.Fprintf(w, "Connected to MySQL and Redis!")
   }
   
   func main() {
       http.HandleFunc("/", handler)
       http.ListenAndServe(":8080", nil)
   }
   ```

2. 创建 `Dockerfile`：

   ```dockerfile
   dockerfile代码解读复制代码FROM golang:1.20-alpine AS builder
   WORKDIR /app
   COPY . .
   RUN go mod init app && go mod tidy
   RUN CGO_ENABLED=0 GOOS=linux go build -o /app/main
   
   FROM alpine:latest
   COPY --from=builder /app/main /app/main
   EXPOSE 8080
   CMD ["/app/main"]
   ```

3. 构建并推送镜像到仓库（或本地构建）：

   ```bash
   bash代码解读复制代码docker build -t yourusername/golang-app:v1 .
   docker push yourusername/golang-app:v1
   ```

#### **4.2 部署Golang应用到k3s**

```yaml
yaml代码解读复制代码# golang-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: golang-deployment
spec:
  replicas: 2
  selector:
    matchLabels:
      app: golang
  template:
    metadata:
      labels:
        app: golang
    spec:
      containers:
        - name: golang
          image: yourusername/golang-app:v1  # 替换为你的镜像
          ports:
            - containerPort: 8080
          env:
            - name: MYSQL_ROOT_PASSWORD  # 从Secret注入
              valueFrom:
                secretKeyRef:
                  name: mysql-secret
                  key: root_password
            - name: MYSQL_DATABASE
              valueFrom:
                secretKeyRef:
                  name: mysql-secret
                  key: database
          livenessProbe:  # 健康检查
            httpGet:
              path: /
              port: 8080
            initialDelaySeconds: 10
            periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: golang-service
spec:
  selector:
    app: golang
  ports:
    - port: 8080
      targetPort: 8080
  type: ClusterIP
bash

代码解读
复制代码kubectl apply -f golang-deployment.yaml
```

------

### **5. 部署Nginx反向代理**

#### **5.1 创建Nginx配置文件**

```yaml
yaml代码解读复制代码# nginx-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: nginx-config
data:
  default.conf: |
    server {
        listen 80;
        server_name localhost;

        location / {
            proxy_pass http://golang-service:8080;  # 转发到Golang服务
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }
bash

代码解读
复制代码kubectl apply -f nginx-config.yaml
```

#### **5.2 部署Nginx**

```yaml
yaml代码解读复制代码# nginx-deployment.yaml
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
            - mountPath: /etc/nginx/conf.d
              name: nginx-config
      volumes:
        - name: nginx-config
          configMap:
            name: nginx-config
---
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  selector:
    app: nginx
  ports:
    - port: 80
      targetPort: 80
  type: NodePort  # 或LoadBalancer
bash

代码解读
复制代码kubectl apply -f nginx-deployment.yaml
```

------

### **6. 验证部署**

#### **6.1 查看所有资源状态**

```bash
bash

代码解读
复制代码kubectl get pods,svc,pvc
```

- 确保所有Pod状态为 `Running`，服务正常启动。

#### **6.2 访问应用**

```bash
bash代码解读复制代码# 获取Nginx的NodePort
kubectl get svc nginx-service -o jsonpath='{.spec.ports[0].nodePort}'

# 访问应用（假设节点IP为192.168.1.100，NodePort为30007）
curl http://192.168.1.100:30007
```

- 预期输出：`Connected to MySQL and Redis!`

------

### **7. 扩展与维护**

#### **7.1 扩容Golang副本**

```bash
bash

代码解读
复制代码kubectl scale deployment golang-deployment --replicas=3
```

#### **7.2 更新Golang应用**

1. 修改代码后重新构建镜像：

   ```bash
   bash代码解读复制代码docker build -t yourusername/golang-app:v2 .
   docker push yourusername/golang-app:v2
   ```

2. 更新Deployment镜像版本：

   ```bash
   bash
   
   代码解读
   复制代码kubectl set image deployment/golang-deployment golang=yourusername/golang-app:v2
   ```

------

### **8. 关键配置说明**

| 组件   | 核心配置项                                      | 作用说明            |
| ------ | ----------------------------------------------- | ------------------- |
| MySQL  | `persistentVolumeClaim`                         | 数据持久化到PVC     |
| Redis  | `command: ["redis-server", "--appendonly yes"]` | 启用AOF持久化       |
| Golang | `livenessProbe`                                 | 自动重启不健康的Pod |
| Nginx  | `proxy_pass http://golang-service`              | 反向代理到后端服务  |

------

### **附：常见问题排查**

1. **Golang无法连接MySQL/Redis**

   - 检查服务名称是否正确（`mysql-service`、`redis-service`）
   - 验证Secret中的密码是否匹配

   ```bash
   bash
   
   代码解读
   复制代码kubectl exec -it <golang-pod> -- env | grep MYSQL_ROOT_PASSWORD
   ```

2. **Nginx返回502错误**

   - 检查Golang服务是否正常运行：

     ```bash
     bash
     
     代码解读
     复制代码kubectl logs <golang-pod>
     ```

3. **持久化存储未生效**

   - 确认PVC状态是否为 `Bound`：

     ```bash
     bash
     
     代码解读
     复制代码kubectl get pvc
     ```