#!/usr/bin/env bash
curl http://192.168.59.103:8080/dbtest/
curl http://192.168.59.103:8080/myweb/
curl http://192.168.59.103/java/dbtest/
curl http://192.168.59.103/java/myweb/
curl http://192.168.59.103/java/myweb/webjars/bootstrap/3.3.4/css/bootstrap.min.css
curl -v -b "ChannelCode=test;ChannelSecretkey=a8152b13f4ef9daca84cf981eb5a7907"  http://192.168.59.103/api
curl -v -b "ctoken=testf97a93b6e5e08843a7c825a53bdae246" http://192.168.59.103/api
mysql -h 192.168.59.103 -ujava -pjava -Djavatest --skip-column-names --raw < mysql2redis.sql |redis-cli -h 192.168.59.103 --pipe

#渠道管理配置
curl http://192.168.59.103:32786/mychannel.html