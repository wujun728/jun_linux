docker rm -f mysql-master1
docker run -d --name mysql-master1 \
  -e MYSQL_ROOT_PASSWORD=root \
  -e MYSQL_REPLICATION_USER=repl \
  -e MYSQL_REPLICATION_PASSWORD=repl \
  -e XTRABACKUP=y \
  -e BACKUP_INTERVAL_SEC=30 \
  -e BACKUP_DIR=/xtrabackup-data \
  -e POD_NAME=testpod \
  -v `pwd`/my.cnf.tmpl:/config-center/ln/my.cnf \
  mysql-5.7.16-master-xb-cm:20161129

