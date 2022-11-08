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

#server-id
SERVERID=`grep server-id /config-center/ln/my.cnf`
if [ -z "$SERVERID" ]; then
        echo 'has no server-id, add it'
		sed -i "/\[mysqld\]/ a server-id = $RANDOM" /config-center/ln/my.cnf
		echo 'the added server-id line is: '`grep server-id /config-center/ln/my.cnf`
else
        echo 'the old server-id line is: '$SERVERID
        sed -i "s/$SERVERID/server-id = $RANDOM/g" /config-center/ln/my.cnf
		echo 'the new server-id line is: '`grep server-id /config-center/ln/my.cnf`
fi

#report-host
REPORTHOST=`grep report-host /config-center/ln/my.cnf`
if [ -z "$REPORTHOST" ]; then
        echo 'has no report-host, add it'
        sed -i "$ a\report-host = `hostname -i`" /config-center/ln/my.cnf
		echo 'the added report-host line is: '`grep report-host /config-center/ln/my.cnf`
else
        echo 'the old report-host line is: '$REPORTHOST
        sed -i "s/$REPORTHOST/report-host = `hostname -i`/g" /config-center/ln/my.cnf
		echo 'the new report-host line is: '`grep report-host /config-center/ln/my.cnf`
fi

# start mysqld
docker-entrypoint.sh $1 &

# foreground process to keep container running
tail -f /var/log/mysql/error.log

