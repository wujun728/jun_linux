FROM    debian:7.8

#2015-01-24修订,中文语言
MAINTAINER supermy <springclick@gmail.com>

#RUN sed -i '1,3d'   /etc/apt/sources.list

#RUN sed -i '4a \
#    deb http://mirrors.163.com/debian/ wheezy main non-free contrib \n \
#    deb http://mirrors.163.com/debian/ wheezy-proposed-updates main contrib non-free \n \
#    deb http://mirrors.163.com/debian-security/ wheezy/updates main contrib non-free \n \
#    deb-src http://mirrors.163.com/debian/ wheezy main non-free contrib \n \
#    deb-src http://mirrors.163.com/debian/ wheezy-proposed-updates main contrib non-free \n \
#    deb-src http://mirrors.163.com/debian-security/ wheezy/updates main contrib non-free \n \
#	\
#    ' /etc/apt/sources.list

# 慢
#    deb http://ftp.sjtu.edu.cn/debian/ wheezy main non-free contrib \n \
#    deb http://ftp.sjtu.edu.cn/debian/ wheezy-proposed-updates main contrib non-free \n \
#    deb http://ftp.sjtu.edu.cn/debian-security/ wheezy/updates main contrib non-free \n \
#    deb-src http://ftp.sjtu.edu.cn/debian/ wheezy main non-free contrib \n \
#    deb-src http://ftp.sjtu.edu.cn/debian/ wheezy-proposed-updates main contrib non-free \n \
#    deb-src http://ftp.sjtu.edu.cn/debian-security/ wheezy/updates main contrib non-free \n \

#RUN cat /etc/apt/sources.list


RUN apt-get -y update  &&  apt-get install -qq -y curl wget sudo

RUN     apt-get -y install locales && \
        sed -i 's/# zh_CN.UTF-8 UTF-8/zh_CN.UTF-8 UTF-8/' /etc/locale.gen && \
        locale-gen && \
        update-locale LC_ALL= "zh_CN.UTF-8" && \
        export LANGUAGE=zh_CN && \
        export LANG=zh_CN.UTF-8 && \
        locale

RUN sed -i '$a \
    * soft nproc 65536 \
    * hard nproc 65536  \
    * soft nofile 65536  \
    * hard nofile 65536  \
    '  \
    /etc/security/limits.conf


#RUN sed -i '$a \
#        fs.file-max = 767246   \
#        fs.aio-max-nr = 1048576  \
#        ' /etc/sysctl.conf

RUN sed -i '$a \
            ulimit -s 4096   \
            ulimit -m 15728640  \
        ' /etc/profile


RUN apt-get -y update && apt-get install -qq -y unzip

#--net=none
RUN wget https://github.com/jpetazzo/pipework/archive/master.zip
RUN unzip master.zip

RUN cp pipework-master/pipework  /usr/local/bin/
RUN chmod +x /usr/local/bin/pipework
#RUN pipework kbr0 test1 172.17.1.3/24@172.17.1.1
#RUN brctl show
#RUN ip a

RUN    apt-get clean && \
      rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN echo "Asia/Shanghai" > /etc/timezone
RUN dpkg-reconfigure -f noninteractive tzdata

ENV LANG       zh_CN.UTF-8
ENV LANGUAGE   zh_CN:zh

#userage
#docker build -t supermy/docker-debian:7 mydebian
