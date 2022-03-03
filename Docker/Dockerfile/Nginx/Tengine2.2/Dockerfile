#FROM alpine:3.5
#FROM yikaus/alpine-bash
# 参考：https://github.com/nginxinc/docker-nginx/blob/3e8a6ee0603bf6c9cd8846c5fa43e96b13b0f44b/stable/alpine/Dockerfile
# 某作者的讲解：https://segmentfault.com/a/1190000004990514
FROM yunai/alpine
MAINTAINER TENGINE Docker Maintainers "zhijiantianya@gmail.com"

# RUN apk update && apk upgrade

ENV TEGINE_VERSION 2.2.0

RUN \
 # 安装编译依赖
 apk add --no-cache --virtual .build-deps \
     gcc \
     curl \
     make \
     libc-dev \
     pcre-dev \
     openssl-dev \
     jemalloc-dev \
 # 下载tengine TODO 判断是否md5正确 MD5: c5f040d07cdade7b618a4f04f1fdb8fa
 && curl -fSL http://tengine.taobao.org/download/tengine-$TEGINE_VERSION.tar.gz -o nginx.tar.gz \
 # 解压tegine
 && mkdir -p /usr/src \
 && tar -zxC /usr/src -f nginx.tar.gz \
 && rm nginx.tar.gz \
 # 创建nginx用户和用户组
 && addgroup -S nginx \
 && adduser -D -S -h /var/cache/nginx -s /sbin/nologin -G nginx nginx \
 # 编译
 && CONFIG="\
        --prefix=/etc/nginx \
        --sbin-path=/usr/sbin/nginx \
        --conf-path=/etc/nginx/nginx.conf \
        --error-log-path=/var/log/nginx/error.log \
        --http-log-path=/var/log/nginx/access.log \
        --pid-path=/var/run/nginx.pid \
        --lock-path=/var/run/nginx.lock \
        --http-client-body-temp-path=/var/cache/nginx/client_temp \
        --http-proxy-temp-path=/var/cache/nginx/proxy_temp \
        --http-fastcgi-temp-path=/var/cache/nginx/fastcgi_temp \
        --http-uwsgi-temp-path=/var/cache/nginx/uwsgi_temp \
        --http-scgi-temp-path=/var/cache/nginx/scgi_temp \
        --user=nginx \
        --group=nginx \
        --with-jemalloc \
    " \
 && cd /usr/src/tengine-$TEGINE_VERSION \
 && ./configure $CONFIG --with-debug \
 && make \
 && make install \
 # 创建nginx html目录
 && rm -rf /etc/nginx/html/ \
 && mkdir -p /usr/share/nginx/html/ \
 && install -m644 html/index.html /usr/share/nginx/html/ \
 && install -m644 html/50x.html /usr/share/nginx/html/ \
 # 创建nginx conf目录
 && mkdir /etc/nginx/conf.d/ \
 # 移除源码
 && rm -rf /usr/src/tengine-$TEGINE_VERSION \
 # Bring in gettext so we can get `envsubst`, then throw
 # the rest away. To do this, we need to install `gettext`
 # then move `envsubst` out of the way so `gettext` can
 # be deleted completely, then move `envsubst` back.
 && apk add --no-cache --virtual .gettext gettext \
 && mv /usr/bin/envsubst /tmp/ \
 && runDeps="$( \
    scanelf --needed --nobanner /usr/sbin/nginx /usr/lib/nginx/modules/*.so /tmp/envsubst \
        | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
        | sort -u \
        | xargs -r apk info --installed \
        | sort -u \
    )" \
 && apk add --no-cache --virtual .nginx-rundeps $runDeps \
 # 移除apk
 && apk del .build-deps \
 && apk del .gettext \
 && mv /tmp/envsubst /usr/local/bin/ \
 # forward request and error logs to docker log collector：这样我们就能使用 docker logs 命令方便的查看日志了
 && ln -sf /dev/stdout /var/log/nginx/access.log \
 && ln -sf /dev/stderr /var/log/nginx/error.log

COPY conf/nginx.conf /etc/nginx/nginx.conf
COPY conf/nginx.vh.default.conf /etc/nginx/conf.d/default.conf

EXPOSE 80 443

CMD ["nginx", "-g", "daemon off;"]