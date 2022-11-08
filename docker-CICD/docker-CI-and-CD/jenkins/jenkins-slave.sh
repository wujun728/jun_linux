#!/bin/bash
#

if [[ $# < 3 ]];then
    echo "Usage: $0 <http://master-ip:port> <secret> <slave-name>"
    exit 1
fi

JENKINS_URL=$1
SECRET=$2
SLAVE_NAME=$3

export JENKINS_URL SECRET SLAVE_NAME

docker-compose -f docker-compose-jenkins-slave.yml up -d 
