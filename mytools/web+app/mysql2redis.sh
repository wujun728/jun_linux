#mysql 的数据同步到redis;同步时间间隔由crontab 控制
#–raw: 使mysql不转换字段值中的换行符。
#–skip-column-names: 使mysql输出的每行中不包含列名。
#单独执行 echo -en '*3\r\n$3\r\nSET\r\n$3\r\nkey\r\n$5\r\nvalue\r\n' | redis-cli --pipe
#mysql -h 127.0.0.1 -uroot -pmy67163 -Dtest --skip-column-names --raw <mysql2redis.sql |redis-cli --pipe
mysql -h 192.168.59.103 -ujava -pjava -Djavatest --skip-column-names --raw < mysql2redis.sql |redis-cli -h 192.168.59.103 --pipe
mysql -h 172.17.0.3 -ujava -pjava -Djavatest --skip-column-names --raw <mysql2redis.sql |redis-cli --pipe