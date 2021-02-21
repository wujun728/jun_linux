#FROM cpuguy83/ubuntu
#docker build -t supermy/mymonitor:latest -f Dockerfile-nagios .

FROM supermy/docker-debian:7

#RUN export http_proxy=http://192.168.0.121:8087

RUN sed -i '1,3d'   /etc/apt/sources.list

RUN sed -i '4a \
    deb http://mirrors.163.com/debian/ wheezy main non-free contrib \n \
    deb http://mirrors.163.com/debian/ wheezy-proposed-updates main contrib non-free \n \
    deb http://mirrors.163.com/debian-security/ wheezy/updates main contrib non-free \n \
    deb-src http://mirrors.163.com/debian/ wheezy main non-free contrib \n \
    deb-src http://mirrors.163.com/debian/ wheezy-proposed-updates main contrib non-free \n \
    deb-src http://mirrors.163.com/debian-security/ wheezy/updates main contrib non-free \n \
	\
    ' /etc/apt/sources.list

RUN cat /etc/apt/sources.list


RUN apt-get update  && apt-get upgrade
RUN apt-get install -y apache2 libapache2-mod-php5 build-essential libgd2-xpm-dev libssl-dev
RUN groupadd -g 9000 nagios
RUN groupadd -g 9001 nagcmd
RUN useradd -u 9000 -g nagios -G nagcmd -d /usr/local/nagios -c 'Nagios Admin' nagios
RUN adduser www-data nagcmd

RUN wget http://prdownloads.sourceforge.net/sourceforge/nagios/nagios-3.5.1.tar.gz
RUN tar xzf nagios-3.5.1.tar.gz

RUN ./configure –-prefix=/usr/local/nagios -–with-nagios-user=nagios –-with-nagios-group=nagios –-with-command-user=nagios –-with-command-group=nagcmd

RUN make all && make install && make install-init &&make install-config && make install-commandmode && make install-webconf
RUN htpasswd -c /usr/local/nagios/etc/htpasswd.users nagiosadmin  && chown nagios:nagcmd /usr/local/nagios/etc/htpasswd.users
