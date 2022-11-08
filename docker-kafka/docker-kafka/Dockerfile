FROM anapsix/alpine-java

#定义kafka版本信息
ARG kafka_version=0.11.0.1
ARG scala_version=2.11

MAINTAINER Koma

#设置软件源
RUN echo 'https://mirrors.ustc.edu.cn/alpine/v3.6/community/' >  /etc/apk/repositories \
    && echo 'https://mirrors.ustc.edu.cn/alpine/v3.6/main/' >> /etc/apk/repositories

#设置时区
RUN apk update && apk add tzdata \
    && cp /usr/share/zoneinfo/Asia/Hong_Kong /etc/localtime \
    && echo 'Asia/Hong_Kong' > /etc/timezone \
    && apk del tzdata

RUN apk add --update unzip wget curl docker supervisor

ENV KAFKA_VERSION=$kafka_version
ENV SCALA_VERSION=$scala_version

#运行下载kafka脚本并解压到指定文件下
ADD download-kafka.sh /tmp/download-kafka.sh
RUN chmod a+x /tmp/download-kafka.sh \
    && sync && /tmp/download-kafka.sh \
    && tar xzf /tmp/kafka_${SCALA_VERSION}-${KAFKA_VERSION}.tgz -C /opt \
    && rm /tmp/kafka_${SCALA_VERSION}-${KAFKA_VERSION}.tgz \
    && ln -s /opt/kafka_${SCALA_VERSION}-${KAFKA_VERSION} /opt/kafka

VOLUME ["/kafka"]

ENV KAFKA_HOME /opt/kafka
ENV PATH ${PATH}:${KAFKA_HOME}/bin

ADD start-kafka.sh /usr/bin/start-kafka.sh
RUN chmod a+x /usr/bin/start-kafka.sh

ADD supervisord.conf /etc/supervisord.conf

CMD ["start-kafka.sh"]
