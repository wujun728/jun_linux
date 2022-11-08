FROM tomcat:9

ADD ./server.xml /usr/local/tomcat/conf/

EXPOSE 8080
EXPOSE 8009

VOLUME "/usr/local/tomcat/webapps"
VOLUME "/usr/local/tomcat/conf"

WORKDIR /usr/local/tomcat


CMD [ "/usr/local/tomcat/bin/catalina.sh" , "run"]
