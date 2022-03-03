```shell
#常用
#sudo docker-compose up -d
#sudo docker-compose stop
#sudo docker-compose ps

#Name               Command              State                    Ports
#----------------------------------------------------------------------------------------
#mysql   docker-entrypoint.sh mysqld     Up      0.0.0.0:3305->3306/tcp
#nginx   nginx -g daemon off;            Up      0.0.0.0:443->443/tcp, 0.0.0.0:81->80/tcp
#php     docker-php-entrypoint php-fpm   Up      0.0.0.0:9000->9000/tcp


#启动mysql实例
#sudo docker run --name mysql -p:3305:3306 -e MYSQL_ROOT_PASSWORD=123456 -d mysql:latest
#查看mysql日记
#sudo docker logs mysql
#进入mysql容器
#sudo docker exec -it mysql bash

#删除所有容器
#sudo docker rm $(sudo docker ps -a -q)
#删除所有镜像
#sudo docker rmi $(sudo docker images -a -q)
```