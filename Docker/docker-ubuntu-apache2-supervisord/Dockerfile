FROM ubuntu:16.04
MAINTAINER Ryan_Newman <15244909057.ww@gmail.com>

# use china souce
# copy ./apt/sources.list /etc/apt/sources.list

# update software

RUN apt-get -y update
RUN apt-get -y upgrade

# install apache2

RUN apt-get -y install apache2

# install php and plugin

RUN apt-get -y install php7.0 libapache2-mod-php7.0 php7.0-mysql php7.0-common php7.0-zip php7.0-mbstring php7.0-mcrypt php7.0-json php7.0-gd php7.0-curl

# install supervisor

RUN apt-get -y install supervisor

# copy configure file

## apache2 conf
ADD ./apache2/apache2.conf /etc/apache2/apache2.conf
ADD ./apache2/ports.conf /etc/apache2/ports.conf
ADD ./apache2/sites-available/000-default.conf /etc/apache2/sites-available/000-default.conf
ADD ./apache2/sites-available/default-ssl.conf /etc/apache2/sites-available/default-ssl.conf
ADD ./apache2/sites-enabled/000-default.conf /etc/apache2/sites-enabled/000-default.conf

## supervisor conf
ADD ./supervisor/supervisord.conf /etc/supervisor/supervisord.conf
ADD ./supervisor/conf.d/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# run container

EXPOSE 80 443

CMD ["/usr/bin/supervisord"]
