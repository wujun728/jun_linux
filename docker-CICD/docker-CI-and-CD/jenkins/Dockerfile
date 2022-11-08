FOM jenkins

USER root

RUN echo "deb http://apt.dockerproject.org/repo debian-jessie main" > /etc/apt/sources.list.d/docker.list \
    && apt-key adv --keyserver hkp://ha.pool.sks-keyservers.net:80 \
       --recv-keys 58118E89F3A912897C070ADBF76221572C52609D \
    && apt-get update \
    && apt-get -y install ca-certificates sudo docker-engine libyaml-0-2 python-crypto python-ecdsa python-httplib2 python-jinja2 python-markupsafe python-paramiko python-yaml python-netaddr sshpass \
    && rm -rf /var/lib/apt/lists/*  \
    && wget http://archive.ubuntu.com/ubuntu/pool/universe/a/ansible/ansible_2.0.0.2-2_all.deb \
    && dpkg -i ansible_2.0.0.2-2_all.deb \
    && rm ansible_2.0.0.2-2_all.deb

RUN echo "jenkins ALL=NOPASSWD: ALL" >> /etc/sudoers

RUN curl -L "https://github.com/docker/compose/releases/download/1.9.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose; chmod +x /usr/local/bin/docker-compose

RUN sed -i '/host_key_checking/ s/^#//' /etc/ansible/ansible.cfg \
	&& sed -i '/forks/ s/^#\(.*\)5/\1 50/' /etc/ansible/ansible.cfg \
	&& sed -i '/#pipelining/ s/^#\(.*\)False/\1 True/' /etc/ansible/ansible.cfg

USER jenkins
