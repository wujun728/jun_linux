#!/usr/bin/env bash
#    apt-get -qqy install gcc libpcre3 libpcre3-dev openssl libssl-dev make wget libreadline-dev libncurses-dev graphicsmagick
tar xvf tengine-2.1.1.tar.gz
tar zxf ngx_openresty-1.7.10.2.tar.gz
tar zxf ngx_cache_purge-2.3.tar.gz

cd ngx_openresty-1.7.10.2
./configure --prefix=/usr/local/openresty --with-luajit --with-ld-opt="-L /usr/local/lib" && make && make install
cd -

cd LuaBitOp-1.0.2
make && make install
cd -


echo "/usr/local/lib" > /etc/ld.so.conf.d/usr_local_lib.conf

cd tengine-2.1.1
sed -in 's/nginx\//myserver\//g' src/core/nginx.h
sed -in 's/1.6.2/8.8/g' src/core/nginx.h
sed -in 's/Tengine\"/myserver\"/g' src/core/nginx.h
sed -in 's/2.1.0/8.8/g' src/core/nginx.h
sed -in 's/NGINX\"/myserver\"/g' src/core/nginx.h
sed -in 's/2001000/800800/g' src/core/nginx.h
cd -

cd tengine-2.1.1 &&\
./configure  \
   --with-ld-opt='-Wl,-rpath,/usr/local/lib/' \
    --add-module=../ngx_openresty-1.7.10.2/bundle/redis2-nginx-module-0.12/ \
    --add-module=../ngx_openresty-1.7.10.2/bundle/ngx_devel_kit-0.2.19/ \
    --add-module=../ngx_openresty-1.7.10.2/bundle/set-misc-nginx-module-0.29/ \
    --add-module=../ngx_openresty-1.7.10.2/bundle/echo-nginx-module-0.58/ \
    --add-module=../ngx_openresty-1.7.10.2/bundle/ngx_lua-0.9.16/ \
    --add-module=../ngx_cache_purge-2.3/ \
    --with-ld-opt="-L /usr/local/lib" \
&& make && make install
cd -

#cat /etc/ld.so.conf
#ldconfig -v|grep pcre
#/etc/ld.so.conf.d/usr_local_lib.conf
#ldconfig -v|grep pcre

cp  nginx.conf /usr/local/nginx/conf/nginx.conf

cp -rf nginx.d /usr/local/nginx/conf/nginx.d
cp -rf www /usr/local/nginx/

#mkdir -p /etc/my_init.d
#cp  nginx.sh /etc/my_init.d/nginx.sh
#chmod 755 /etc/my_init.d/nginx.sh

mkdir -p /var/lib/nginx/cache
