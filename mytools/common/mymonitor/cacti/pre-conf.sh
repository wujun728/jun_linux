#!/bin/bash

/usr/bin/mysqld_safe &
 sleep 10s

 mysqladmin -u root password mysqlpsswd
 mysqladmin -u root -pmysqlpsswd reload
 mysqladmin -u root -pmysqlpsswd create cacti
 mysql -u root -pmysqlpsswd cacti < /usr/share/cacti/conf_templates/cacti.sql

 echo "GRANT ALL ON cacti.* TO cacti@localhost IDENTIFIED BY '9PIu8AbWQSf8'; flush privileges; " | mysql -u root -pmysqlpsswd 


killall mysqld
sleep 10s
