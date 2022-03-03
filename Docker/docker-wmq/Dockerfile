FROM xsh/wmq75:0.1 

RUN yum install -y python-setuptools && easy_install supervisor && mkdir -p /var/log/supervisor

COPY supervisord.conf /usr/etc/supervisord.conf
COPY start_queue_manager.sh /
RUN chmod +x /start_queue_manager.sh

EXPOSE 1414

CMD ["/usr/bin/supervisord"]
