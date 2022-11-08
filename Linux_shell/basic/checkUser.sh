#!/bin/bash
#检测用户
if [ $UID -ne 0 ]       # root UID=0
then
    echo "please run as root"
else
    echo "go on.."
fi
