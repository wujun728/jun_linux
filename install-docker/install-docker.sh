#! /bin/bash

##### Constants
DOCKER_LIB_HOME=/u01/lib/docker
STEP_COUNT=1
# YOUR_REGISTRY_MIRROR
DOCKER_REGISTRY_MIRROR="$1"

##### Functions
function command_installed(){
    if [ -n "$1" ] && (type "$1" &> /dev/null ); then    
        return 0; # true
    fi
    return 1;
}

function service_started(){
    if [ -n "$1" ]; then
        info=$(systemctl status $1 | grep 'Active' )
        read prefix status rest <<<"$info"
        if [ $status == 'active' ]; then
            return 0;
        fi
    fi
    return 1;   
}

function install_common_package(){
    echo "########################"
    echo " $STEP_COUNT. install common tools"
    echo "########################"
    
    if command_installed 'pip' && command_installed 'git' &&  command_installed 'iptables'; then
        echo "common packages must be already installed."
    else
        yum makecache
        yum install -y net-tools vim git \
            ntsysv setuptool yum-utils python-pip python-setuptools \
            lsof bzip2 unzip tar gcc wget nfs-utils
        yum install -y policycoreutils-python
        # install pip
        curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"
        python get-pip.py
        rm -f get-pip.py
        mkdir ~/.pip/
        tee ~/.pip/pip.conf <<-'EOF'
[global]
index-url = http://mirrors.aliyun.com/pypi/simple/
[install]
trusted-host=mirrors.aliyun.com
EOF
    fi

    add_step_count 
}

function install_docker_engine(){

    docker_repo_file=/etc/yum.repos.d/docker-ce.repo
    docker_config_dir=/etc/systemd/system/docker.service.d

    echo "########################"
    echo " $STEP_COUNT. install docker engine"
    echo "########################"

    if command_installed 'docker'; then
        echo "docker engine must be already installed."
    else
        curl -o $docker_repo_file https://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
        yum makecache fast
        # Uninstall old versions
        yum remove docker \
                  docker-common \
                  docker-selinux \
                  docker-engine

        yum install -y docker-ce
        mkdir -p $docker_config_dir
        if [ -n "$DOCKER_REGISTRY_MIRROR" ]; then
            tee "$docker_config_dir/docker.conf" <<-EOF
[Service]
ExecStart=
ExecStart=/usr/bin/dockerd \
  --graph=${DOCKER_LIB_HOME} \
  --registry-mirror=${DOCKER_REGISTRY_MIRROR}
EOF
        else
            tee "$docker_config_dir/docker.conf" <<-EOF
[Service]
ExecStart=
ExecStart=/usr/bin/dockerd \
  --graph=${DOCKER_LIB_HOME}
EOF
        fi
        systemctl daemon-reload
        systemctl restart docker
        systemctl enable docker
        # enable IPv4
        sysctl -w net.ipv4.ip_forward=1

    fi

    add_step_count
}

function install_docker_compose(){
    echo "########################"
    echo " $STEP_COUNT. install Docker-Compose"
    echo "########################"

    if command_installed 'docker-compose'; then
        echo "docker-compose must be already installed."
    else
        pip install docker-compose 
    fi

    add_step_count
}

function install_supervisor(){
    echo "########################"
    echo " $STEP_COUNT. install Supervisor"
    echo "########################"

    if command_installed 'supervisord'; then
        echo "supervisord must be already installed."
    else
        easy_install pip
        pip install supervisor
    fi

    add_step_count
}

function add_step_count(){
    ((STEP_COUNT++))
}

function main(){
    install_common_package
    install_docker_engine
    install_docker_compose
    install_supervisor
}

main

