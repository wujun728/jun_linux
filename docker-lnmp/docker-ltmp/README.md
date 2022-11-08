# ltmp
基于dockerfile构建centos7.4+ tengine2.1.2+ php7+ php扩展环境

centOS7.4.1708 + tengine-2.1.2 + php-7.0.17 + PHP扩展(、PDO、PDO_MYSQL、gd、curl、mysqli、pcntl、soap、Redis、mongodb、memcached、gearman、zeromq、ICE)

php扩展
~~~
redis
~~~
由于php源代码太大 需自己到官网下载相应版本 放到src目录下
~~~
wget -O ./src/php-7.0.17.tar.gz http://cn2.php.net/get/php-7.0.17.tar.gz/from/this/mirror 

docker build -t lnmp .

docker run -d -p 88:80 -p 1022:22 lnmp

ssh root@127.0.0.1:1022 -p

~~~

用户名:root
密码:123465
