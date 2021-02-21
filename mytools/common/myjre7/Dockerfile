FROM supermy/docker-debian:7

RUN wget --no-check-certificate --header "Cookie: oraclelicense=accept-securebackup-cookie" \
    http://download.oracle.com/otn-pub/java/jdk/7u76-b13/server-jre-7u76-linux-x64.tar.gz

RUN mkdir /opt/jre
RUN tar -zxf server-jre-7u76-linux-x64.tar.gz -C /opt/jre
RUN rm server-jre-7u76-linux-x64.tar.gz

RUN update-alternatives --install /usr/bin/java java /opt/jre/jdk1.7.0_76/bin/java 100
RUN update-alternatives --install /usr/bin/javac javac /opt/jre/jdk1.7.0_76/bin/javac 100
RUN update-alternatives --install /usr/bin/jar jar /opt/jre/jdk1.7.0_76/bin/jar 100

#docker镜像不保存当前状态，状态写在配置文件里面
RUN sed -i '1a JAVA_HOME="/opt/jre/jdk1.7.0_76/"' /etc/profile

ENV JAVA_HOME /opt/jre/jdk1.7.0_76/

RUN    apt-get clean && \
      rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
