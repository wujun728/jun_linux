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
# docker build [OPTIONS] PATH | URL | -
# OPTIONS说明:
# --build-arg=[] : 设置镜像创建时的变量
# --cpu-shares : 设置 cpu 使用权重
# --cpu-period : 限制 CPU CFS周期
# --cpu-quota : 限制 CPU CFS配额
# --cpuset-cpus : 指定使用的CPU id
# --cpuset-mems : 指定使用的内存 id
# --disable-content-trust : 忽略校验，默认开启
# -f : 指定要使用的Dockerfile路径
# --force-rm : 设置镜像过程中删除中间容器
# --isolation : 使用容器隔离技术
# --label=[] : 设置镜像使用的元数据
# -m : 设置内存最大值
# --memory : 设置内存最大值
# --memory-swap : 设置Swap的最大值为内存+swap,"-1"表示不限swap
# --no-cache : 创建镜像的过程不使用缓存
# --pull : 尝试去更新镜像的新版本
# -q : 安静模式，成功后只输出镜像ID
# --rm : 设置镜像成功后删除中间容器
# --shm-size : 设置/dev/shm的大小，默认值是64M
# --ulimit : Ulimit配置
# eg:
# docker build --rm \
#              --force-rm \
#              --no-cache \
#              --memory=2g \
#              --shm-size=2g \
#              -t 192.168.8.251/library/oracle-11g-ee:database \
#              -f dockerfile .
######################################################################################

# set env
imagetag="192.168.8.251/library/oracle-11g-ee:database"
dockerfile="dockerfile"

# do build
docker build --rm \
             --force-rm \
             --no-cache \
             --memory=2g \
             --shm-size=2g \
             -t ${imagetag} \
             -f ${dockerfile} .
