#!/bin/bash

/**
* @author 驻云科技
* @describe for centos6.5 and ubuntu12.04
*/

pull_images()
{
        docker pull centos
        docker pull ubuntu
        docker pull tutum/lamp
}
if grep -iq centos /etc/issue
then
        yum install -y device-mapper-event-libs docker-io
        /etc/init.d/docker start
        chkconfig docker on
        pull_images
else
        apt-get install -y apt-transport-https
        apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 36A1D7869245C8950F966E92D8576A8BA88D21E9
        bash -c "echo deb https://get.docker.io/ubuntu docker main > /etc/apt/sources.list.d/docker.list"
        apt-get update
        apt-get install --force-yes -y lxc-docker-1.6.2 lxc-docker
        service docker start
        pull_images

fi
