#!/usr/bin/env bash
# 通用工具构造
cd common
sh build.sh
cd ..

#分布式系统build
docker build -t supermy/docker-mongodb:3.0.4 /Users/moyong/project/env-myopensource/3-tools/mytools/mymongodb/base/
docker build -t supermy/docker-mynginx:2.1 /Users/moyong/project/env-myopensource/3-tools/mytools/web+app/mynginx/
docker build -t supermy/docker-mytomcat:7 /Users/moyong/project/env-myopensource/3-tools/mytools/web+app/mytomcat/

cd /Users/moyong/project/env-myopensource/mytools/web+app/mynginx
fig stop && fig rm --force -v && fig build

cd /Users/moyong/project/env-myopensource/mytools/web+app/mytomcat
fig stop && fig rm --force -v && fig build

cd /Users/moyong/project/env-myopensource/mytools/web+app
fig stop && fig rm --force -v && fig build


#云平台build
#cd /Users/moyong/project/env-myopensource/mytools/mycloud
#fig stop && fig rm --force -v && fig build

#cd /Users/moyong/project/env-myopensource/mytools/mycloud-hadoop
#fig stop && fig rm --force -v && fig build

#cd /Users/moyong/project/env-myopensource/mytools/mycloud-hbase
#fig stop && fig rm --force -v && fig build

#cd /Users/moyong/project/env-myopensource/mytools/mycloud-zookeeper
#fig stop && fig rm --force -v && fig build

#cd /Users/moyong/project/env-myopensource/mytools/mytomcat
#fig stop && fig rm --force -v && fig build
