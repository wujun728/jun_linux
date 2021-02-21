#!/usr/bin/env bash
docker build -t supermy/docker-mynginx:2.1 mynginx

#默认为tomcat-redis-session
docker build -t supermy/docker-mytomcat:7 mytomcat

docker build -t supermy/docker-tomcat-redis:7 -f mytomcat/Dockerfile-redis mytomcat
docker build -t supermy/docker-tomcat-memcache:7 -f mytomcat/Dockerfile-memcache mytomcat


docker build -t supermy/docker-springboot springboot
