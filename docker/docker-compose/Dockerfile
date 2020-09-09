FROM php:7.1.19-fpm-alpine3.7

MAINTAINER Nixus <nixus@nixus.cn>

LABEL 基于7.1.19-fpm-alpine3.7构建的PHP环境；安装了pdo pdo_mysql bcmath gd zip bz2（如果需要ffmpeg，可以取消注释）
LABEL 添加swoole扩展

RUN apk add --no-cache --virtual .phpize-deps $PHPIZE_DEPS \
    #&& apk add --no-cache ffmpeg \
    && apk add --no-cache libpng-dev \
    #&& apk add --no-cache gcc \
    #&& apk add --no-cache make \
    #&& apk add --no-cache autoconf \
    #&& apk add --no-cache pcre \
    && pecl install -o -f redis-4.0.1 \
    && rm -rf /tmp/pear \
    && apk del .phpize-deps \
    && docker-php-ext-enable redis \
    && docker-php-ext-install pdo pdo_mysql bcmath gd zip
