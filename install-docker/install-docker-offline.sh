#! /bin/bash
set -e

##### Constants
DOCKER_LIB_HOME=/u01/lib/docker
STEP_COUNT=1
# YOUR_REGISTRY_MIRROR
DOCKER_REGISTRY_MIRROR="$1"
DOCKER_PACKAGE_PATH=`pwd`/packages/
DOCKER_IMAGES_PATH=`pwd`/images

SUPPORT_MAP="
x86_64-centos-7
"

##### Functions
command_installed() {
    if [ -n "$1" ] && (type "$1" &> /dev/null ); then    
        return 0; # true
    fi
    return 1;
}

service_started() {
    if [ -n "$1" ]; then
        info=$(systemctl status $1 | grep 'Active' )
        read prefix status rest <<<"$info"
        if [ $status == 'active' ]; then
            return 0;
        fi
    fi
    return 1;   
}

function add_step_count(){
    ((STEP_COUNT++))
}

# Check if this is a forked Linux distro
check_forked() {

	# Check for lsb_release command existence, it usually exists in forked distros
	if command_exists lsb_release; then
		# Check if the `-u` option is supported
		set +e
		lsb_release -a -u > /dev/null 2>&1
		lsb_release_exit_code=$?
		set -e

		# Check if the command has exited successfully, it means we're in a forked distro
		if [ "$lsb_release_exit_code" = "0" ]; then
			# Print info about current distro
			cat <<-EOF
			You're using '$lsb_dist' version '$dist_version'.
			EOF

			# Get the upstream release info
			lsb_dist=$(lsb_release -a -u 2>&1 | tr '[:upper:]' '[:lower:]' | grep -E 'id' | cut -d ':' -f 2 | tr -d '[:space:]')
			dist_version=$(lsb_release -a -u 2>&1 | tr '[:upper:]' '[:lower:]' | grep -E 'codename' | cut -d ':' -f 2 | tr -d '[:space:]')

			# Print info about upstream distro
			cat <<-EOF
			Upstream release is '$lsb_dist' version '$dist_version'.
			EOF
		else
			if [ -r /etc/debian_version ] && [ "$lsb_dist" != "ubuntu" ] && [ "$lsb_dist" != "raspbian" ]; then
				# We're Debian and don't even know it!
				lsb_dist=debian
				dist_version="$(sed 's/\/.*//' /etc/debian_version | sed 's/\..*//')"
				case "$dist_version" in
					9)
						dist_version="stretch"
					;;
					8|'Kali Linux 2')
						dist_version="jessie"
					;;
					7)
						dist_version="wheezy"
					;;
				esac
			fi
		fi
	fi
}

check_supported() {
	# Check if we actually support this configuration
	if ! echo "$SUPPORT_MAP" | grep "$(uname -m)-$lsb_dist-$dist_version" >/dev/null; then
		cat >&2 <<-'EOF'

		Either your platform is not easily detectable or is not supported by this
		installer script.
		Please visit the following URL for more detailed installation instructions:

		https://docs.docker.com/engine/installation/

		EOF
		exit 1
	fi
}

get_distribution() {
	lsb_dist=""
	# Every system that we officially support has /etc/os-release
	if [ -r /etc/os-release ]; then
		lsb_dist="$(. /etc/os-release && echo "$ID")"
	fi
	# Returning an empty string here should be alright since the
	# case statements don't act unless you provide an actual value
	echo "$lsb_dist"
}

get_package_path() {
    lsb_dist=$( get_distribution )
    if [ $lsb_dist = 'centos' ]; then
        echo $(find $DOCKER_PACKAGE_PATH -type f -name "*.el7.centos.x86_64.rpm" | head -n 1)
    fi
}

install_common_packages() {
    echo "########################"
    echo " $STEP_COUNT. install common tools"
    echo "########################"

    yum localinstall -y --nogpgcheck ${DOCKER_PACKAGE_PATH}common/*.rpm

    add_step_count
}

do_install_docker() {
    echo "########################"
    echo " $STEP_COUNT. install docker engine"
    echo "########################"

    docker_config_dir=/etc/systemd/system/docker.service.d    

    if command_installed 'docker'; then
        echo "docker engine must be already installed."
    else
        docker_package=$( get_package_path )
        if [ -z "$docker_package" ]; then
            echo 'cant find docker ce package.'
    		exit 1
        fi
        yum install -y $docker_package

        # set docker config
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
    fi

    add_step_count
}

install_docker_compose() {
    echo "########################"
    echo " $STEP_COUNT. install Docker-Compose"
    echo "########################"

    if command_installed 'docker-compose'; then
        echo "docker-compose must be already installed."
    else
        cp ${DOCKER_PACKAGE_PATH}docker-compose-Linux-x86_64* /usr/local/bin/docker-compose
        chmod +x /usr/local/bin/docker-compose
    fi

    add_step_count
}

install_supervisor() {
    echo "########################"
    echo " $STEP_COUNT. install Supervisor"
    echo "########################"

    if command_installed 'supervisord'; then
        echo "supervisord must be already installed."
    else
        pip_package_path=${DOCKER_PACKAGE_PATH}pip
        # install pip
        python $pip_package_path/get-pip.py --no-index --find-links=$pip_package_path
        
        # install supervisor
        pip install --no-index --find-links=${DOCKER_PACKAGE_PATH}pip/supervisor supervisor
    fi

    add_step_count
}

load_docker_images() {
    echo "########################"
    echo " $STEP_COUNT. load docker images."
    echo "########################"

    hello_image='hello-world'

    if ! docker images | grep -q "$hello_image" ; then
        docker load --input $DOCKER_IMAGES_PATH/$hello_image.tar
    fi

    add_step_count
}

main() {
    install_common_packages
    do_install_docker
    install_docker_compose
    install_supervisor
    load_docker_images

    docker run --rm hello-world
}

main

# see also https://get.docker.com/
