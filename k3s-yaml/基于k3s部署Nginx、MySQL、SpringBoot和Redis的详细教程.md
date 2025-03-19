# 基于k3s部署Nginx、MySQL、SpringBoot和Redis的详细教程



### **1. 安装k3s集群**

#### **1.1 单节点快速部署**

```bash
bash代码解读复制代码# 使用root或sudo权限执行
curl -sfL https://get.k3s.io | sh -

# 验证安装
sudo kubectl get nodes  # 输出应为Ready状态
sudo systemctl status k3s
```

#### **1.2 配置kubectl权限（可选）**

```bash
bash代码解读复制代码mkdir -p ~/.kube
sudo cp /etc/rancher/k3s/k3s.yaml ~/.kube/config
sudo chown $USER ~/.kube/config
export KUBECONFIG=~/.kube/config
```

------

### **2. 部署MySQL数据库**

#### **2.1 创建持久化存储卷**

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
      storage: 5Gi  # 生产环境建议10Gi以上
      
      
      
      
bash

代码解读
复制代码kubectl apply -f mysql-pvc.yaml
```

#### **2.2 创建数据库密码Secret**

```bash
bash代码解读复制代码kubectl create secret generic mysql-secret \
  --from-literal=root_password=your_secure_password \
  --from-literal=database=springdb
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
      storage: 2Gi
      
      
      
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
          image: redis:7.0-alpine
          command: ["redis-server", "--appendonly yes"]  # 启用持久化
          ports:
            - containerPort: 6379
          volumeMounts:
            - mountPath: /data
              name: redis-data
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

### **4. 部署SpringBoot应用**

#### **4.1 准备SpringBoot Docker镜像**

1. **示例`application.properties`**：

   ```properties
   properties代码解读复制代码spring.datasource.url=jdbc:mysql://mysql-service:3306/${MYSQL_DATABASE}
   spring.datasource.username=root
   spring.datasource.password=${MYSQL_ROOT_PASSWORD}
   spring.redis.host=redis-service
   spring.redis.port=6379
   ```

2. **Dockerfile**：

   ```dockerfile
   dockerfile代码解读复制代码FROM maven:3.8.6-jdk-11 AS build
   WORKDIR /app
   COPY . .
   RUN mvn clean package -DskipTests
   
   FROM openjdk:11-jre-slim
   COPY --from=build /app/target/*.jar /app.jar
   ENTRYPOINT ["java","-jar","/app.jar"]
   ```

3. **构建并推送镜像**：

   ```bash
   bash代码解读复制代码docker build -t yourusername/springboot-app:v1 .
   docker push yourusername/springboot-app:v1
   ```

#### **4.2 部署SpringBoot到k3s**

```yaml
yaml代码解读复制代码# springboot-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: springboot-deployment
spec:
  replicas: 2
  selector:
    matchLabels:
      app: springboot
  template:
    metadata:
      labels:
        app: springboot
    spec:
      containers:
        - name: springboot
          image: yourusername/springboot-app:v1
          ports:
            - containerPort: 8080
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
          livenessProbe:
            httpGet:
              path: /actuator/health
              port: 8080
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /actuator/health
              port: 8080
---
apiVersion: v1
kind: Service
metadata:
  name: springboot-service
spec:
  selector:
    app: springboot
  ports:
    - port: 8080
      targetPort: 8080
  type: ClusterIP
  
  
  
  
bash

代码解读
复制代码kubectl apply -f springboot-deployment.yaml
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
            proxy_pass http://springboot-service:8080;
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

#### **6.1 检查所有组件状态**

```bash
bash代码解读复制代码kubectl get pods,svc,pvc
# 输出示例：
# NAME                                       READY   STATUS    RESTARTS   AGE
# pod/mysql-deployment-7c6d8f8b4d-abcde      1/1     Running   0          5m
# pod/redis-deployment-7d5f8d4b5f-fghij      1/1     Running   0          4m
# pod/springboot-deployment-6d5f8d4b5f-klmno 2/2     Running   0          3m
# pod/nginx-deployment-7c6d8f8b4d-pqrst      1/1     Running   0          2m
```

#### **6.2 访问SpringBoot应用**

```bash
bash代码解读复制代码# 获取NodePort
NODE_PORT=$(kubectl get svc nginx-service -o jsonpath='{.spec.ports[0].nodePort}')
curl http://<节点IP>:$NODE_PORT
# 预期输出：SpringBoot应用的响应（如"Hello World"）
```

------

### **7. 扩展与维护**

#### **7.1 横向扩展SpringBoot**

```bash
bash

代码解读
复制代码kubectl scale deployment springboot-deployment --replicas=3
```

#### **7.2 更新应用版本**

1. 修改代码后重新构建镜像：

   ```bash
   bash代码解读复制代码docker build -t yourusername/springboot-app:v2 .
   docker push yourusername/springboot-app:v2
   ```

2. 滚动更新：

   ```bash
   bash
   
   代码解读
   复制代码kubectl set image deployment/springboot-deployment springboot=yourusername/springboot-app:v2
   ```

------

### **8. 关键配置说明**

| 组件       | 核心配置项                                      | 作用说明               |
| ---------- | ----------------------------------------------- | ---------------------- |
| MySQL      | `persistentVolumeClaim`                         | 数据持久化存储         |
| Redis      | `command: ["redis-server", "--appendonly yes"]` | 启用AOF持久化          |
| SpringBoot | `livenessProbe` 和 `readinessProbe`             | 健康检查确保服务可用性 |
| Nginx      | `proxy_pass http://springboot-service`          | 反向代理到Java应用     |

------

### **附：常见问题排查**

1. **SpringBoot无法连接MySQL**

   - 检查Secret中的密码是否匹配：

     ```bash
     bash
     
     代码解读
     复制代码kubectl get secret mysql-secret -o jsonpath='{.data.root_password}' | base64 -d
     ```

   - 查看SpringBoot日志：

     ```bash
     bash
     
     代码解读
     复制代码kubectl logs -f <springboot-pod>
     ```

2. **Nginx返回502错误**

   - 确认SpringBoot服务是否就绪：

     ```bash
     bash
     
     代码解读
     复制代码kubectl get endpoints springboot-service
     ```

3. **数据持久化失败**

   - 检查PVC绑定状态：

     ```bash
     bash
     
     代码解读
     复制代码kubectl get pvc
     ```

