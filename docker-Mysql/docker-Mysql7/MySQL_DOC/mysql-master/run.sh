#!/bin/bash

# link mysql conf
ln -sf /config-center/ln/my.cnf /etc/mysql/my.cnf

# link mysql init sql
for f in /config-center/init/*; do
    case "$f" in
        *.sh|*.sql|*.sql.gz)
            echo $f
            ln -sf $f /docker-entrypoint-initdb.d/${f##*/}
            ;;
        *)        echo "$0: ignoring $f" ;;
        esac
done

# start mysqld
docker-entrypoint.sh $1 &

# start xtrabackup if $XTRABACKUP = Y/y
if [[ "$XTRABACKUP" = "Y" || "$XTRABACKUP" = "y" ]]; then
	echo "starting xtrabackup..."
	cd /home/xtrabackup/cron/bin/
	./runBackup.sh & >> backup.log
	echo "xtrabackup started."
else
    echo "XTRABACKUP not set, xtrabackup will not run."
fi

# foreground process to keep container running
tail -f /var/log/mysql/error.log

