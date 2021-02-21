FROM supermy/docker-jre:ap

MAINTAINER James Mo

RUN apk add --update bash wget && rm -rf /var/cache/apk/*

RUN mkdir /opt/flume
#RUN wget -qO- http://archive.apache.org/dist/flume/1.6.0/apache-flume-1.6.0-bin.tar.gz \
#  | tar zxvf - -C /opt/flume --strip 1

WORKDIR /tmp
RUN wget http://archive.apache.org/dist/flume/1.6.0/apache-flume-1.6.0-bin.tar.gz

RUN tar zxvf apache-flume-1.6.0-bin.tar.gz
#RUN mv apache-flume-1.6.0-bin/*  /opt/flume/
RUN cp -rf apache-flume-1.6.0-bin/*  /opt/flume/
#RUN ls /opt/flume
#--strip-path 1

RUN rm  apache-flume-1.6.0-bin.tar.gz


COPY conf /var/tmp/
COPY lib/* /opt/flume/lib/

RUN sed  -i '/log4j.logger.org.apache.flume.lifecycle/a log4j.logger.org.apache.flume.interceptor = DEBUG'  /opt/flume/conf/log4j.properties


RUN cat /etc/hosts

RUN  echo "192.168.99.101 hbasemasteripc" >> /etc/hosts

EXPOSE 44444

ENV PATH /opt/flume/bin:$JAVA_HOME/bin:$PATH

#ADD start-flume.sh /opt/flume/bin/start-flume
#RUN chmod a+x /opt/flume/bin/start-flume
#
#
#COPY gosu /bin/gosu
#ADD docker-entrypoint.sh /entrypoint.sh
#
#RUN chmod a+x /bin/gosu
#RUN chmod a+x /entrypoint.sh
#
#RUN addgroup flume \
#	&& adduser -D -G flume -h /opt/flume flume \
#	&& chown -R flume:flume /opt/flume
#
#ENTRYPOINT ["/entrypoint.sh"]
#CMD ["start"]

#
COPY docker-entrypoint1.sh /docker-entrypoint.sh
RUN chmod a+x /docker-entrypoint.sh
ENTRYPOINT [ "/docker-entrypoint.sh" ]