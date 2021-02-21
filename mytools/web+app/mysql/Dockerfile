#转移到common/mysql
FROM    mysql:latest
MAINTAINER supermy <springclick@gmail.com>


#配置时区
RUN echo "Asia/Shanghai" > /etc/timezone
RUN dpkg-reconfigure -f noninteractive tzdata
RUN mysql_upgrade -u root -p --force
