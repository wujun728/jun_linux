FROM debian:jessie

ADD http://192.168.1.1:9999/wkhtmltox-0.13.0-alpha-7b36694_linux-jessie-amd64-1.deb /alidata/opt/tools/wkhtmltox.deb

WORKDIR /alidata/opt/tools

RUN dpkg --force-all -i wkhtmltox.deb

VOLUME ["/usr/local/bin"]
