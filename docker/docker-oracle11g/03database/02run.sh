#!/usr/bin/env bash

set -e

# set envirionment
PWD=`pwd`
BASE_DIR="${PWD}"
SOURCE="$0"
while [ -h "$SOURCE"  ]; do
    BASE_DIR="$( cd -P "$( dirname "$SOURCE"  )" && pwd  )"
    SOURCE="$(readlink "$SOURCE")"
    [[ $SOURCE != /*  ]] && SOURCE="$BASE_DIR/$SOURCE"
done
BASE_DIR="$( cd -P "$( dirname "$SOURCE"  )" && pwd  )"

cd ${BASE_DIR}

######################################################################################
# docker run [OPTIONS] IMAGE [COMMAND] [ARG...]
# OPTIONS说明:
# -a stdin : 指定标准输入输出内容类型，可选 STDIN/STDOUT/STDERR 三项
# -d : 后台运行容器，并返回容器ID
# -i : 以交互模式运行容器，通常与 -t 同时使用
# -t : 为容器重新分配一个伪输入终端，通常与 -i 同时使用
# --name="nginx-lb" : 为容器指定一个名称
# --dns 8.8.8.8 : 指定容器使用的DNS服务器，默认和宿主一致
# --dns-search example.com : 指定容器DNS搜索域名，默认和宿主一致
# -h "mars" : 指定容器的hostname
# -e username="ritchie" : 设置环境变量
# --env-file=[] : 从指定文件读入环境变量
# --cpuset="0-2" or --cpuset="0,1,2" : 绑定容器到指定CPU运行
# -m : 设置容器使用内存最大值
# --net="bridge" : 指定容器的网络连接类型，支持 bridge/host/none/container: 四种类型
# --link=[] : 添加链接到另一个容器
# --expose=[] : 开放一个端口或一组端口
######################################################################################

# do run
docker run -it \
           --rm \
           --memory=2g \
           --shm-size=2g \
           --name="oracle-11g-ee-database" \
           --hostname="database" \
           -e ENABLE_EM="false" \
           -p 1521:1521 \
           -p 1158:1158 \
           192.168.8.251/library/oracle-11g-ee:database \
          "bash"
