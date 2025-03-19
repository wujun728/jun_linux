# 生产环境使用k3s避雷指南：避免数据丢失与不可恢复



### **1. 存储安全：避免数据丢失的核心**

#### **1.1 必须使用持久化存储**

- **问题**：k3s默认使用临时存储（如`emptyDir`），容器重启后数据会丢失。

- **解决方案**：

  - **生产环境必须使用持久化存储卷（PVC）** ，并绑定到可靠的存储后端（如云厂商的块存储、NFS、Longhorn等）。

  - **示例**：[在MySQL/Redis的Deployment中](https://juejin.cn/spost/7481111646142087205)，替换`emptyDir`为持久化PVC：

    ```yaml
    yaml代码解读复制代码volumes:
      - name: mysql-data
        persistentVolumeClaim:
          claimName: mysql-pvc  # 预先创建好的PVC
    ```

#### **1.2 配置存储类（StorageClass）**

- **作用**：自动化管理存储卷的创建和绑定。

- **操作**：

  ```yaml
  yaml代码解读复制代码# storage-class.yaml（以NFS为例）
  apiVersion: storage.k8s.io/v1
  kind: StorageClass
  metadata:
    name: nfs-storage
  provisioner: k8s-sigs.io/nfs-subdir-external-provisioner
  parameters:
    archiveOnDelete: "false"  # 删除PVC时保留数据
  ```

  ```bash
  bash
  
  代码解读
  复制代码kubectl apply -f storage-class.yaml
  ```

  - **关键参数**：`reclaimPolicy: Retain`（删除PVC时不删除数据）。

#### **1.3 避免单点故障**

- **多副本存储**：
  - MySQL/Redis等有状态服务，使用主从复制方案（如MySQL主从、Redis Sentinel）。
  - 使用支持高可用的存储后端（如Ceph、云厂商的分布式存储）。

------

### **2. 备份策略：数据恢复的生命线**

#### **2.1 定期备份关键数据**

- **数据库备份**：

  - **MySQL**：使用`mysqldump`或`Percona XtraBackup`，备份文件保存到云存储（如S3）。
  - **Redis**：启用RDB/AOF持久化，定期备份`dump.rdb`文件。

- **操作示例**（CronJob自动备份MySQL）：

  ```yaml
  yaml代码解读复制代码apiVersion: batch/v1
  kind: CronJob
  metadata:
    name: mysql-backup
  spec:
    schedule: "0 2 * * *"  # 每天凌晨2点执行
    jobTemplate:
      spec:
        template:
          spec:
            containers:
            - name: mysqldump
              image: mysql:5.7
              command:
              - /bin/sh
              - -c
              - "mysqldump -h mysql-service -uroot -p$MYSQL_ROOT_PASSWORD --all-databases | gzip > /backup/backup.sql.gz"
              env:
              - name: MYSQL_ROOT_PASSWORD
                valueFrom:
                  secretKeyRef:
                    name: mysql-secret
                    key: password
              volumeMounts:
              - mountPath: /backup
                name: backup-volume
            volumes:
            - name: backup-volume
              persistentVolumeClaim:
                claimName: backup-pvc  # 绑定到持久化存储
            restartPolicy: OnFailure
  ```

#### **2.2 使用Velero实现全集群备份**

- **Velero工具**：备份整个k3s集群（包括资源定义和数据）。

- **操作步骤**：

  1. 安装Velero（需配置云存储如AWS S3、MinIO）：

     ```bash
     bash代码解读复制代码velero install --provider aws --plugins velero/velero-plugin-for-aws:v1.0.0 \
     --bucket your-bucket --secret-file ./credentials-aws \
     --backup-location-config region=us-east-1 \
     --use-volume-snapshots=false
     ```

  2. 创建每日备份：

     ```bash
     bash
     
     代码解读
     复制代码velero create schedule daily-backup --schedule="0 1 * * *"
     ```

------

### **3. 高可用部署：避免服务不可用**

#### **3.1 k3s集群高可用**

- **多节点部署**：

  - 至少部署3个`server`节点（奇数个，避免脑裂问题）。

  - 安装命令：

    ```bash
    bash代码解读复制代码# 第一个节点
    curl -sfL https://get.k3s.io | sh -s - server --cluster-init
    # 后续节点
    curl -sfL https://get.k3s.io | sh -s - server --server https://<第一个节点IP>:6443
    ```

- **Agent节点**：用于运行工作负载，与server节点分离。

#### **3.2 应用多副本与健康检查**

- **Deployment配置**：

  ```yaml
  yaml代码解读复制代码spec:
    replicas: 3  # 至少3个副本
    strategy:
      type: RollingUpdate  # 滚动更新避免中断
    template:
      spec:
        containers:
        - name: nginx
          livenessProbe:   # 存活检查
            httpGet:
              path: /
              port: 80
            initialDelaySeconds: 5
            periodSeconds: 10
          readinessProbe:  # 就绪检查
            httpGet:
              path: /
              port: 80
  ```

------

### **4. 安全加固：防止人为误操作**

#### **4.1 限制删除操作**

- **资源保护**：

  ```bash
  bash代码解读复制代码# 防止误删Namespace
  kubectl annotate ns default kubernetes.io/metadata.name=default --overwrite
  ```

- **RBAC权限控制**：

  - 为不同用户分配最小权限（避免使用`cluster-admin`）。

  - 示例（只读权限）：

    ```yaml
    yaml代码解读复制代码apiVersion: rbac.authorization.k8s.io/v1
    kind: Role
    metadata:
      name: viewer
    rules:
    - apiGroups: [""]
      resources: ["pods", "services"]
      verbs: ["get", "list"]
    ```

#### **4.2 审计与监控**

- **启用k3s审计日志**：

  ```bash
  bash代码解读复制代码# 修改k3s启动参数（/etc/systemd/system/k3s.service）
  ExecStart=/usr/local/bin/k3s server --audit-log-path=/var/log/k3s-audit.log
  ```

- **监控工具**：

  - 使用Prometheus + Grafana监控集群状态。
  - 使用Loki + Promtail收集日志。

------

### **5. 灾难恢复：最后一层防线**

#### **5.1 恢复流程**

1. **从Velero备份恢复集群**：

   ```bash
   bash
   
   代码解读
   复制代码velero restore create --from-backup daily-backup
   ```

2. **手动恢复数据库**：

   ```bash
   bash
   
   代码解读
   复制代码kubectl exec -it mysql-pod -- mysql -uroot -p$MYSQL_ROOT_PASSWORD < backup.sql
   ```

#### **5.2 定期演练恢复**

- **每季度模拟一次灾难场景**：
  - 删除一个Namespace，验证备份恢复是否有效。
  - 随机终止节点，检查服务是否自动迁移。

------

### **关键总结**

| 风险点     | 避雷方案                    | 操作示例                        |
| ---------- | --------------------------- | ------------------------------- |
| 数据丢失   | 使用持久化存储 + Velero备份 | PVC绑定云存储 + 每日定时备份    |
| 服务不可用 | 多副本部署 + 健康检查       | `replicas: 3` + `livenessProbe` |
| 人为误操作 | RBAC权限控制 + 资源保护     | 只读权限角色 + 防删注解         |
| 集群崩溃   | 多节点高可用 + 定期恢复演练 | 3个server节点 + 模拟灾难测试    |

------

### **附：新手常见误操作与预防**

1. **误删PVC**：
   - **预防**：设置`persistentVolumeReclaimPolicy: Retain`。
2. **使用latest镜像标签**：
   - **预防**：固定镜像版本（如`nginx:1.23.4`）。
3. **节点资源不足**：
   - **预防**：监控资源使用率，设置`resources.limits`。