#docker-redis

docker pull redis:6.2.6

docker run -p 6379:6379 --name redis666 -v /home/redis/conf/redis.conf:/etc/redis/redis.conf -v /home/redis/data:/data -d redis:6.2.6 redis-server /etc/redis/redis.conf --appendonly yes

docker run -itd --name redis-7 -p 6379:6379 redis:6.0
docker run -itd --name redis-test -p 6379:6379 redis
docker exec -it redis-test /bin/bash

 


