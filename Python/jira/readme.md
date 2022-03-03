# build
**阿里云image已经删除, 请执行以下命令本地build**

```bash
docker build -t registry.aliyuncs.com/bansh/jira:latest .
```

# install

### start mysql

```bash
docker run -d \
    --name=mysql-db \
    --hostname=mysql-db \
    -e MYSQL_ROOT_PASSWORD=123456 \
    -e MYSQL_DATABASE=jira \
    -e MYSQL_USER=jira \
    -e MYSQL_PASSWORD=jira \
    -v /var/jira/shared/db_data:/var/lib/mysql \
    -e /var/jira/shared/db_logs:/var/log/mysql \
    mysql:5.6 --character-set-server=utf8  --collation-server=utf8_bin
```

### start jira

```bash
docker run -d --publish 8080:8080 \
    --link mysql-db:mysql \
    -v /var/jira/shared/jira_data:/var/atlassian/jira \
    -v /var/jira/shared/jira_logs:/opt/atlassian/jira/logs \
    registry.aliyuncs.com/bansh/jira:latest
```

### start all

```bash
docker-compose up -d
```