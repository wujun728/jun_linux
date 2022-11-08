FROM php:5.6-fpm

RUN mkdir -p /alidata/opt/log/php && mkdir -p /alidata/opt/php/ext
RUN chown -R www-data:www-data /alidata/opt/log/php /alidata/opt/php/ext

ADD sources.list    /etc/apt/sources.list
RUN apt-get update && apt-get install -y \
        git \
        libgearman-dev \
        libmemcached-dev \
        libmcrypt-dev \
        libfreetype6-dev \
        libjpeg62-turbo-dev \
        libpng12-dev \
        alien \
        && rm -r /var/lib/apt/lists/*

# Install PHP extensions
COPY ext/memcached-2.2.0.tgz /alidata/opt/php/ext/memcached.tgz
COPY ext/gearman-1.1.2.tgz /alidata/opt/php/ext/gearman.tgz
COPY ext/redis-2.2.5.tgz /alidata/opt/php/ext/redis.tgz
COPY ext/xdebug-2.4.0.tgz /alidata/opt/php/ext/xdebug.tgz
COPY ext/memcache-3.0.8.tgz /alidata/opt/php/ext/memcache.tgz
COPY ext/xhprof-0.9.4.tgz /alidata/opt/php/ext/xhprof.tgz
COPY ext/yar-1.2.5.tgz  /alidata/opt/php/ext/yar.tgz

ADD http://192.168.1.1:9999/oracle-instantclient11.2-basic-11.2.0.4.0-1.x86_64.rpm /alidata/opt/oracle/oracle-instantclient11.2-basic-11.2.0.4.0-1.x86_64.rpm
ADD http://192.168.1.1:9999/oracle-instantclient11.2-devel-11.2.0.4.0-1.x86_64.rpm /alidata/opt/oracle/oracle-instantclient11.2-devel-11.2.0.4.0-1.x86_64.rpm

WORKDIR /alidata/opt/oracle
RUN alien -i oracle-instantclient11.2-basic-11.2.0.4.0-1.x86_64.rpm
RUN alien -i oracle-instantclient11.2-devel-11.2.0.4.0-1.x86_64.rpm

RUN docker-php-ext-configure gd --with-freetype-dir=/usr/include/ --with-jpeg-dir=/usr/include/ \
        && docker-php-ext-install zip \
        && docker-php-ext-install gd \
        && docker-php-ext-install mbstring \
        && docker-php-ext-install mcrypt \
        && docker-php-ext-install pdo_mysql \
        && docker-php-ext-install oci8 

WORKDIR /alidata/opt/php/ext
RUN pecl install memcached.tgz && echo "extension=memcached.so" > /usr/local/etc/php/conf.d/memcached.ini 
RUN pecl install gearman.tgz && echo "extension=gearman.so" > /usr/local/etc/php/conf.d/gearman.ini 
RUN pecl install memcache.tgz && echo "extension=memcache.so" > /usr/local/etc/php/conf.d/memcache.ini 
RUN pecl install yar.tgz && echo "extension=yar.so" > /usr/local/etc/php/conf.d/yar.ini 
RUN pecl install xdebug.tgz && echo "zend_extension=/usr/local/lib/php/extensions/no-debug-non-zts-20131226/xdebug.so" > /usr/local/etc/php/conf.d/xdebug.ini
        

ADD composer.phar /usr/local/bin/composer
RUN chmod 755 /usr/local/bin/composer

RUN usermod -u 1000 www-data

ENV DEBIAN_FRONTEND noninteractive

# apt-get update
RUN apt-get -q update
# install inotify-tools
RUN apt-get install -yq inotify-tools

# install pip
RUN apt-get install -yq python-pip

# install xlsx2csv
RUN pip install xlsx2csv


VOLUME ["/alidata/opt/php"]

# wkhtmltox
WORKDIR /alidata/opt/tools

#RUN rm -rf /usr/local/etc/php/php.ini && rm -rf /usr/local/etc/php-fpm.conf
#ADD php.ini /usr/local/etc/php/php.ini
#ADD php-fpm.conf /usr/local/etc/php-fpm.conf

WORKDIR /alidata
CMD echo 'export PATH="~/.composer/vendor/bin:$PATH"' >> /etc/profile && source /etc/profile
CMD kill -SIGINT `cat /alidata/opt/log/php/php-fpm.pid`
CMD php-fpm
