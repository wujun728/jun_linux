#!/usr/bin/env bash
curl http://192.168.59.103:8080/dbtest/
curl http://192.168.59.103:8080/myweb/
curl http://192.168.59.103:8080/myweb/webjars/bootstrap/3.3.4/css/bootstrap.min.css


#redis 缓存的项目,redis 进行session 共享
fig -f fig-redis.yml up -d && fig -f fig-redis.yml ps
#测试redis session 共享
curl http://192.168.59.103:32789/dbtest/token.jsp
curl http://192.168.59.103:32788/dbtest/token.jsp
