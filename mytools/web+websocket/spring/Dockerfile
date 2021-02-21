#export JAVA_HOME="/Library/Java/JavaVirtualMachines/jdk1.7.0_60.jdk/Contents/Home/"
#build spring app use jdk1.7
#spring app 源代码 :https://github.com/supermy/docker-gs-messaging-stomp-websocket
FROM  myjre7_base:latest

RUN mkdir -p /opt/spring-boot-maven-docker/
ADD gs-messaging-stomp-websocket-0.1.0.jar /opt/spring-boot-maven-docker/
EXPOSE 8080
WORKDIR /opt/spring-boot-maven-docker/
CMD ["java", "-jar", "gs-messaging-stomp-websocket-0.1.0.jar"]