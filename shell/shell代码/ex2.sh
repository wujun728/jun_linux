#!/bin/sh
/bin/date +%F >> /test/shelldir/ex2.info
echo "disk info:" >> /test/shelldir/ex2.info
/bin/df -h >> /test/shelldir/ex2.info
echo >> /test/shelldir/ex2.info
echo "online users:" >> /test/shelldir/ex2.info
/usr/bin/who | /bin/grep -v root >> /test/shelldir/ex2.info
echo "memory info:" >> /test/shelldir/ex2.info
/usr/bin/free -m >> /test/shelldir/ex2.info
echo >> /test/shelldir/ex2.info
#write root
/usr/bin/write root < /test/shelldir/ex2.info && /bin/rm /test/shelldir/ex2.info
#crontab -e
#0 9 * * 1-5 /bin /sh /test/ex2.sh
