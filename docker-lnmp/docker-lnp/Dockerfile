# 采用Nginx稳定版本
FROM nginx:stable-alpine

MAINTAINER koma <komazhang@foxmail.com>

# 定义Nginx及虚拟机配置文件，可根据实际情况修改路径
ARG NGINX_CONF=conf/nginx/nginx.conf
ARG NGINX_WWW_CONF=conf/nginx/www.conf
ARG FPM_CONF=conf/php-fpm/php-fpm.conf
ARG FPM_WWW_CONF=conf/php-fpm/www.conf
ARG PHP_CONF=conf/php/php.ini

# 设置软件源为清华镜像
RUN echo 'https://mirrors.ustc.edu.cn/alpine/v3.6/community/' >  /etc/apk/repositories && \
    echo 'https://mirrors.ustc.edu.cn/alpine/v3.6/main/'      >> /etc/apk/repositories

# 设置好系统时区为东八区
RUN apk update && apk add tzdata \
    && cp /usr/share/zoneinfo/Asia/Chongqing /etc/localtime \
    && apk del tzdata

# 安装系统运行需要的软件，可根据实际情况增删
RUN apk update \
    && apk add bash \
    wget curl autoconf vim git supervisor gcc g++ openssl-dev

# 安装PHP及常用扩展，可根据实际情况增删
RUN apk add php7-fpm \
    php7-common \
    php7-dev \
    php7-xdebug \ 
    php7-pdo \
    php7-pdo_mysql \
    php7-mysqlnd \
    php7-mysqli \
    php7-mcrypt \
    php7-mbstring \
    php7-ctype \
    php7-zlib \
    php7-gd \
    php7-exif \
    php7-intl \
    php7-sqlite3 \
    php7-pdo_pgsql \
    php7-pgsql \
    php7-xml \
    php7-xsl \
    php7-curl \
    php7-openssl \
    php7-iconv \
    php7-json \
    php7-phar \
    php7-soap \
    php7-dom \
    php7-zip \
    php7-session \
    php7-imap \
    php7-opcache \
    php7-pear \
    php7-sockets \
    php7-pcntl \
    php7-posix \
    php7-sysvmsg \
    php7-sysvshm \
    php7-sysvsem

# 覆盖Nginx及FPM配置文件
RUN rm -rf /etc/nginx/nginx.conf \
    && rm -rf /etc/nginx/conf.d/default.conf \
    && rm -rf /etc/php7/php-fpm.conf \
    && rm -rf /etc/php7/php-fpm.d/www.conf \
    && rm -rf /etc/php7/php.ini
ADD $NGINX_CONF /etc/nginx/nginx.conf
ADD $NGINX_WWW_CONF /etc/nginx/conf.d/www.conf
ADD $FPM_CONF /etc/php7/php-fpm.conf
ADD $FPM_WWW_CONF /etc/php7/php-fpm.d/www.conf
ADD $PHP_CONF /etc/php7/php.ini

# 复制 supervisor 配置文件
RUN rm -rf /etc/supervisord.conf 
ADD conf/supervisord.conf /etc/supervisor/supervisord.conf

# 装载启动脚本
ADD scripts/start.sh /start.sh
RUN chmod a+x /start.sh

# 将虚拟机 root 路径暴露成卷
# 方便宿主机和容器实现目录共享
# 该值为虚拟机配置中的 root 路径，这里默认为 /var/www
# 可根据实际虚拟机配置进行修改
VOLUME /var/www

# 执行一些必要的 bash 命令来确保系统配置正常运行，可根据实际情况调整
RUN addgroup www-data \
    && adduser -G www-data -s /sbin/nologin -D www-data

EXPOSE 80
CMD ["/start.sh"]