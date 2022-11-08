#!/bin/bash
# General docker installation script

command_exists() {
	command -v "$@" > /dev/null 2>&1
}

os_debian() {
	apt-get update
	apt-get -y install docker-engine python-pip
	command_exists pip || pip install docker-compose==1.9.0
}

os_centos() {
	yum makecache fast
	yum -y install libsepol docker-engine python-pip 
	command_exists pip || pip install docker-compose==1.9.0
}

yum_repo() {
	echo """
[base]
name=CentOS-$1 - Base
baseurl=https://mirrors.tuna.tsinghua.edu.cn/centos/$1/os/x86_64/
#mirrorlist=http://mirrorlist.centos.org/?release=$1&arch=x86_64&repo=os
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-$1

#released updates
[updates]
name=CentOS-$1 - Updates
baseurl=https://mirrors.tuna.tsinghua.edu.cn/centos/$1/updates/x86_64/
#mirrorlist=http://mirrorlist.centos.org/?release=$1&arch=x86_64&repo=updates
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-$1

#additional packages that may be useful
[extras]
name=CentOS-$1 - Extras
baseurl=https://mirrors.tuna.tsinghua.edu.cn/centos/$1/extras/x86_64/
#mirrorlist=http://mirrorlist.centos.org/?release=$1&arch=x86_64&repo=extras
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-$1

#additional packages that extend functionality of existing packages
[centosplus]
name=CentOS-$1 - Plus
baseurl=https://mirrors.tuna.tsinghua.edu.cn/centos/$1/centosplus/x86_64/
#mirrorlist=http://mirrorlist.centos.org/?release=$1&arch=x86_64&repo=centosplus
gpgcheck=1
enabled=0
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-$1

""" > /etc/yum.repos.d/CentOS-Base.repo


	echo """
[dockerrepo]
name=Docker Repository
baseurl=https://mirrors.tuna.tsinghua.edu.cn/docker/yum/repo/centos$1
enabled=1
gpgcheck=1
gpgkey=https://mirrors.tuna.tsinghua.edu.cn/docker/yum/gpg
""" > /etc/yum.repos.d/docker.repo
}

apt_os_version=(wheezy jessie 12.04 14.04 16.04)
yum_os_version=(centos:6 centos:7)


if command_exists apt-get; then
	sudo apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
	for v in ${apt_os_version[@]};do
		APT_VERSION=$(grep -om1 $v /etc/os-release)
		case ${APT_VERSION} in
			wheezy)
				echo "deb https://mirrors.tuna.tsinghua.edu.cn/docker/apt/repo debian-wheezy main" | sudo tee /etc/apt/sources.list.d/docker.list
				os_debian	
				exit 0
				;;
			jessie)
				echo "deb https://mirrors.tuna.tsinghua.edu.cn/docker/apt/repo debian-jessie main" | sudo tee /etc/apt/sources.list.d/docker.list
				os_debian	
				exit 0
				;;
			12.04)
				echo "deb https://mirrors.tuna.tsinghua.edu.cn/docker/apt/repo ubuntu-precise main" | sudo tee /etc/apt/sources.list.d/docker.list
				os_debian	
				exit 0
				;;
			14.04)
				echo "deb https://mirrors.tuna.tsinghua.edu.cn/docker/apt/repo ubuntu-trusty main" | sudo tee /etc/apt/sources.list.d/docker.list
				os_debian	
				exit 0
				;;
			16.04)
				echo "deb https://mirrors.tuna.tsinghua.edu.cn/docker/apt/repo ubuntu-xenial main" | sudo tee /etc/apt/sources.list.d/docker.list
				os_debian	
				exit 0
				;;
		esac
	done
elif command_exists yum; then
	yum clean all
	for v in ${yum_os_version[@]};do
		YUM_VERSION=$(grep -om1 $v /etc/os-release)
		case ${YUM_VERSION} in
			centos:6)
				yum_repo 6
				os_centos
				exit 0
				;;
			centos:7)
				yum_repo 7
				os_centos
				exit 0
			;;
		esac
	done
fi
