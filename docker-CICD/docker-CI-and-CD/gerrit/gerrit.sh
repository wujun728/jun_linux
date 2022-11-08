#!/bin/bash
#

if [[ $# < 1 ]];then
    echo "Usage: $0 <http://gerrit-ip:port>"
    exit 1
fi

WEBURL=$1

export WEBURL

docker-compose up -d
