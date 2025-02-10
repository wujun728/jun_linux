1.搜索FastDFS镜像文件 docker search fastdfs



2.下载对应的镜像文件 docker pull season/fastdfs



3.查看文件镜像     docker images



4.创建挂载文件夹

cd /data

mkdir fastdfs

cd fastdfs

mkdir tracker storage

cd storage 

mkdir storage_data

cd ../tracker/

mkdir tracker_data



 5.运行tracker容器

docker run -ti -d --name trakcer --restart=always -v /data/fastdfs/tracker/tracker_data:/fastdfs/tracker/data -p 22122:22122  season/fastdfs tracker



6.运行storage容器

    docker run -tid --name storage --restart=always -v /data/fastdfs/storage/storage_data:/fastdfs/storage/data -v /data/fastdfs/storage/store_path:/fastdfs/store_path -p 23000:23000 -e TRACKER_SERVER:192.168.64.4:22122 -e GROUP_NAME=group1 season/fastdfs storage

7. 进入storage容器，到storage的配置文件中配置http访问的端口，配置文件在fdfs_conf目录下的storage.conf

进入storage容器查看ip

docker exec -it storage bash

cd /fdfs_conf/

more storage.conf



 将文件复制复制一份出来修改成想要的ip

 docker cp storage:/fdfs_conf/storage.conf ~/
 vi ~/storage.conf

 

 将修改好的文件复制到容器中

    docker cp ~/storage.conf storage:/fdfs_conf/
8.重启容器
     docker stop storage
     docker start storage

 

 9.查看tracker容器与storage容器关联

     docker exec -it storage bash
     cd fdfs_conf
     fdfs_monitor storage.conf



 10.在docker模拟客户端上传文件到storage容器

     开启一个客户端
     docker run -tid --name fdfs_sh -p 13000:13000 season/fastdfs sh
     更改配置文件，因为之前已经改过一次了，所以现在直接拷贝
     docker cp ~/storage.conf  fdfs_sh:/fdfs_conf/
    
     进入fdfs_sh容器
     docker exec -it fdfs_sh bash
    
     创建文件b.txt
     echo hello>b.txt
    
     上传文件
     cd fdfs_conf
     fdfs_upload_file storage.conf /b.txt



 

 退出容器，查看文件

cd /data/fastdfs/storage/store_path/data/00/00



可能遇到问题

安装过程需要关闭机器防火墙

     关闭防火墙
    systemctl stop firewalld
    vi /etc/sysconfig/selinux
    将SELINUX的值改成disabled
    
    重启服务器
    reboot

以上是安装fastdfs全过程
————————————————
版权声明：本文为CSDN博主「客官酒来了」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/qq_35744706/article/details/124163127