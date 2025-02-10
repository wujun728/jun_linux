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

docker run -it --rm --name java-1.8.181 ${DOCKER_REPOSTORY}/${DOCKER_PROJECT}/${DOCKER_IMAGE}:java-1.8.181 ""
docker run -it --rm --name java-1.8.181 -p 10022:22 ${DOCKER_REPOSTORY}/${DOCKER_PROJECT}/${DOCKER_IMAGE}:java-1.8.181 ""
docker run -it --rm --name java-1.8.181 -p 18080:8080 -p 10001:10001 -p 10002:10002 ${DOCKER_REPOSTORY}/${DOCKER_PROJECT}/${DOCKER_IMAGE}:java-1.8.181 "bash"
