#! /bin/bash
mkdir -p /data
mkdir -p /data/www
mkdir -p /data/mysqlData
mkdir -p /data/nginx
mkdir -p /data/nginx/ca
mkdir -p /data/nginx/conf.d
mkdir -p /data/php/conf.d
curl -o /data/php/conf.d/php.ini https://raw.githubusercontent.com/php/php-src/php-${PHP_VERSION}/php.ini-production
cp nginx/conf.d/default.conf /data/nginx/conf.d
cp nginx/nginx.conf /data/nginx
cp app/src/index.php /data/www/

sudo yum -y update
sudo tee /etc/yum.repos.d/docker.repo <<-'EOF'
[dockerrepo]
name=Docker Repository
baseurl=https://yum.dockerproject.org/repo/main/centos/7/
enabled=1
gpgcheck=1
gpgkey=https://yum.dockerproject.org/gpg
EOF
sudo yum -y install docker-engine
sudo systemctl start docker
sudo systemctl enable docker.service
sudo yum -y install epel-release
sudo yum -y install python-pip
sudo pip install -U docker-compose
docker-compose up -d --build
