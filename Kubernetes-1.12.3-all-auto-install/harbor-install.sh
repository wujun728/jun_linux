# 部署Harbor仓库
# 安装docker-compose
curl -L "https://github.com/docker/compose/releases/download/1.23.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
docker-compose --version

# 下载harbor企业级Registry仓库 
cd ~
wget https://storage.googleapis.com/harbor-releases/release-1.6.0/harbor-offline-installer-v1.6.3.tgz
tar zxvf harbor-offline-installer-v1.6.3.tgz
cd harbor

# 修改配置文件的hostname与password
sed -i s/hostname.*/hostname=192.168.119.212/g harbor.cfg
sed -i s/harbor_admin_password.*/harbor_admin_password=admin/g harbor.cfg

# 将当前仓库添加到docker的配置文件中去
sed -i s/\"insecure-registries\".*/\"insecure-registries\":[\"192.168.119.212\"]/g /etc/docker/daemon.json
systemctl daemon-reload
systemctl restart docker
docker info 

# 开启harbor
./prepare
./install.sh

# 查看启动情况
docker-compose ps