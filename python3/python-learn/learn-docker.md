#docker 使用总结

###1. 搜索image
docker search archlinux

###2. 下载一个image
docker pull archlinux


###3. 查看下载的images
docker images


###4. 交互式运行下载的image
docker run -i -t base/archlinux /bin/bash


###5. 安装ssh
docker run -i -t base/archlinux /bin/bash
passwd
pacman -Sy
pacman -S openssh
vi /etc/ssh/sshd_config #开启密码认证


###6. 后台方式运行image
docker run -d base/archlinux /usr/bin/sshd -D #不指定端口的话虚拟机的22端口映射到本机的随机端口


###7. 端口映射 本机2222映射到虚拟机22
docker run -d -p 2222:22 base/archlinux /usr/bin/sshd -D
ssh root@localhost -p 2222


###8. 目录映射
docker run -i -t -v /home/demo/data:/data base/archlinux /bin/bash


###9. 创建container
docker run #执行成功就会自动创建container


###10. 查看所有container
docker ps -a


###11. 删除container
docker rm container_id


###12. 删除image
docker rmi image_id #得先删除image被依赖的container再删除image

###13. 交互式启动一个container
docker ps -a #看到已有的containers 然后
docker start -i container_id


###14. 停止一个container
docker stop container_id
