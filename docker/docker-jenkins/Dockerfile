# 基于jenkins:1.609.1官方镜像
FROM jenkins:1.609.1

USER root
# 安装sudo
RUN apt-get update \
  && apt-get install -y sudo \
  && rm -rf /var/lib/apt/lists/*
# 给jenkins用户赋予sudo权限
RUN echo "jenkins ALL=NOPASSWD: ALL" >> /etc/sudoers

USER jenkins
# plugins.txt 拷贝
COPY plugins.txt /usr/share/jenkins/plugins.txt
# 下载相应的插件，/usr/local/bin/plugins.sh可以参加jenkins官方镜像源码https://github.com/jenkinsci/docker
RUN /usr/local/bin/plugins.sh /usr/share/jenkins/plugins.txt
