web（极限性能挖掘，可快速扩充）
====================

介绍
---------------------
nginx(tengine)+tomcat+mysql+redis 集群
一键构造，一键启动，一键数据初始化。

>   nginx 整合HttpRedis2Module/lua-resty-redis完成，http方式访问redis;
>   mysql2redis.sh 将mysql 的数据同步到redis,通过linux 的crontab 进行配置；
>   增加webjars and nginx4webjars 缓存配置
>
>开发调试脚本
>
>tail -f docker-share/logs/web/error.log
>
>telnet 192.168.59.103 6379/monitor/keys */set key value/get key/hget rowkey fieldkey
>
>curl -v -b "ChannelCode=test;ChannelSecretkey=a8152b13f4ef9daca84cf981eb5a7907"  http://192.168.59.103/api
>
>curl -v -b "ctoken=testf97a93b6e5e08843a7c825a53bdae246" http://192.168.59.103/api
>
>mysql -h 192.168.59.103 -ujava -pjava -Djavatest --skip-column-names --raw < mysql2redis.sql |redis-cli -h 192.168.59.103 --pipe
>
> ## end
