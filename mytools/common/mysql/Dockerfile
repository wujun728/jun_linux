#version 5.6.22
FROM mysql:latest

RUN  sed -i '/client\]/a  max_allowed_packet = 48M ' /etc/mysql/my.cnf
RUN  sed -i '/mysqld\]/a   \
event_scheduler=ON   \n\
default-storage-engine=INNODB   \n\
#default-character-set=utf8    \n\
character-set-server = utf8    \n\
max_allowed_packet = 16M    \n\
wait_timeout	= 500    \n\
interactive_timeout	= 500    \n\
connect_timeout = 20    \n\

' /etc/mysql/my.cnf

#配置时区
RUN echo "Asia/Shanghai" > /etc/timezone
RUN dpkg-reconfigure -f noninteractive tzdata

RUN  more /etc/mysql/my.cnf
