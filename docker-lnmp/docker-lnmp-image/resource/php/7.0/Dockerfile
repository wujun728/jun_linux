Skip to content
This repository
Search
Pull requests
Issues
Gist
 @jianyong
 Unwatch 1
  Star 0
 Fork 0 m-docker/php7
 Code  Issues 0  Pull requests 0  Wiki  Pulse  Graphs  Settings
Branch: master Find file Copy path
php7/Dockerfile
d888bc0  11 days ago
@jianyong jianyong --enable-maintainer-zts
1 contributor
RawBlameHistory     Executable File  28 lines (26 sloc)  1.84 KB
FROM index.alauda.cn/library/centos:6
RUN yum -y install epel-release
RUN yum -y update
RUN yum -y install -y gcc gcc-c++  make zlib zlib-devel pcre pcre-devel  libjpeg libjpeg-devel \
    libpng libpng-devel freetype freetype-devel libxml2 libxml2-devel \
    glibc glibc-devel glib2 glib2-devel bzip2 bzip2-devel ncurses ncurses-devel curl curl-devel\
    e2fsprogs e2fsprogs-devel krb5 krb5-devel openssl openssl-devel \
    openldap openldap-devel nss_ldap openldap-clients openldap-servers \
    php-mysqlnd libmcrypt-devel  libtidy libtidy-devel recode recode-devel libxpm-devel
RUN yum -y install tar
RUN yum install -y libXpm.x86_64 libXpm-devel.x86_64
RUN yum install -y mcrypt libmcrypt.x86_64 libmcrypt-devel.x86_64
RUN mkdir -p ~/server
WORKDIR ~/server
ADD http://cn2.php.net/get/php-7.0.2.tar.gz/from/this/mirror php-7.0.2.tar.gz
RUN tar zxvf php-7.0.2.tar.gz
RUN ln -s php-7.0.2 php
WORKDIR ~/server/php
RUN ./configure --prefix=~/server/php --with-config-file-path=~/server/php/etc --with-mysql=mysqlnd --with-pdo-mysql=mysqlnd --with-mysqli=mysqlnd --with-gd --with-iconv --with-zlib --enable-xml --enable-bcmath --enable-shmop --enable-sysvsem --enable-inline-optimization --enable-mbregex --enable-fpm --enable-mbstring --enable-ftp --enable-gd-native-ttf --with-openssl --enable-pcntl --enable-sockets --with-xmlrpc --enable-zip --enable-soap --without-pear --with-gettext --enable-session --with-mcrypt --with-curl --with-jpeg-dir --with-freetype-dir --with-xpm-dir=/usr --with-bz2 --enable-maintainer-zts
RUN make && make install
RUN cp php.ini-production /etc/php.ini
RUN cp sapi/fpm/init.d.php-fpm /etc/init.d/php-fpm
RUN cp etc/php-fpm.conf.default etc/php-fpm.conf
RUN cp etc/php-fpm.d/www.conf.default etc/php-fpm.d/www.conf
RUN chmod +x /etc/init.d/php-fpm

CMD ~/server/php/bin/php -v
Status API Training Shop Blog About
© 2016 GitHub, Inc. Terms Privacy Security Contact Help
m-docker / php7
master
 Dockerfile
 README.md
