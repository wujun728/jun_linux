#latest=8.1   wheezy=7.8
FROM    debian:7.9
#FROM    supermy/docker-debian:7

MAINTAINER supermy <springclick@gmail.com>

RUN sed -i '1,3d'   /etc/apt/sources.list \
    && echo '#hello'>> /etc/apt/sources.list \
    && sed -i '1a \
    deb http://mirrors.163.com/debian/ wheezy main non-free contrib \n \
    deb http://mirrors.163.com/debian/ wheezy-proposed-updates main contrib non-free \n \
    deb http://mirrors.163.com/debian-security/ wheezy/updates main contrib non-free \n \
    deb-src http://mirrors.163.com/debian/ wheezy main non-free contrib \n \
    deb-src http://mirrors.163.com/debian/ wheezy-proposed-updates main contrib non-free \n \
    deb-src http://mirrors.163.com/debian-security/ wheezy/updates main contrib non-free \n \
    ' /etc/apt/sources.list

# sohu 更新服务器：
#RUN sed -i '1a \
#    deb http://mirrors.sohu.com/debian/ wheezy main non-free contrib  \
#    deb http://mirrors.sohu.com/debian/ wheezy-proposed-updates main non-free contrib \
#    deb http://mirrors.sohu.com/debian-security/ wheezy/updates main contrib non-free \n \
#    deb-src http://mirrors.sohu.com/debian/ wheezy main non-free contrib \
#    deb-src http://mirrors.sohu.com/debian/ wheezy-proposed-updates main non-free contrib \
#    deb-src http://mirrors.sohu.com/debian-security/ wheezy/updates main contrib non-free \n \
#    ' /etc/apt/sources.list



RUN apt-get -qqy update && \
    apt-get -qqy install gcc libpcre3 libpcre3-dev openssl libssl-dev make wget libreadline-dev libncurses-dev graphicsmagick


#RUN export http_proxy=http://172.16.71.25:8087
#-e http_proxy=172.16.71.25:8087

WORKDIR /tmp
RUN wget http://tengine.taobao.org/download/tengine-2.1.2.tar.gz \
    && wget --no-check-certificate https://openresty.org/download/openresty-1.9.7.4.tar.gz \
    && wget http://labs.frickle.com/files/ngx_cache_purge-2.3.tar.gz \
    && tar xvf tengine-2.1.2.tar.gz \
    && tar zxf openresty-1.9.7.4.tar.gz \
    && tar zxf ngx_cache_purge-2.3.tar.gz



WORKDIR /tmp/openresty-1.9.7.4
RUN ./configure --prefix=/usr/local/openresty --with-luajit && make && make install

WORKDIR /tmp/openresty-1.9.7.4/bundle/lua-5.1.5
RUN make linux && make install
#
#WORKDIR /tmp
#RUN wget http://bitop.luajit.org/download/LuaBitOp-1.0.2.tar.gz
#RUN tar zxf LuaBitOp-1.0.2.tar.gz
#WORKDIR /tmp/LuaBitOp-1.0.2
#RUN make && make install
#
#WORKDIR /tmp
#COPY lua-lib/lua-resty-kafka /tmp/lua-resty-kafka
#WORKDIR /tmp/lua-resty-kafka
#RUN make && make install


###waf begin naxsi 应用防火墙 抵御SQL注入、跨站脚本、跨域伪造请求、本地和远程文件包含漏洞
ENV NAXSI_VERSION master
WORKDIR /tmp

RUN gpg --keyserver keyserver.ubuntu.com --recv-keys 2685AED4 7BD9BF62 A1C052F8 \
    && apt-get install ca-certificates -y \
    && wget "https://github.com/nbs-system/naxsi/archive/${NAXSI_VERSION}.tar.gz" -O nginx-${NAXSI_VERSION}.tar.gz && \
    tar zxvf nginx-${NAXSI_VERSION}.tar.gz
###waf end


WORKDIR /tmp/tengine-2.1.2
RUN echo "/usr/local/lib" > /etc/ld.so.conf.d/usr_local_lib.conf

#更新，混淆版本标识
RUN sed -in 's/nginx\//myserver\//g' /tmp/tengine-2.1.2/src/core/nginx.h
RUN sed -in 's/1.6.2/8.8/g' /tmp/tengine-2.1.2/src/core/nginx.h
RUN sed -in 's/Tengine\"/myserver\"/g' /tmp/tengine-2.1.2/src/core/nginx.h
RUN sed -in 's/2.1.0/8.8/g' /tmp/tengine-2.1.2/src/core/nginx.h
RUN sed -in 's/NGINX\"/myserver\"/g' /tmp/tengine-2.1.2/src/core/nginx.h
RUN sed -in 's/2001000/800800/g' /tmp/tengine-2.1.2/src/core/nginx.h


RUN \
    cd /tmp/tengine-2.1.2 &&\
    ./configure  \
       --with-ld-opt='-Wl,-rpath,/usr/local/lib/' \
        --add-module=/tmp/openresty-1.9.7.4/bundle/redis2-nginx-module-0.12/ \
        --add-module=/tmp/openresty-1.9.7.4/bundle/ngx_devel_kit-0.2.19/ \
        --add-module=/tmp/openresty-1.9.7.4/bundle/set-misc-nginx-module-0.30/ \
        --add-module=/tmp/openresty-1.9.7.4/bundle/echo-nginx-module-0.58/ \
        --add-module=/tmp/openresty-1.9.7.4/bundle/ngx_lua-0.10.2/ \
        --add-module=/tmp/ngx_cache_purge-2.3/ \
        --add-module=/tmp/naxsi-${NAXSI_VERSION}/naxsi_src/ \
        --with-ld-opt="-L /usr/local/lib" \
    && make && make install

ADD nginx.conf /usr/local/nginx/conf/nginx.conf




WORKDIR /root
#RUN rm -rf /tmp/tengine-*
#RUN rm -rf /tmp/lua-*

ENV HOME /root
RUN rm -rf /etc/service/sshd /etc/my_init.d/00_regen_ssh_host_keys.sh

RUN mkdir -p /etc/my_init.d

#nginx 配置文件
COPY http.d /usr/local/nginx/conf/http.d
COPY server.d /usr/local/nginx/conf/server.d
COPY naxsi.d /usr/local/nginx/conf/naxsi.d
RUN cp /tmp/naxsi-master/naxsi_config/naxsi_core.rules /usr/local/nginx/conf/naxsi.d/

COPY waf.d /usr/local/nginx/conf/waf.d
RUN  mkdir -p /data/logs/hack && chmod -R 775 /data/logs/hack


#lua 库与配置文件
COPY lua-lib /usr/local/nginx/conf/lua-lib
COPY lua.d /usr/local/nginx/conf/lua.d


ADD nginx.sh /etc/my_init.d/nginx.sh
RUN chmod 755 /etc/my_init.d/nginx.sh

#RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN mkdir -p /var/lib/nginx/cache

#配置时区
RUN echo "Asia/Shanghai" > /etc/timezone
RUN dpkg-reconfigure -f noninteractive tzdata

EXPOSE 80 443

CMD ["/etc/my_init.d/nginx.sh"]

# build
# docker build -t supermy/docker-mynginx:2.1 .
# userage
# docker run -d -p 8080:80 --name test -v /home/utgard/www/:/data/www/ mynginx_web
