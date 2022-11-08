#!/bin/bash

# 设置时间变量
CTIME=$(date "+%Y%m%d%H%M")
# SVN地址
SVN_URL=svn://118.26.169.20/eagle
# 项目名称，建议和gitlab仓库名称一致
project=shark
# 项目SVN地址
PROJECT_SVN="$SVN_URL"/"$project"
# 本地代码目录（gitlab拉取代码后存放目录）
CODE_DIR=/Users/TaoBangren/eagle/"$project"/trunk
# 临时代码目录，用来修改配置文件和编译打包代码
TMP_DIR=/Users/TaoBangren/eagle/tmp/"$project"
# 用来存放war包
WAR_DIR=/Users/TaoBangren/eagle/war/"$project"

# 远程主机名称
REMOTE_HOST="10.100.19.106"
# 远程主机用户
REMOTE_USER=yanfa

# 远程主机应用目录
REMOTE_APP_DIR=/home/yanfa/deploy/webapps/
# 远程主机war包存放目录
REMOTE_WAR_DIR=/home/yanfa/deploy/war
# 远程主机应用代码目录
REMOTE_CODE_TMP=/home/yanfa/deploy/code

# 上线日志
DEPLOY_LOG=/data/log/pro_log.log

# 脚本使用帮助
usage(){
   echo $"Usage: $0 [deploy tag | rollback_list | rollback_pro ver]"
}

# 拉取代码
svn_pro(){
   if [ $# -lt 1 ];then
        echo "请传入tag"
        exit 1
   fi
   tag=$1

   if [ ! -d "$CODE_DIR" ];then
        mkdir -p ${CODE_DIR} && cd ${CODE_DIR} && svn co ${PROJECT_SVN} .
   else
        cd ${CODE_DIR} && svn up
   fi

   if [ $? != 0 ];then
        echo "拉取代码失败"
        exit 10
   else
        echo "拉取代码完成"
   fi

   # 推送代码到临时目录
   if [ ! -d "$TMP_DIR" ];then
        mkdir -p ${TMP_DIR}
   fi
   /Users/TaoBangren/opt/apache-maven-3.2.1/bin/mvn clean 2>/dev/null >/dev/null && rsync -avz --delete ${CODE_DIR}/ ${TMP_DIR}/ 2>/dev/null >/dev/null
}

# 打包代码
tar_pro(){
   echo "本地打包代码"
   if [ ! -d "$WAR_DIR" ];then
        mkdir -p ${WAR_DIR}
   fi
   cd ${TMP_DIR} && /Users/TaoBangren/opt/apache-maven-3.2.1/bin/mvn clean compile install -Pdev -Dmaven.test.skip=true && cp shark-api/target/shark-api.war "$WAR_DIR"/shark-api_"$CTIME".war
}

# 推送war包到远端服务器
rsync_pro(){
   echo "推送war包到远端服务器"

   for host in ${REMOTE_HOST};do
    scp "$WAR_DIR"/shark-api_"$CTIME".war ${REMOTE_USER}@${host}:${REMOTE_WAR_DIR}
   done
}

# 解压代码包
solution_pro(){
   echo "解压代码包"
   for host in ${REMOTE_HOST};do
    ssh ${REMOTE_USER}@${host} "unzip "${REMOTE_WAR_DIR}"/shark-api_"${CTIME}".war -d "${REMOTE_CODE_TMP}"/shark-api_"${CTIME}""
   done
}

# api测试
test_pro(){
   # 运行api测试脚本，如果api测试有问题，则退出部署
   if [ $? != 0 ];then
    echo "API测试存在问题，退出部署"
    exit 10
   fi
}


# 部署代码
deploy_pro(){
   echo "部署代码"
   for host in ${REMOTE_HOST};do
    ssh ${REMOTE_USER}@${host} "sh /home/yanfa/opt/apache-tomcat-7.0.77/bin/shutdown.sh"
    ssh ${REMOTE_USER}@${host} "rm -rf" ${REMOTE_APP_DIR}"/shark-api && ln -s "${REMOTE_CODE_TMP}"/shark-api_"${CTIME} ${REMOTE_APP_DIR}"/shark-api"
    echo "重启$host"
    ssh ${REMOTE_USER}@${host} "sh /home/yanfa/opt/apache-tomcat-7.0.77/bin/startup.sh && tail -f /home/yanfa/opt/apache-tomcat-7.0.77/logs/catalina.out"
    sleep 3
   done
}

# 列出可以回滚的版本
rollback_list(){
  echo "------------可回滚版本-------------"
  ssh ${REMOTE_USER}@${REMOTE_HOST} "ls -r "${CODE_TMP}" | grep -o $project.*"
}

# 回滚代码
rollback_pro(){
  echo "回滚中"
  for host in ${REMOTE_HOST};do
    ssh haproxy "echo "disable server ${project}/${host}" | /usr/bin/socat /var/lib/haproxy/stats stdio"
    ssh ${REMOTE_USER}@${host} "rm -rf $REMOTE_CODE_DIR"
    ssh ${REMOTE_USER}@${host} "ln -s "${CODE_TMP}"$1/ $REMOTE_CODE_DIR"
    ssh ${REMOTE_USER}@${host} "/etc/init.d/tomcat restart"
    sleep 3
    ssh haproxy "echo "enable server ${project}/${host}" | /usr/bin/socat /var/lib/haproxy/stats stdio"
  done
}

# 记录日志
record_log(){
  echo "$CTIME 主机:$REMOTE_HOST 项目:$project tag:$1" >> ${DEPKOY_LOG}
}

# 代码执行选项设置
main(){
  case $1 in
   deploy)
   svn_pro $2;
   tar_pro;
   rsync_pro;
   solution_pro;
   deploy_pro;
#   record_log $2;
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
