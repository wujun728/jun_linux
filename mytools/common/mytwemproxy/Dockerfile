FROM  supermy/docker-debian:7
#FROM ubuntu:14.04

#RUN export http_proxy=http://10.77.45.191:8087
RUN apt-get update
RUN apt-get install libtool make automake supervisor curl python2.7 python-pip -qy
RUN apt-get install libyaml-0-2 -yq
#RUN apt-get install -y memcached

# Install twemproxy
RUN curl -qL https://twemproxy.googlecode.com/files/nutcracker-0.3.0.tar.gz | tar xzf -
RUN cd nutcracker-0.3.0 && ./configure --enable-debug=log && make && mv src/nutcracker /usr/local/bin/nutcracker
RUN cd / && rm -rf nutcracker-0.3.0

# install pip deps
RUN pip install pyaml==14.05.7
RUN pip install boto==2.32.0

# Configuration
RUN mkdir -p /etc/nutcracker
RUN mkdir -p /var/log/nutcracker
ADD generate_configs.py /generate_configs.py
ADD run.sh /run.sh
RUN chmod a+x run.sh

EXPOSE 3000 22222 22123 11211 22121
CMD ["/run.sh"]

RUN apt-get remove libtool make automake curl -yq



