#!/bin/bash

# 远程主机名称
REMOTE_HOST="10.100.19.104"
# 远程主机用户
REMOTE_USER=yanfa
# OPT_DIR
OPT_DIR=/home/yanfa/opt
# TOMCAT_NAME
TOMCAT_NAME=apache-tomcat-7.0.77
# 远程主机Tomcat安装目录
TOMCAT_DIR=${OPT_DIR}"/"${TOMCAT_NAME}

# JDK_NAME
JDK_NAME=jdk-7u80-linux-x64


# 本地文件目录
LOCAL_DIR=/Users/TaoBangren/eagle/dubbokeeper/deploy

# Tomcat安装
install_tomcat(){
   for host in ${REMOTE_HOST};do
        echo "创建opt目录"
        ssh ${REMOTE_USER}@${host} "mkdir -p" ${OPT_DIR}

        echo "上传tomcat安装包"
        scp ${LOCAL_DIR}"/"${TOMCAT_NAME}".tar.gz" ${REMOTE_USER}@${host}:${OPT_DIR}

        echo "解压tomcat安装包"
        ssh ${REMOTE_USER}@${host} "cd" ${OPT_DIR} "&& tar zxvf "${TOMCAT_NAME}".tar.gz"
   done
}

# JDK安装
install_jdk(){
   for host in ${REMOTE_HOST};do
        echo "上传JDK安装包"
        scp ${LOCAL_DIR}"/"${JDK_NAME}".rpm" ${REMOTE_USER}@${host}:${OPT_DIR}

        echo "安装JDK"
        ssh ${REMOTE_USER}@${host} "cd" ${OPT_DIR} "&& sudo rpm -ivh "${JDK_NAME}".rpm"

        echo "检查JDK是否成功"
        ssh ${REMOTE_USER}@${host} "java -version"
   done
}

# 代码执行选项设置
main(){
#   install_tomcat;
   install_jdk;
}

main
