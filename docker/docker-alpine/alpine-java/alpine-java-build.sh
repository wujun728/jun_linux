#!/usr/bin/env bash

set -e

# set envirionment
PWD=`pwd`
BASE_DIR="${PWD}"
SOURCE="$0"
while [ -h "$SOURCE"  ]; do # resolve $SOURCE until the file is no longer a symlink
    BASE_DIR="$( cd -P "$( dirname "$SOURCE"  )" && pwd  )"
    SOURCE="$(readlink "$SOURCE")"
    [[ $SOURCE != /*  ]] && SOURCE="$BASE_DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
BASE_DIR="$( cd -P "$( dirname "$SOURCE"  )" && pwd  )"

cd ${BASE_DIR}

DOCKER_REPOSTORY=myharbor.com
DOCKER_PROJECT=base
DOCKER_IMAGE=alpine
DOCKER_FILE=alpine-java-dockerfile

docker build --rm \
             --no-cache \
             --add-host assets-cdn.github.com:151.101.72.133 \
             --add-host github.global.ssl.fastly.net:151.101.13.194 \
             --add-host github.global.ssl.fastly.net:151.101.73.194 \
             --add-host github.global.ssl.fastly.net:151.101.113.194 \
             --add-host github.com:192.30.253.112 \
             --add-host github.com:192.30.253.113 \
             --add-host codeload.github.com:192.30.253.120 \
             --add-host codeload.github.com:192.30.253.121 \
             --add-host raw.githubusercontent.com:151.101.72.133 \
             --build-arg MYJRE_VER=8u181 \
             --build-arg MYJRE_URL=http://download.oracle.com/otn-pub/java/jdk/8u181-b13/96a7b8442fe848ef90c96a2fad6ed6d1/server-jre-8u181-linux-x64.tar.gz \
             -t ${DOCKER_REPOSTORY}/${DOCKER_PROJECT}/${DOCKER_IMAGE}:java-1.8.181 \
             -t ${DOCKER_REPOSTORY}/${DOCKER_PROJECT}/${DOCKER_IMAGE}:java-1.8 \
             -f ${DOCKER_FILE} .
