FROM debian-jre8:dreamlu

WORKDIR /usr/local/zbus

ENV ZBUS_VERSION 6.1.0-SNAPSHOT
ENV ZBUS_JAR_URL http://soft.dreamlu.net/ZbusServer-"$ZBUS_VERSION".jar

RUN set -x \
	&& curl -fSL "$ZBUS_JAR_URL" -o ZbusServer.jar

EXPOSE 15555 16666 16667
CMD ["java", "-jar", "ZbusServer.jar"]