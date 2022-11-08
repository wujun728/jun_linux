FROM debian:jessie

COPY ./logstash-forwarder /
RUN chmod +x /logstash-forwarder
ENTRYPOINT ["/logstash-forwarder", "-config"]