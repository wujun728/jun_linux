FROM maven:3.3-jdk-7
MAINTAINER Xusheng Gong <gongxsh00@163.com>
ENV REFRESHED_AT 2016-01-24
RUN curl -fSL https://github.com/knightliao/disconf/archive/2.6.30.zip -o 2.6.30.zip
RUN unzip 2.6.30.zip
ENV ONLINE_CONFIG_PATH /home/work/dsp/disconf-rd/online-resources
ENV WAR_ROOT_PATH /home/work/dsp/disconf-rd/working/war
RUN cd disconf-2.6.30/disconf-web
VOLUME /home/work/dsp/disconf-rd/online-resources
VOLUME /home/work/dsp/disconf-rd/working
WORKDIR disconf-2.6.30/disconf-web
CMD ["sh", "deploy/deploy.sh"]
