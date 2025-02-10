FROM buildpack-deps:jessie-curl

MAINTAINER Dreamlu <qq596392912@gmail.com>

WORKDIR /tmp

# Default to UTF-8 file.encoding
ENV LANG C.UTF-8

ENV MAJOR 8
ENV MINOR 51
ENV JAVA_DEBIAN_VERSION 8u51-b14-2~bpo8+2

## timeZone
RUN echo "Asia/Shanghai" > /etc/timezone
RUN dpkg-reconfigure -f noninteractive tzdata

RUN set -x \
	&& curl -fSL http://soft.dreamlu.net/server-jre-${MAJOR}u${MINOR}-linux-weixin-i586.tar.gz -o server-jre.tar.gz \
	&& mkdir oracle-server-jre \
	&& tar -xzf server-jre.tar.gz -C ./oracle-server-jre \
	&& mkdir -p /opt/oracle-server-jre \
	&& cp -r /tmp/oracle-server-jre/jdk1.${MAJOR}.0_${MINOR}/* /opt/oracle-server-jre/ \
	&& ln -s /opt/oracle-server-jre/bin/java /usr/bin/java \
	&& chmod ugo+x /usr/bin/java \
	&& rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*