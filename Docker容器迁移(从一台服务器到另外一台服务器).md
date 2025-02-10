## DOCKER服务迁移(从一台服务器到另一台服务器)

以Nginx为例，其他容易也是一样的:

#### 1、首先在183服务器部署NGINX服务:

①拉取镜像

```bash
docker pull nginx:latest
```

![在这里插入图片描述](https://www.freesion.com/images/559/a3081acc8c5e9ca3c50a9ac4ad8f61ff.png)
②运行容器

```bash
docker run --name nginx-test -p 12308:80 -d nginx
```

> 参数说明：
> –name nginx-test：容器名称。
> -p 12308:80： 端口进行映射，将本地 12308 端口映射到容器内部的 80 端口。
> -d nginx： 设置容器在在后台一直运行。

③查看容器进程

```bash
docker ps -a
```

![在这里插入图片描述](https://www.freesion.com/images/542/a338084efd57221234fc1588d59bb406.png)
访问192.168.1.183:12308，访问成功：
![在这里插入图片描述](https://www.freesion.com/images/493/62e49be060b596d24693170a2a376dcd.png)

#### 2、将容器保存为镜像

> docker commit 容器名称 镜像名称
>
> docker commit 容器ID  新镜像名称

```bash
docker commit nginx-test nginxtest
docker commit nginx-test nginxtest

docker commit kkfileview  kkfileview_new
```

这是可以看到多出来一个Nginx的镜像，这个镜像就是我们刚刚生成的。
![在这里插入图片描述](https://www.freesion.com/images/782/7ed4f25bf7a3b7a06d75be269405f966.png)

#### 3、将镜像打包成TAR文件

> docker save -o xxx.tar 镜像名称

```bash
docker save -o nginxTest.tar nginxtest
或
docker save nginxtest > nginxTest.tar

docker save -o kkfileview_new.tar kkfileview_new
```

![在这里插入图片描述](https://www.freesion.com/images/947/23b4b020ac0a15108a655a8bc3813073.png)
注意：如需将多个镜像合并成一个tar包：

> docker save [images] [images] > [name.tar]

#### 4、将TAR文件下载下来，上传到其他服务器(185)

直接down就可以了



#### 4.1、使用scp 进行linux服务器之间数据拷贝

使用scp 进行linux服务器之间数据拷贝
登录到 文件源服务器   执行 scp 直接可以实现linux 服务器之间的拷贝

`scp local_file remote_username@remote_ip:remote_folder`      

`或者`      

`scp local_file remote_username@remote_ip:remote_file`      

`或者`      

`scp local_file remote_ip:remote_folder`      

`或者`      

`scp local_file remote_ip:remote_file`  



scp   /root/kkfileview_new.tar       root@175.24.233.55:/root/  



#### 5、镜像恢复

执行以下命令进行恢复:

```bash
docker load < xxx.tar
或
docker load -i xxx.tar
123
```

![在这里插入图片描述](https://www.freesion.com/images/29/9372ffa9b81cbe45742156303ac9bc0d.png)
此时185服务器的docker中就出现了nginxtest镜像
![在这里插入图片描述](https://www.freesion.com/images/43/16973cc238dd81f50f28faedd3021333.png)
执行以下命令启动容器:

```bash
 docker run --name nginx-test -p 12309:80 -d nginxtest
1
```

![在这里插入图片描述](https://www.freesion.com/images/817/db8abfdc24d7210f2e6902e076cced59.png)
访问192.168.1.185:12309，访问成功：
![在这里插入图片描述](https://www.freesion.com/images/134/dc0210f6c4aa56407d89e41921972e5e.png)