#!/bin/bash

if [ ! -x "/opt" ];then
	mkdir /opt
fi

mirror="https://mirrors.tuna.tsinghua.edu.cn/apache/"
url="${mirror}kafka/${KAFKA_VERSION}/kafka_${SCALA_VERSION}-${KAFKA_VERSION}.tgz"
wget "${url}" -O "/tmp/kafka_${SCALA_VERSION}-${KAFKA_VERSION}.tgz"