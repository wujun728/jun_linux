#!/bin/bash

yum -y update

curl -sSL https://get.daocloud.io/docker | sh 
sudo chkconfig docker on 
sudo systemctl start docker

sudo systemctl status docker
