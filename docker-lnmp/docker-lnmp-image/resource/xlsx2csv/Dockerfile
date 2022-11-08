# xlsx2csv inotify
# execl转csv的python插件 需要安装pip

FROM debian:8
MAINTAINER maintain@geneegroup.com

ENV DEBIAN_FRONTEND noninteractive

# apt-get update
RUN apt-get -q update

# install inotify-tools
RUN apt-get install -yq inotify-tools

# install pip
RUN apt-get install -yq python-pip

# install xlsx2csv
RUN pip install xlsx2csv

ADD bin/xlsx2csv /usr/bin/xlsx2csv