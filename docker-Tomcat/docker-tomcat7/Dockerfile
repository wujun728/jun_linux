FROM         ubuntu:12.04
MAINTAINER    binarywang<binarywang@gmail.com>

#把java与tomcat添加到容器中
ADD jdk-8u111-linux-x64.tar.gz /opt/app/
ADD apache-tomcat-8.5.6.tar.gz /opt/app/

#配置java与tomcat环境变量
ENV JAVA_HOME /opt/app/jdk1.8.0_111
ENV CLASSPATH $JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar
ENV CATALINA_HOME /opt/app/apache-tomcat-8.5.6
ENV CATALINA_BASE /opt/app/apache-tomcat-8.5.6
ENV PATH $PATH:$JAVA_HOME/bin:$CATALINA_HOME/lib:$CATALINA_HOME/bin

#容器运行时监听的端口
EXPOSE  8080