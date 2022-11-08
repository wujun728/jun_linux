backupIntervalMin=$BACKUP_INTERVAL_SEC
echo "PID of this script:$$" >> backup.log
a=$(date +%s)
backup_dir=$BACKUP_DIR/$POD_NAME
mkdir -p $backup_dir
cp -r /home/xtrabackup/cron/conf $backup_dir
cp -r /home/xtrabackup/cron/log $backup_dir
cp -r /home/xtrabackup/cron/var $backup_dir

while [ "1" = "1" ];do
  b=$(date +%s)
  declare -i c=$b-$a
  if [ "$c" -ge "$backupIntervalMin" ];then
    ./mysql_increment_hot_backup.sh
    a=$(date +%s)
  fi
  sleep 5
done
