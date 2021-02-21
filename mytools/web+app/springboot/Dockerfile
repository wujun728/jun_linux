FROM supermy/docker-jre:7
VOLUME /tmp
ADD gs-accessing-data-rest-0.1.0.war app.war
#    spring-boot 按class生成时间进行加载没有解决

RUN bash -c 'touch /app.jar'
EXPOSE 8080

ENTRYPOINT ["java","-Djava.security.egd=file:/dev/./urandom","-jar","/app.war"]


#CMD ["java", "-cp", "/app/", "org.springframework.boot.loader.JarLauncher"]

#CMD java -jar spring-boot-restful-service.jar
#ADD build/spring-boot-restful-service.jar /data/spring-boot-restful-service.jar