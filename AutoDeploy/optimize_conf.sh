#!/bin/bash

# 远程主机名称
REMOTE_HOST="10.100.19.106"
# 远程主机用户
REMOTE_USER=yanfa
# 远程主机Tomcat安装目录
TOMCAT_DIR=/home/yanfa/opt/apache-tomcat-7.0.77

# 本地文件目录
LOCAL_DIR=/Users/TaoBangren/eagle/shark/trunk/deploy

# Tomcat优化配置
optimize_tomcat(){
   for host in ${REMOTE_HOST};do
        echo "停服..."
        ssh ${REMOTE_USER}@${host} "sh" ${TOMCAT_DIR}"/bin/shutdown.sh"

        echo "删除webapps下所有文件"
        ssh ${REMOTE_USER}@${host} "rm -rf" ${TOMCAT_DIR}"/webapps/*"

        echo "删除server/webapps下所有文件"
        ssh ${REMOTE_USER}@${host} "rm -rf" ${TOMCAT_DIR}"/server/webapps/*"

        echo "上传server.xml"
        ssh ${REMOTE_USER}@${host} "cd" ${TOMCAT_DIR}"/conf && mv server.xml server.xml.bak"
        scp ${LOCAL_DIR}"/server.xml" ${REMOTE_USER}@${host}:${TOMCAT_DIR}"/conf/"

        echo "上传catalina.sh"
        ssh ${REMOTE_USER}@${host} "cd" ${TOMCAT_DIR}"/bin && mv catalina.sh catalina.sh.bak"
        scp ${LOCAL_DIR}"/catalina.sh" ${REMOTE_USER}@${host}:${TOMCAT_DIR}"/bin/"

        echo "上传logging.properties"
        ssh ${REMOTE_USER}@${host} "cd" ${TOMCAT_DIR}"/conf && mv logging.properties logging.properties.bak"
        scp ${LOCAL_DIR}"/logging.properties" ${REMOTE_USER}@${host}:${TOMCAT_DIR}"/conf/"
   done
}

# 代码执行选项设置
main(){
  case $1 in
   tomcat)
   optimize_tomcat;
   ;;
   rollback_list)
   rollback_list;
   ;;
   rollback_pro)
   rollback_pro $2;
   record_log;
   ;;
   *)
   usage;
   esac
}
main $1 $2
