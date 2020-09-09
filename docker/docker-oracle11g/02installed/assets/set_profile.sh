#!/usr/bin/env bash

set -e

source /assets/colorecho

trap "echo_red '******* ERROR: Something went wrong.'; exit 1" SIGTERM
trap "echo_red '******* Caught SIGINT signal. Stopping...'; exit 2" SIGINT

echo_yellow ""
echo_yellow "Set profile for oracle user"
cat /assets/conf/profile 
cat /assets/conf/profile >> /home/oracle/.bash_profile
cat /assets/conf/profile >> /home/oracle/.bashrc
