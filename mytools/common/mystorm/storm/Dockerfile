FROM supermy/docker-jre:7

MAINTAINER supermy <springclick@gmail.com>

RUN echo 'root:supermy' | chpasswd

#RUN sed -i '1,7d' /etc/apt/sources.list

#更换比较快的镜像
#RUN echo 'deb http://mirrors.sohu.com/debian/ wheezy main non-free contrib '>>/etc/apt/sources.list
#RUN echo 'deb http://mirrors.sohu.com/debian/ wheezy-proposed-updates main contrib non-free '>>/etc/apt/sources.list
#RUN echo 'deb http://mirrors.sohu.com/debian-security/ wheezy/updates main contrib non-free '>>/etc/apt/sources.list
#RUN echo 'deb-src http://mirrors.sohu.com/debian/ wheezy main non-free contrib '>>/etc/apt/sources.list
#RUN echo 'deb-src http://mirrors.sohu.com/debian/ wheezy-proposed-updates main contrib non-free '>>/etc/apt/sources.list
#RUN echo 'deb-src http://mirrors.sohu.com/debian-security/ wheezy/updates main contrib non-free '>>/etc/apt/sources.list

#RUN cat /etc/apt/sources.list

RUN apt-get update -y && apt-get install --no-install-recommends -y -q curl sudo supervisor

#RUN mkdir /var/run/sshd
#RUN sed -i 's/PermitRootLogin without-password/PermitRootLogin yes/' /etc/ssh/sshd_config

RUN wget -q -O - http://mirrors.sonic.net/apache/storm/apache-storm-0.9.3/apache-storm-0.9.3.tar.gz | tar -xzf - -C /opt

ENV STORM_HOME /opt/apache-storm-0.9.3
RUN groupadd storm; useradd --gid storm --home-dir /home/storm --create-home --shell /bin/bash storm; chown -R storm:storm $STORM_HOME; mkdir /var/log/storm ; chown -R storm:storm /var/log/storm

RUN ln -s $STORM_HOME/bin/storm /usr/bin/storm

ADD storm.yaml $STORM_HOME/conf/storm.yaml
ADD cluster.xml $STORM_HOME/logback/cluster.xml
ADD config-supervisord.sh /usr/bin/config-supervisord.sh
ADD start-supervisor.sh /usr/bin/start-supervisor.sh 

RUN ls -hl /usr/bin/start-supervisor.sh

RUN echo [supervisord] | tee -a /etc/supervisor/supervisord.conf ; echo nodaemon=true | tee -a /etc/supervisor/supervisord.conf
#RUN echo [supervisord] >> /etc/supervisor/supervisord.conf ; echo nodaemon=true >> /etc/supervisor/supervisord.conf
#RUN cat /etc/supervisor/supervisord.conf
