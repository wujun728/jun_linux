FROM centos:7
MAINTAINER Frank.Wu <pkaq@msn.com>

#install some tools
RUN yum install -y \
    wget \
    tar && \
    yum clean all && rm -rf /var/cache/yum/*

#set java env
ENV JAVA_VERSION=1.8.0_45
ENV JAVA_TARBALL=server-jre-8u45-linux-x64.tar.gz
ENV JAVA_HOME=/opt/java/jdk${JAVA_VERSION}

#download
RUN wget --no-check-certificate --directory-prefix=/tmp \
         --header "Cookie: gpw_e24=http%3A%2F%2Fwww.oracle.com%2F; oraclelicense=accept-securebackup-cookie" \
         http://download.oracle.com/otn-pub/java/jdk/8u45-b14/${JAVA_TARBALL} && \
    mkdir -p /opt/java && \
    tar -xzf /tmp/${JAVA_TARBALL} -C /opt/java/ && \
    alternatives --install /usr/bin/java java /opt/java/jdk${JAVA_VERSION}/bin/java 100 && \
    rm -rf /tmp/* && rm -rf /var/log/*

#set tomcat env
ENV TOMCAT_VERSION 8.0.24
ENV CATALINA_HOME /opt/tomcat

#download
RUN cd /opt && \
    wget -q http://apache.fayea.com/tomcat/tomcat-8/v${TOMCAT_VERSION}/bin/apache-tomcat-${TOMCAT_VERSION}.tar.gz -O /opt/tomcat.tar.gz && \
    tar -zxvf /opt/tomcat.tar.gz && \
    rm /opt/tomcat.tar.gz && \
    ln -s /opt/apache-tomcat-${TOMCAT_VERSION} /opt/tomcat

#add user
ADD ["tomcat-users.xml", "$CATALINA_HOME/conf/tomcat-users.xml"]

EXPOSE 8080

CMD $CATALINA_HOME/bin/catalina.sh run
