FROM    supermy/docker-jre:7

ENV SOLR_VERSION 4.10.4
ENV MYSOLR solr-$SOLR_VERSION

#procps是一个实用程序包，主要包括ps top kill等程序主要用来显示与控制一些系统信息，进程状态之类的内容。
RUN export DEBIAN_FRONTEND=noninteractive && \
  apt-get update && \
  apt-get -y install procps && \
  mkdir -p /opt && \
  wget -nv --output-document=/opt/$MYSOLR.tgz http://www.mirrorservice.org/sites/ftp.apache.org/lucene/solr/$SOLR_VERSION/$MYSOLR.tgz && \
  tar -C /opt --extract --file /opt/$MYSOLR.tgz && \
  ln -s /opt/$MYSOLR /opt/solr

RUN rm /opt/$MYSOLR.tgz

#RUN update-alternatives --install /usr/bin/jar jar /opt/jre/jdk1.7.0_76/bin/jar 100

RUN mkdir -p /opt/solr/example/solr-webapp/webapp/ && \
    cd /opt/solr/example/solr-webapp/webapp/ && \
    jar xvf /opt/solr/example/webapps/solr.war \
    && ls -hl
COPY conf/schema.xml /opt/solr/example/solr/collection1/conf/
COPY classes /opt/solr/example/solr-webapp/webapp/WEB-INF/classes
COPY lib/IKAnalyzer2012FF_u1.jar  /opt/solr/example/solr-webapp/webapp/WEB-INF/lib/

EXPOSE 8983
CMD ["/bin/bash", "-c", "/opt/solr/bin/solr -f"]

