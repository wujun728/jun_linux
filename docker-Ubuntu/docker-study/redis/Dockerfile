# http://git.oschina.net/ahern88/docker-redis
FROM        ubuntu:14.04.3LTS

RUN         apt-get update

RUN         apt-get -y install redis-server

EXPOSE      6379

ENTRYPOINT  ["/usr/bin/redis-server"]

# Access Example
# redis-cli -h host -p open_port