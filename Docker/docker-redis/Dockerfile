FROM centos:centos6
MAINTAINER qm <juapk@qq.com>

RUN yum update -y

# install redis
RUN yum install -y curl tar make gcc && \
    cd /usr/local/src && \
    curl -O http://download.redis.io/releases/redis-2.8.9.tar.gz && \
    tar xf redis-2.8.9.tar.gz && \
    cd redis-2.8.9 && \
    make && \
    make install

EXPOSE 6379
CMD ["/usr/local/bin/redis-server"]