docker --help
docker -h
docker -v
docker build
docker build -h
docker build -t PRPF:0.1 .
docker build -t c-n .
docker build -t c_n .
docker build -t centos-nginx
docker build -t centos-nginx .
docker build -t ffmpeg-alpine .
docker build -t mysql:autostart .
docker build -t nginx .
docker build -t nixus/php-7.1.19-fpm-alpine3.7-swoole:1.1 .
docker build -t nixus/php-7.1.19-fpm-alpine:1.0 .
docker build -t nixus/php-7.1.19-fpm-alpine:3.7 .
docker build -t only-centos .
docker build -t onlyCentos .
docker build -t php-redis .
docker build -t php-redis-mysqli .
docker build -t php-redis-pdo .
docker build -t php7.1.19-mysqli-redis4.0.1
docker build -t php7.1.19-mysqli-redis4.0.1 .
docker build -t phpwithmysql .
docker build -t prpf:0.1 .
docker build .
docker conatiner ls
docker container -aq
docker container logs 63070529f662
docker container ls
docker container ls --all
docker container ls -a
docker container ls -aq
docker container rm 37b64850e585
docker container rm 49f7960eb7e4
docker container rm 62652a9f85f2
docker container rm 63070529f662
docker container rm 6cc90d5f4f1a
docker container rm c698beee68e9 ccf5563828ad
docker container rm efc9db4418d0 6dccb90577e4
docker container run --help
docker container run --rm -p 8000:3000 -it koa-demo
docker container run -p 8000:3000 -it koa-demo /bin/bash
docker container run \\n--rm \\n--name php \\nphp:7.1
docker container run \\n--rm \\n--name wordpress \\n--hostname myapp.mydomain.com \\n--volume "$PWD/":/var/www/html \\nphp:5.6-apache
docker container run \\n--rm \\n--name wordpress \\n--hostname myapp.mydomain.com:8080:80 \\n--volume "$PWD/":/var/www/html \\nphp:5.6-apache
docker container run \\n--rm \\n--name wordpress \\n--p 8080:80 \\n--volume "$PWD/":/var/www/html \\nphp:5.6-apache
docker container run \\n--rm \\n--name wordpress \\n--port 8080:80 \\n--volume "$PWD/":/var/www/html \\nphp:5.6-apache
docker container run \\n--rm \\n--name wordpress \\n--ports 8080:80
docker container run \\n--rm \\n--name wordpress \\n--ports 8080:80 \\n--volume "$PWD/":/var/www/html \\nphp:5.6-apache
docker container run \\n--rm \\n--name wordpress \\n--valume "$PWD/":/var/www/html \\nphp:5.6-apache
docker container run \\n--rm \\n--name wordpress \\n--volume "$PWD/":/var/www/html \\n--link wordpressdb:mysql \\n-p 8000:80 \\nphpwithmysql
docker container run \\n--rm \\n--name wordpress \\n--volume "$PWD/":/var/www/html \\n--link wordpressdb:mysql \\nphpwithmysql
docker container run \\n--rm \\n--name wordpress \\n--volume "$PWD/":/var/www/html \\n-p 8000:80 \php:5.6-apache
docker container run \\n--rm \\n--name wordpress \\n--volume "$PWD/":/var/www/html \\nphp:5.6-apache
docker container run \\n--rm \\n--name wordpress \\n--volume "$PWD/":/var/www/html ]
docker container run \\n--rm \\n--name wordpress \\n--volumn "$PWD/":/var/www/html \\nphp:5.6-apache
docker container run \\n--rm \\n--name wordpress \\n-p 127.0.0.2:8080:80 \\n--volume "$PWD/":/var/www/html \\nphp:5.6-apache
docker container run \\n--rm \\n--name wordpress \\n-p 172.17.0.2:8080:80 \\n--volume "$PWD/":/var/www/html \\nphp:5.6-apache
docker container run \\n--rm \\n--name wordpress \\n-p 8080:80 \\n--volume "$PWD/":/var/www/html \\nphp:5.6-apache
docker container run \\n-d \\n--rm \\n--name wordpress \\n--env WORDPRESS_DB_PASSWORD=123456 \\n--link wordpressdb:mysql \\n-p 8000:80 \\nwordpress
docker container run \\n-d \\n--rm \\n--name wordpressdb \\n--env MYSQL_ROOT_PASSWORD \n: 1529938128:0;docker container run \\n-d \\n--rm \\n--name wordpressdb \\n--env MYSQL_ROOT_PASSWORD=123456 \\n--env MYSQL_DATABASE=wordpress \\nmysql:5.7
docker container run \\n-d \\n--rm \\n--name wordpressdb \\n--env MYSQL_ROOT_PASSWORD=123456 \\n--env MYSQL_DATABASE=wordpress \\nmysql:5.7
docker container run \\n-d \\n-p 127.0.0.2:8080:80 \\n--rm \\n--name mynginx \\nnginx
docker container run \\n-d \\n-p 127.0.0.4:8080:80 \\n--rm \\n--name mynginx \\nnginx
docker container run \\n-d \\n-p 192.168.1.111:8080:80 \\n--rm \\n--name mynginx \\nnginx
docker container run \\n-d \\n-p 8000:80 \\n--rm \\n--name mynginx \\nnginx
docker container run hello-world
docker container run php:7.1
docker container start 034f349e45a4 -i bash
docker container start 034f349e45a4 -it bash
docker container start 35cc29cc135a
docker container start 35cc29cc135a -it bash
docker container start 9dea4d2b422e
docker container start ccf5563828ad
docker container status
docker container stop c9984c4481022ca5cf13f5d56dfc474ae6ddbf73a37b275a7283403a8f6bb9f7
docker container stop efc9db4418d0
docker container stop efc9db4418d0 6dccb90577e4
docker container stop wordpress
docker container stop wordpress wordpressdb
docker create --help
docker create -h
docker create ecc74d703eca
docker exec --help
docker exec -h
docker exec -i 35cc29cc135a /bin/bash
docker exec -i 35cc29cc135a bash
docker exec -i bash
docker exec -it 1c0ca6ce5961 bash
docker exec -it 35cc29cc135a bash
docker exec -it 67cc9dc81d0f bash
docker exec -it 9dea4d2b422e bash
docker exec -it bash
docker exec -it e9721354736d bash
docker exec -it employee
docker exec -it f4272 bash
docker exec -it f7aa
docker exec -it f7aa bash
docker exec -it idocker_web_1 bash
docker exec -it learn_mysql_1 bash
docker exec -it mina_mysql_1 bash
docker exec -it mina_mysql_1 sh
docker exec -it mina_nginx_1 sh
docker exec -it mina_php_1 sh
docker exec -it mina_php_1 sh && cd /usr/share/nginx/html/mina
docker exec -it mina_php_1 sh 'cd /usr/share/nginx/html/mina'
docker exec -it mina_php_1 sh -c 'cd /usr/share/nginx/html/mina'
docker exec -it mina_redis_1 sh
docker exec -it test2_nginx_1 sh
docker exec -it test2_php_1 sh
docker exec -it test_mysql_1 bash
docker exec -it test_nginx_1 bash
docker exec -it test_php_1 bash
docker image -h
docker image build -t koa-demo .
docker image ls
docker image ls -a
docker image ls -h
docker image ls a
docker image pull library/hello-world
docker image push nixus/koa-demo
docker image rm 17ce7f35ef74
docker image rm koa-demo nixus/koa-demo hello-world node
docker image rm nginx
docker image rm node
docker image rm node:8.4
docker image rm php
docker image rm ubuntu
docker image rm ubuntu:15.10
docker image search php
docker image tag centos:centos7.4.1708 only
docker image tag koa-demo nixus/koa-demo
docker images
docker images --help
docker images -a
docker info
docker init
docker inspect 6eeb5
docker inspect lucid_archimedes
docker inspect mina_mysql_1
docker inspect test_mysql_1
docker list
docker login
docker logs
docker logs 027ad
docker logs 21fd576027b1
docker logs 6eeb5
docker logs 6eeb55524d8a
docker logs b79b44a221fa
docker logs f631
docker logs idocker_php
docker logs idocker_php_1
docker logs learn_mysql_1
docker logs lucid_archimedes
docker logs mina_ffmpeg_1
docker logs mina_mysql_1
docker logs mina_nginx_1
docker logs mina_nginx_1 > 8081.logs
docker logs mina_nginx_1>8081.logs
docker logs mina_php_1
docker logs php
docker logs test2_nginx_1
docker logs test2_php_1
docker logs test2_phpfpm_1
docker logs test3_nginx_1
docker logs test_mysql_1
docker logs test_nginx_1
docker logs test_php_1
docker logs test_redis_1
docker ls
docker network ls
docker ps
docker ps --filter names
docker ps --filter=names
docker ps --format "{{.ID}}:{{.Names}}:{{.Status}}:{{.Ports}}"
docker ps --format "{{.ID}}\t{{.Names}}\t{{.Status}}\t{{.Ports}}"
docker ps --help
docker ps -a
docker ps -all
docker ps -aq
docker ps -f names
docker ps -h
docker pull alpine
docker pull centos6
docker pull imagine10255/centos6-lnmp-php56
docker pull mysql
docker pull mysql:5.7
docker pull mysql:5.7.22
docker pull mysql:8.0.11
docker pull nclans/centos6
docker pull nginx:1.15.0
docker pull nginx:1.15.0-alpine
docker pull opencoconut/ffmpeg
docker pull php
docker pull php:7.1.18
docker pull php:7.1.19-fpm
docker pull php:7.1.19-fpm-alpine3.7
docker pull redis:4.0
docker pull redis:4.0.10-alpine
docker pull zzzshanghai/centos6-64bit
docker push -h
docker push nixus/php-7.1.19-fpm-alpine:3.7
docker push nixus/php-redis-pdo-ffmpeg:1.0
docker push nixus/php-redis-pdo:1.0
docker push php-redis-pdo:1.0
docker rename --help
docker rm *
docker rm 027ad
docker rm 034f349e45a4
docker rm 0593 70ae
docker rm 0c3233
docker rm 1231
docker rm 2abe72c03bbe 35cc29cc135a
docker rm 2be7e269207e
docker rm 2f3d0
docker rm 304f7
docker rm 48bff71f4b77
docker rm 5eefb
docker rm 63251
docker rm 75ffd
docker rm 7df81261903c
docker rm 84d3bece8233
docker rm 9dea4d2b422e a08440fb1ebb 13a4f2f50b92
docker rm 9e0c
docker rm b0a99
docker rm b1cd9789976f 3dd7f1a5c54e
docker rm b2caaf2d44a5
docker rm c5426804f93f
docker rm d01bf
docker rm d1e2fd4689ad
docker rm de8b1 9ed9b 5aede
docker rm e09da
docker rm ec8bbc03e111 722788b33a62
docker rm ee0c84982055
docker rm f005301a4d86 7b89071b45bf f78665d83d15 b1687e9bb00d e9742b7b80c8
docker rm f2cd8
docker rm f4272
docker rm f57a0e18f8b8 202b9fdc4663 f18f41ce2c93
docker rm f7aaa
docker rmi 0b9c7186b8d4
docker rmi 1a58
docker rmi 28319c1b419b 7801d36d734c 17ce7f35ef74 51952e946807 0d16d0a97dd1
docker rmi 31e54e187f70
docker rmi 3afd
docker rmi 3afd47092a0e
docker rmi 3afd47092a0e 3afd47092a0e
docker rmi 3fd9
docker rmi 5699ececb21c
docker rmi 5bfc08807ea4 26c1ce63ec9c 21495fddd220 328edcd84f1b 9e64176cd8a2
docker rmi 6d14c 7f022
docker rmi 9b5f6b667a56
docker rmi a430
docker rmi alpine
docker rmi b13c0e203bf2 554369fa05ed 42b8aa8be229 8e51bd3e0ab8 bc7fdec94612 a8a59477268d eb15f92a08af 95b8f4b0dbc9
docker rmi b5d
docker rmi b5d9
docker rmi c3562
docker rmi c8eb659d5df6
docker rmi cb8
docker rmi centos
docker rmi centos:7
docker rmi e07a2f30ac5a
docker rmi e38bc07ac18e
docker rmi ecc74d703eca
docker rmi f2e28e58849c 31e54e187f70 71a81cb279e3 5699ececb21c 66bc0f66b7af
docker rmi f337abb849ba 3afd47092a0e
docker rmi imagine10255/centos6-lnmp-php56
docker rmi mysql:8.0.11
docker rmi mysql:autostart
docker rmi mysql:latest
docker rmi nginx:latest
docker rmi nixus/php-fmp7.1.19-alpine3.7:1.0
docker rmi nixus/php-redis-pdo-ffmpeg:1.0
docker rmi only-centos
docker rmi only:latest
docker rmi php-redis
docker rmi php-redis-mysqli
docker rmi php-redis-pdo
docker rmi php:7.1-fpm-alpine3.7
docker rmi php:7.1.19-fpm-alpine
docker rmi php:7.2.7-fpm-alpine3.7
docker run --help
docker run --name mymysql -e MYSQL_ROOT_PASSWORD=123456 -d mysql:first
docker run --name mysql -e MYSQL_ROOT_PASSWORD=123456
docker run --name mysql -e MYSQL_ROOT_PASSWORD=123456  -d
docker run --rm centos:7
docker run --rm centos:7 -it /bin/bash
docker run --rm only -i bash
docker run --rm only-centos
docker run --rm only-centos -i /bin/sh
docker run --rm only-centos -it /bin/bash
docker run --rm only-centos -it /bin/sh
docker run -e --help
docker run -e list
docker run -h
docker run -it --name hi-mysql -v ./mysql/conf:/etc/mysql/conf.d -v ./mysql/data:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=123456 mysql:5.7 bash
docker run -it --name hi-mysql -v /Users/Nixus/iDocker/mysql/conf:/etc/mysql/conf -v /Users/Nixus/iDocker/mysql/data:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=123456 mysql:5.7 bash
docker run -it --name hi-nginx -p 8080:80 -v /Users/Nixus/iDocker/nginx/conf:/etc/nginx/conf -v /Users/Nixus/iDocker/nginx/data:/usr/share/nginx/html nginx:1.15.0 bash
docker run -it --name hi-nginx -p 8080:80 nginx:1.15.0 bash
docker run -it --name mysql -e MYSQL_ROOT_PASSWORD=123456 mysql bash
docker run -it --name mysql -e MYSQL_ROOT_PASSWORD=123456 mysql:5.7 bash
docker run -it --name=employee -v /Users/Nixus/Learn/conf.d/mysql.cnf:/etc/mysql/conf.d/mysql.cnf -v /Users/Nixus/Learn/mysql:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=root --ip 192.168.1.113 -p 3306:3306 --expose=3306 mysql:5.7.22 bash
docker run -it --name=employee -v /Users/Nixus/Learn/conf.d/mysql.cnf:/etc/mysql/conf.d/mysql.cnf -v /Users/Nixus/Learn/mysql:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=root --network bridge --ip 192.168.1.113 -p 3306:3306 --expose=3306 mysql:5.7.22 bash
docker run -it --name=employee -v /Users/Nixus/Learn/conf.d/mysql.cnf:/etc/mysql/conf.d/mysql.cnf -v /Users/Nixus/Learn/mysql:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=root -P mysql:5.7.22 bash
docker run -it --name=employee -v /Users/Nixus/Learn/conf.d/mysql.cnf:/etc/mysql/conf.d/mysql.cnf -v /Users/Nixus/Learn/mysql:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=root -p 192.168.1.110:3306:3306 --expose=3306 mysql:5.7.22 bash
docker run -it --name=employee -v /Users/Nixus/Learn/conf.d/mysql.cnf:/etc/mysql/conf.d/mysql.cnf -v /Users/Nixus/Learn/mysql:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=root -p 3306:3306 --expose=3306 mysql:5.7.22 bash
docker run -it --name=employee -v /Users/Nixus/Learn:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=employee -p 3308:3306 mysql:5.7.22 bash
docker run -it --name=employee -v /Users/Nixus/Learn:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=employee mysql:5.7.22 bash
docker run -it --rm  mysql:5.7 bash
docker run -it --rm  php-redis-mysqli:latest sh
docker run -it --rm --env MYSQL_ROOT_PASSWORD=root -p 38790:3306 --expose=38790 mysql:5.7 bash
docker run -it --rm --env MYSQL_ROOT_PASSWORD=root -p 38790:3306 --expose=38790 mysql:5.7.22 bash
docker run -it --rm --name=employee -v /Users/Nixus/Learn/conf.d/mysql.cnf:/etc/mysql/conf.d/mysql.cnf -v /Users/Nixus/Learn/mysql:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=employee -p 3308:3306 mysql:5.7.22 bash
docker run -it --rm --name=employee -v /Users/Nixus/Learn/conf.d/mysql.cnf:/etc/mysql/conf.d/mysql.cnf -v /Users/Nixus/Learn:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=employee -p 3308:3306 mysql:5.7.22 bash
docker run -it --rm --name=employee -v /Users/Nixus/Learn/conf.d:/etc/mysql/conf.d -v /Users/Nixus/Learn:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=employee -p 3308:3306 mysql:5.7.22 bash
docker run -it --rm -e MYSQL_ROOT_PASSWORD=root -p 38790:3306 --expose=38790 mysql:5.7 bash
docker run -it --rm -e MYSQL_ROOT_PASSWORD=root -p 38790:3306 --expose=38790 mysql:5.7.22 bash
docker run -it --rm -e MYSQL_ROOT_PASSWORD=root mysql:5.7.22 bash
docker run -it --rm -p 8080:80 -v /Users/Nixus/tmp:/usr/share/nginx/html nginx:1.15.0-alpine sh
docker run -it --rm -v ./nginx:/etc/nginx nginx:1.15.0 bash
docker run -it --rm -v /Users/Nixus/Downloads/redis.conf:/home/redis.conf -v /Users/Nixus/Downloads/data:/data redis:4.0.10-alpine sh
docker run -it --rm -v /Users/Nixus/Factory\ of\ Docker/ffmpeg/tmp:/home ffmpeg-alpine:lastest sh
docker run -it --rm -v /Users/Nixus/Factory\ of\ Docker/ffmpeg/tmp:/home ffmpeg-alpine:latest sh
docker run -it --rm -v /Users/Nixus/Learn/conf.d/mysql.cnf:/etc/mysql/conf.d/mysql.cnf -v /Users/Nixus/Learn/mysql:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=root -P mysql:5.7.22 bash
docker run -it --rm -v /Users/Nixus/Learn/conf.d/mysql.cnf:/etc/mysql/conf.d/mysql.cnf -v /Users/Nixus/Learn/mysql:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=root -p 3306:3306 --expose=3306 mysql:5.7.22 bash
docker run -it --rm -v /Users/Nixus/Learn/conf.d/mysql.cnf:/etc/mysql/conf.d/mysql.cnf -v /Users/Nixus/Learn/mysql:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=root -p 38790:3306 --expose=38790 mysql:5.7.22 bash
docker run -it --rm -v /Users/Nixus/Learn/conf.d/mysql.cnf:/etc/mysql/conf.d/mysql.cnf -v /Users/Nixus/Learn/mysql:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=root -p 38790:3306 mysql:5.7.22 bash
docker run -it --rm -v /Users/Nixus/Learn:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=root -MYSQL_DATABASE=employee mysql:5.7.22 bash
docker run -it --rm -v /Users/Nixus/Learn:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=employee mysql:5.7.22 bash
docker run -it --rm -v /Users/Nixus/Learn:/var/lib/mysql mysql:5.7.22 bash
docker run -it --rm -v /Users/Nixus/Studio/mina/conf/redis/redis.conf:/home/redis/redis.conf -v /Users/Nixus/Downloads/data:/data redis:4.0.10-alpine sh
docker run -it --rm -v /Users/Nixus/Studio/mina/temp:/home c8eb sh
docker run -it --rm -v /Users/Nixus/Studio/mina/temp:/home mysql:5.7.22 bash
docker run -it --rm -v /Users/Nixus/Studio/mina/temp:/home php:7.0-fpm-alpine3.7 sh
docker run -it --rm -v /Users/Nixus/Studio/mina/temp:/home php:7.1-fpm-alpine3.7 sh
docker run -it --rm -v /Users/Nixus/Studio/mina/temp:/home php:7.1.19-fpm-alpine3.7 sh
docker run -it --rm -v /Users/Nixus/Studio/mina/temp:/home prpf:0.1 sh
docker run -it --rm -v /Users/Nixus/Studio/mina/temp:/home redis:4.0.10-alpine sh
docker run -it --rm -v /Users/Nixus/Studio/mysql/temp:/home/mysql mysql:5.7.22 bash
docker run -it --rm -v /Users/Nixus/Studio/temp:/usr/share/nginx/html nginx:1.15.0-alpine sh
docker run -it --rm -v /Users/Nixus/test/mysql:/etc/mysql mysql:5.7 bash
docker run -it --rm -v /Users/Nixus/test/mysql:/home mysql:5.7 bash
docker run -it --rm -v /Users/Nixus/test/nginx:/etc/nginx nginx:1.15.0 bash
docker run -it --rm -v /Users/Nixus/test/nginx:/usr/share/nginx/html nginx:1.15.0 bash
docker run -it --rm -v /Users/Nixus/test/redis:/home redis:4.0 bash
docker run -it --rm -v /Users/Nixus/test:/var/www/html php:7.1.19-fpm bash
docker run -it --rm alpine sh
docker run -it --rm centos:7.4 bash
docker run -it --rm centos:7.4.1708 bash
docker run -it --rm mysql:5.7.22 bash
docker run -it --rm mysql:autostart
docker run -it --rm mysql:autostart bash
docker run -it --rm nginx:1.15.0 bash
docker run -it --rm nginx:1.15.0-alpine sh
docker run -it --rm opencoconut/ffmpeg bash
docker run -it --rm opencoconut/ffmpeg sh
docker run -it --rm php-redis bash
docker run -it --rm php:7.1.18 bash
docker run -it --rm php:7.1.19-fpm
docker run -it --rm php:7.1.19-fpm bash
docker run -it --rm php:7.1.19-fpm-alpine bash
docker run -it --rm php:7.1.19-fpm-alpine sh
docker run -it --rm php:7.1.19-fpm-alpine3.7 sh
docker run -it --rm redis:4.0
docker run -it --rm redis:4.0.10-alpine sh
docker run -it 1e2839c3d5b9 bash
docker run -it centos bash
docker run -it imagine10255/centos6-lnmp-php56 /bin/bash
docker run -it latest /bin/bash
docker run -it mysql:5.7 --name mysql -e MYSQL_ROOT_PASSWORD=123456 bash
docker run -it mysql:5.7 -n mysql -e MYSQL_ROOT_PASSWORD=123456 bash
docker run -it mysql:5.7 -n mysql -e list
docker run -it mysql:5.7 -n mysql MYSQL_ROOT_PASSWORD=123456 bash
docker run -it mysql:8.0.11 bash
docker run -it nixus/php-7.1.19-fpm-alpine sh
docker run -it nixus/php-7.1.19-fpm-alpine:1.0 sh
docker run -it php:7.1.18  bash
docker run -it zzzshanghai/centos6-64bit
docker run -it zzzshanghai/centos6-64bit /bin/bash
docker run \n: 1529935563:0;docker container run \\n--rm \\n--name php\\nphp:7.1
docker run ecc74d703eca
docker run hello-world
docker run imagine10255/centos-lnmp-php56
docker run mysql:8.0.11 -it bash
docker run only
docker run only-centos
docker run php:7.1
docker run ubuntu:15.10 /bin/echo "hello world"
docker search -h
docker search centos
docker search centos6
docker search php
docker search php-fpm:7.1
docker search php:7.1
docker start
docker start --help
docker start e9742b7b80c8
docker start f4272
docker start f7aaa
docker stats
docker stats -h
docker stop 2abe72c03bbe
docker stop 2f3d
docker stop 35cc29cc135a
docker stop e9742b7b80c8
docker stop f4272
docker stop f7aaa
docker tag --help
docker tag -h
docker tag 784c nixus/php-fmp7.1.19-alpine3.7:1.0
docker tag php-redis-pdo nixus/php-redis-pdo:1.0
docker tag prpf:0.1 nixus/php-redis-pdo-ffmpeg:1.0
docker version
docker-compose
docker-compose -h
docker-compose -v
docker-compose command --help
docker-compose donw
docker-compose down
docker-compose exec workspace bash
docker-compose images
docker-compose logs
docker-compose ps
docker-compose ps -a
docker-compose restart
docker-compose start
docker-compose start -d
docker-compose status
docker-compose stop
docker-compose up
docker-compose up - d
docker-compose up --build
docker-compose up -d
docker-compose up -d nginx mysql
docker-machine
docker-machine ip
docker-machine ip --help
docker-machine ip mina_mysql_1
docker-machine ls
docker-machine ls -a
