FROM mysql:5.7.24
MAINTAINER Ku8Manager <ku8manager@hpe.com>

# set timezone
ENV TZ Asia/Shanghai

# Set TERM env to avoid mysql client error message "TERM environment variable not set" when running from inside the container
ENV TERM xterm

# install percona-xtrabackup
RUN apt-get update -y && apt-get install -y wget lsb-release vim curl net-tools \
    && wget https://repo.percona.com/apt/percona-release_0.1-4.$(lsb_release -sc)_all.deb \
    && dpkg -i percona-release_0.1-4.$(lsb_release -sc)_all.deb \
    && apt-get update -y && apt-get install -y --force-yes percona-xtrabackup-24 && apt-get install -y pmm-client \
    && apt-get clean -y && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# xtrabackup scripts: to backup mysql data to other storage, e.g. glusterfs
COPY xtrabackup /home/xtrabackup
RUN chmod -R 755 /home/xtrabackup

ENV XTRABACKUP_PATH "/home/xtrabackup/cron/bin"

# my.cnf file attribute must be 644
RUN mkdir -p /config-center/init \
    && mkdir -p /config-center/ln

# slave2master.sh is SQL script to change SLAVE role to MASTER role
COPY slave2master.sh /config-center/slave2master.sh

# /config-center/ln is the mount dir for k8s ConfigMap
# this config file is a sample, will be replaced by ConfigMap setting from Ku8manager
COPY my.cnf.tmpl /config-center/ln/my.cnf
RUN chmod -R 755 /config-center

# customized docker-entrypoint.sh, added MySQL MASTER settings
COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod 755 /usr/local/bin/docker-entrypoint.sh

COPY reConnectMaster.sh /reConnectMaster.sh
RUN chmod 755  /reConnectMaster.sh

# customized container startup script
COPY run.sh /run.sh
RUN chmod 755 /run.sh

ENTRYPOINT ["/run.sh"]
CMD ["mysqld"]
