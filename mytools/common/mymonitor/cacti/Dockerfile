FROM supermy/docker-debian:7

MAINTAINER supermy"springclick@gmail.com"


RUN sed -i '1,3d'   /etc/apt/sources.list
RUN echo '#hello'>> /etc/apt/sources.list

RUN sed -i '1a \
    deb http://mirrors.163.com/debian/ wheezy main non-free contrib \n \
    deb http://mirrors.163.com/debian/ wheezy-proposed-updates main contrib non-free \n \
    deb http://mirrors.163.com/debian-security/ wheezy/updates main contrib non-free \n \
    deb-src http://mirrors.163.com/debian/ wheezy main non-free contrib \n \
    deb-src http://mirrors.163.com/debian/ wheezy-proposed-updates main contrib non-free \n \
    deb-src http://mirrors.163.com/debian-security/ wheezy/updates main contrib non-free \n \
    ' /etc/apt/sources.list


#安装cacti环境,会自动安装mysql
#snmp抓到数据不是存储在mysql中，而是存在rrdtool生成的rrd文件中
#rrdtool的作用只是存储数据和画图
RUN apt-get update
RUN apt-get install  snmpd apache2 -qqy
RUN apt-get install cacti  cacti-spine -qqy

##startup scripts  
#Pre-config scrip that maybe need to be run one time only when the container run the first time .. using a flag to don't 
#run it again ... use for conf for service ... when run the first time ...
RUN mkdir -p /etc/my_init.d
COPY startup.sh /etc/my_init.d/startup.sh
RUN chmod +x /etc/my_init.d/startup.sh


##Adding Deamons to containers

RUN mkdir /etc/service/apache2
COPY apache2.sh /etc/service/apache2/run
RUN chmod +x /etc/service/apache2/run

RUN mkdir /etc/service/mysqld
COPY mysqld.sh /etc/service/mysqld/run
RUN chmod +x /etc/service/mysqld/run

# snmpd 进行数据采集
RUN mkdir /etc/service/snmpd
COPY snmpd.sh /etc/service/snmpd/run
RUN chmod +x /etc/service/snmpd/run

#建立数据库和用户，外置处理。
#pre-config scritp for different service that need to be run when container image is create 
#maybe include additional software that need to be installed ... with some service running ... like example mysqld
COPY pre-conf.sh /sbin/pre-conf
RUN chmod +x /sbin/pre-conf \
    && /bin/bash -c /sbin/pre-conf \
    && rm /sbin/pre-conf

##scritp that can be running from the outside using docker-bash tool ...
## for example to create backup for database with convitation of VOLUME   dockers-bash container_ID backup_mysql
COPY backup.sh /sbin/backup
RUN chmod +x /sbin/backup
VOLUME /var/backups


#add files and script that need to be use for this container
#include conf file relate to service/daemon 
#additionsl tools to be use internally 
COPY snmpd.conf /etc/snmp/snmpd.conf 
COPY cacti.conf /etc/dbconfig-common/cacti.conf
COPY debian.conf /etc/cacti/debian.php
COPY spine.conf /etc/cacti/spine.conf

# to allow access from outside of the container  to the container service
# at that ports need to allow access from firewall if need to access it outside of the server. 
EXPOSE 161

#creatian of volume 
#VOLUME 

# Use baseimage-docker's init system.
CMD ["/sbin/my_init"]
