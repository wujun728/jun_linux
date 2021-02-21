FROM supermy/docker-jre:7

RUN export http_proxy=http://192.168.0.121:8087

# grab gosu for easy step-down from root
RUN gpg --keyserver ha.pool.sks-keyservers.net --recv-keys B42F6819007F00F88E364FD4036A9C25BF357DD4
RUN curl -kx http_proxy=http://192.168.0.121:8087 -o /usr/local/bin/gosu -SL "https://github.com/tianon/gosu/releases/download/1.2/gosu-$(dpkg --print-architecture)" \
	&& curl -kx http_proxy=http://192.168.0.121:8087  -o /usr/local/bin/gosu.asc -SL "https://github.com/tianon/gosu/releases/download/1.2/gosu-$(dpkg --print-architecture).asc" \
	&& gpg --verify /usr/local/bin/gosu.asc \
	&& rm /usr/local/bin/gosu.asc \
	&& chmod +x /usr/local/bin/gosu

RUN apt-key adv --keyserver ha.pool.sks-keyservers.net --recv-keys 46095ACC8548582C1A2699A9D27D666CD88E42B4


ENV ELASTICSEARCH_VERSION 1.7.0



RUN echo "deb http://packages.elastic.co/elasticsearch/${ELASTICSEARCH_VERSION%.*}/debian stable main" > /etc/apt/sources.list.d/elasticsearch.list

RUN apt-get -y update \
	&& apt-get -y install elasticsearch \
	&& rm -rf /var/lib/apt/lists/*

RUN	update-rc.d elasticsearch defaults 95 10

RUN sed -i 's/#cluster.name: elasticsearch/cluster.name: elasticsearch/'   /etc/elasticsearch/elasticsearch.yml

RUN grep cluster.name /etc/elasticsearch/elasticsearch.yml
RUN grep node.name /etc/elasticsearch/elasticsearch.yml


ENV PATH /usr/share/elasticsearch/bin:$PATH

COPY config /usr/share/elasticsearch/config

RUN mkdir -p /usr/share/elasticsearch/logs/  && chmod 777 /usr/share/elasticsearch/logs/
RUN mkdir -p /usr/share/elasticsearch/plugins/analysis-ik/

COPY elasticsearch-analysis-ik-1.4.0-jar-with-dependencies.jar /usr/share/elasticsearch/plugins/analysis-ik/


VOLUME /usr/share/elasticsearch/data

COPY docker-entrypoint.sh /

RUN chmod a+x /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]

EXPOSE 9200 9300

CMD ["elasticsearch"]