FROM nginx:1.9

ADD  nginx.conf      /etc/nginx/nginx.conf
ADD  vhosts/*    /etc/nginx/conf.d/

RUN mkdir -p /alidata/log/nginx 
RUN chown -R www-data:www-data /alidata/log/nginx 


VOLUME ["/alidata/opt", "/alidata/log"]
