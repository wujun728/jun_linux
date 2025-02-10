#!/bin/sh  
  
# install epel  
su -c 'rpm -Uvh http://download.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm'  
rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-EPEL-6  
  
# install rpmfusion  
su -c 'yum localinstall -y --nogpgcheck http://download1.rpmfusion.org/free/el/updates/6/x86_64/rpmfusion-free-release-6-1.noarch.rpm http://download1.rpmfusion.org/nonfree/el/updates/6/x86_64/rpmfusion-nonfree-release-6-1.noarch.rpm'  
  
# update base repo  
mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.backup  
wget http://mirrors.163.com/.help/CentOS6-Base-163.repo  
mv CentOS6-Base-163.repo /etc/yum.repos.d/CentOS-Base.repo  
  
yum install -y yum-priorities  
  
yum makecache  
  
# update  
yum update -y