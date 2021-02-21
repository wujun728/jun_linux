FROM  supermy/docker-debian:7

RUN cat /etc/apt/sources.list

RUN sed -i '1,3d'   /etc/apt/sources.list

RUN echo '#' >> /etc/apt/sources.list

RUN sed -i '$a \
    deb http://mirrors.163.com/debian/ wheezy main non-free contrib \n \
    deb http://mirrors.163.com/debian/ wheezy-proposed-updates main contrib non-free \n \
    deb http://mirrors.163.com/debian-security/ wheezy/updates main contrib non-free \n \
    deb-src http://mirrors.163.com/debian/ wheezy main non-free contrib \n \
    deb-src http://mirrors.163.com/debian/ wheezy-proposed-updates main contrib non-free \n \
    deb-src http://mirrors.163.com/debian-security/ wheezy/updates main contrib non-free \n \
	\
    ' /etc/apt/sources.list

RUN cat /etc/apt/sources.list

# gcc for cgo
RUN apt-get update && apt-get install -y \
		gcc libc6-dev make \
		--no-install-recommends \
	&& rm -rf /var/lib/apt/lists/*

ENV GOLANG_VERSION 1.4.2

# -x 192.168.140:8087
# http://golangtc.com/static/go/go$GOLANG_VERSION.src.tar.gz
# https://golang.org/dl/go$GOLANG_VERSION.src.tar.gz

RUN curl -sSL http://golangtc.com/static/go/go$GOLANG_VERSION.src.tar.gz \
		| tar -v -C /usr/src -xz

RUN cd /usr/src/go/src && ./make.bash --no-clean 2>&1

ENV PATH /usr/src/go/bin:$PATH

RUN mkdir -p /go/src /go/bin && chmod -R 777 /go
ENV GOPATH /go
ENV PATH /go/bin:$PATH
WORKDIR /go

COPY go-wrapper /usr/local/bin/

#### build go end ####

#### build codis begin ####

RUN apt-get update -y && apt-get install -y git

# Add codis
Add codis /go/src/github.com/wandoulabs/codis/
WORKDIR /go/src/github.com/wandoulabs/codis/

#采用下面的数据源，文件不全编译错误
#RUN git clone https://github.com/wandoulabs/codis
#WORKDIR codis

# Install dependency
RUN ./bootstrap.sh
#WORKDIR /go/src/github.com/wandoulabs/codis/sample
WORKDIR  codis/sample


# Expose ports
EXPOSE 19000
EXPOSE 11000
EXPOSE 18087

CMD ./startall.sh && tail -f log/*