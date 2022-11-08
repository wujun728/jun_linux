#docker 使用

```
sudo docker build -t php7 .
sudo docker run -it php7 /bin/bash
```


# PHP7
安装过程中会缺少一些库文件, 需要安装它们

安装过程

如果不安装相应的依赖, 在安装过程中会报错, 所以先安装相关依赖
这里面可能有一些已经安装过了，或者其实不是不需要的，因为一些功能我们可能会在编译时排除掉，但是像libxml2, zlib, freetype, bzip2, curl,curl-devel, openssl这些常用的包还是装上比较好

```
sudo yum -y install -y gcc gcc-c++  make zlib zlib-devel pcre pcre-devel  libjpeg libjpeg-devel \
    libpng libpng-devel freetype freetype-devel libxml2 libxml2-devel \
    glibc glibc-devel glib2 glib2-devel bzip2 bzip2-devel ncurses ncurses-devel curl curl-devel\
    e2fsprogs e2fsprogs-devel krb5 krb5-devel openssl openssl-devel \
    openldap openldap-devel nss_ldap openldap-clients openldap-servers \
    php-mysqlnd libmcrypt-devel  libtidy libtidy-devel recode recode-devel libxpm-devel

./configure --prefix=/alidata/server/php --with-config-file-path=/alidata/server/php/etc --with-mysql=mysqlnd --with-pdo-mysql=mysqlnd --with-mysqli=mysqlnd --with-gd --with-iconv --with-zlib --enable-xml --enable-bcmath --enable-shmop --enable-sysvsem --enable-inline-optimization --enable-mbregex --enable-fpm --enable-mbstring --enable-ftp --enable-gd-native-ttf --with-openssl --enable-pcntl --enable-sockets --with-xmlrpc --enable-zip --enable-soap --without-pear --with-gettext --enable-session --with-mcrypt --with-curl --with-jpeg-dir --with-freetype-dir --with-xpm-dir=/usr --with-bz2

make
make install

cp php.ini-production /etc/php.ini
cp sapi/fpm/init.d.php-fpm /etc/init.d/php-fpm
cp etc/php-fpm.conf.default etc/php-fpm.conf
cp etc/php-fpm.d/www.conf.default etc/php-fpm.d/www.conf
chmod +x /etc/init.d/php-fpm
```


错误记录

[x] configure: error: xml2-config not found. Please check your libxml2 installation.
>    yum -y install libxml2 libxml2-devel

[x] configure: error: Cannot find OpenSSL's <evp.h>
>     yum -y install openssl openssl-devel

[x] checking for BZip2 in default path... not found    configure: error: Please reinstall the BZip2 distribution
>     yum -y install bzip2 bzip2-devel

[x] checking for cURL in default path... not found    configure: error: Please reinstall the libcurl distribution [easy.h should be in <curl-dir>/include/curl/]
>     yum install -y curl curl-devel

[x] If configure fails try --with-webp-dir=<DIR>
configure: error: jpeglib.h not found.
>     yum install -y libjpeg libjpeg-devel

[x] configure: error: png.h not found.
>     yum install -y libpng libpng-devel

[x] configure: error: xpm.h not found.
>     yum install -y libXpm.x86_64 libXpm-devel.x86_64

[x] configure: error: freetype-config not found.
>     yum install -y freetype freetype-devel

[x] configure: error: mcrypt.h not found. Please reinstall libmcrypt.
>     yum install -y libmcrypt-devel
