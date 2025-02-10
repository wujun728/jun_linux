
安装docker-compose
https://docs.docker.com/compose/install/#install-compose

```
sudo curl -L https://github.com/docker/compose/releases/download/1.21.1/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

docker-compose up 错误处理
```
ERROR: Couldn't connect to Docker daemon at http+docker://localhost - is it running?

If it's at a non-standard location, specify the URL with the DOCKER_HOST environment variable.
```

解决办法
```
# sudo vim /etc/default/docker

增加  DOCKER_OPTS="-H tcp://127.0.0.1:4243 -H unix:///var/run/docker.sock"

# sudo service docker restart

设置 DOCKER_HOST 环境变量，可以添加到 ~/.bashrc 文件中

# sudo vim ~/.bashrc

增加 export DOCKER_HOST=tcp://localhost:4243

# source ~/.bashrc

```


学习使用 docker-compose 运行 php+nginx+mysql 环境

自动创建MYSQL导入MYSQL数据

运行
```
docker-compose build     # build dockerfile
docker-compose up        # 构建启动 -d 后台运行
docker-compose start     # 启动
docker-compose stop      # 停止
docker-compose restart   # 重启
docker-compose down      # 清除
```

访问
```
http://127.0.0.1:8080/
```

mysql访问
```
mysql -h 127.0.0.1 -P3306 -uroot -p123456
```

redis访问
```
redis-cli -h 127.0.0.1 -p 6379
```