#! /bin/bash

VERSION='7.4.1708'

PACKAGES_MAP="
audit-libs-python-2.7.6-3.el7.x86_64.rpm
libsemanage-python-2.5-8.el7.x86_64.rpm
libtool-ltdl-2.4.2-22.el7_3.x86_64.rpm
container-selinux-2.28-1.git85ce147.el7.noarch.rpm
libcgroup-0.41-13.el7.x86_64.rpm
libseccomp-2.3.1-3.el7.x86_64.rpm
python-IPy-0.75-6.el7.noarch.rpm
checkpolicy-2.5-4.el7.x86_64.rpm
policycoreutils-python-2.5-17.1.el7.x86_64.rpm
setools-libs-3.3.8-1.1.el7.x86_64.rpm
"

OS_REPO="https://mirrors.aliyun.com/centos/$VERSION/os/x86_64/Packages/"
EXTRAS_REPO="https://mirrors.aliyun.com/centos/$VERSION/extras/x86_64/Packages/"

packages=( $PACKAGES_MAP )

for name in ${packages[@]}; do
    file=`pwd`/$name
    if [ -f $file ]; then
        echo "$name || was already install."
    else
        wget $OS_REPO$name
        if [ ! -f $file ]; then
            wget $EXTRAS_REPO$name            
        fi
    fi
done
