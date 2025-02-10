# docker安装oracle数据库史上最全步骤（带图文）



oracle作为全球最强大的关系型数据库，应用在各行各业。了解并使用过oracle的工程师应该都有体会，在Linux中安装oracle非常麻烦，相信每个人也会遇到各种坑。为了一次装好，也方便将来直接可以导出镜像在各平台移植使用，所以选择用docker安装，并做详细记录，方便有需要的人参考。

1、安装docker环境。（这一步默认您已经学会了docker虚拟化技术，如果还是不会，私聊可以为你解答）

2、开始拉取oracle镜像

```text
         docker pull registry.cn-hangzhou.aliyuncs.com/helowin/oracle_11g
```

大约有6个G，需要一段时间，抽根烟静等大约10分钟。

> **（自己做了一个镜像，有需要的同学可以关注+私我索取！）**

3、下载完成后，查看镜像

```text
     docker images
```



![img](https://pic3.zhimg.com/80/v2-7df3bdeec2468442f5d75a8426597b9e_720w.webp)

![img](https://pic1.zhimg.com/80/v2-4f89913ab376925632be5823a038f938_720w.webp)



4、创建容器

```text
        docker run -d -p 1521:1521 --name oracle11g registry.cn-hangzhou.aliyuncs.com/helowin/oracle_11g
```

可以写成shell脚本，下次打开oracle数据库就可以一条命令创建容器。

shell脚本如下：

```text
# BEGIN ANSIBLE MANAGED BLOCK
#!/bin/bash
docker rm -f oracle11;
docker run -it -d -p 1521:1521 -v /data/oracle:/data/oracle --name oracle11 registry.cn-hangzhou.aliyuncs.com/helowin/oracle_11g
# END ANSIBLE MANAGED BLOCK
```



**但为了保存上一次容易的配置值，是不建议写这个shell脚本的，下次打开直接用docker start oracle11命令打开。**

如果创建成功能会返回容器id

5、进入镜像进行配置

```text
     docker exec -it oracle11 bash
```



![img](https://pic3.zhimg.com/80/v2-8581494efd0e282a9a5219771150c40a_720w.webp)

![img](https://pic1.zhimg.com/80/v2-4f89913ab376925632be5823a038f938_720w.webp)



6、进行软连接

```text
      sqlplus /nolog
```

发现没有该命令，所以切换root用户。

```text
su root 
```

输入密码：helowin

7、编辑profile文件配置ORACLE环境变量

打开：vi /etc/profile ，在文件最后写上下面内容：

```text
            export ORACLE_HOME=/home/oracle/app/oracle/product/11.2.0/dbhome_2
            export ORACLE_SID=helowin
            export PATH=$ORACLE_HOME/bin:$PATH
```



![img](https://pic2.zhimg.com/80/v2-50091fcfb09083142520b37f9fd26d3d_720w.webp)

![img](https://pic1.zhimg.com/80/v2-4f89913ab376925632be5823a038f938_720w.webp)


8、保存后执行source /etc/profile 加载环境变量；

9、创建软连接

```text
            ln -s $ORACLE_HOME/bin/sqlplus /usr/bin
```

10、切换到oracle 用户



![img](https://pic4.zhimg.com/80/v2-ab62c1da0b9da40629b033578a85bc9f_720w.webp)

![img](https://pic1.zhimg.com/80/v2-4f89913ab376925632be5823a038f938_720w.webp)



*这里还要说一下，一定要写中间的内条 - 必须要，否则软连接无效*

11、登录sqlplus并修改sys、system用户密码

```text
      sqlplus /nolog   --登录
     conn /as sysdba  --
     alter user system identified by system;--修改system用户账号密码；
    alter user sys identified by system;--修改sys用户账号密码；
    create user test identified by test; -- 创建内部管理员账号密码；
    grant connect,resource,dba to yan_test; --将dba权限授权给内部管理员账号和密码；
    ALTER PROFILE DEFAULT LIMIT PASSWORD_LIFE_TIME UNLIMITED; --修改密码规则策略为密码永不过期；（会出现坑，后面讲解）
    alter system set processes=1000 scope=spfile; --修改数据库最大连接数据；
```



![img](https://pic1.zhimg.com/80/v2-3ab67f1c92ea1f7e23308bad0113d3a4_720w.webp)

![img](https://pic1.zhimg.com/80/v2-4f89913ab376925632be5823a038f938_720w.webp)


12、修改以上信息后，需要重新启动数据库；

```text
conn /as sysdba
shutdown immediate; --关闭数据库
startup; --启动数据库
exit：退出软链接
```

------

***上面提到的其中一个坑说明：\***

当执行修改密码的时候出现 ： database not open

提示数据库没有打开，不急按如下操作

输入：alter database open;

注意了：这里也许还会提示 ： ORA-01507: database not mounted

![img](https://pic2.zhimg.com/80/v2-cd16214299b8166734131326da5098a5_720w.webp)

![img](https://pic1.zhimg.com/80/v2-4f89913ab376925632be5823a038f938_720w.webp)



**解决办法：**

输入：alter database mount;

输入 ：alter database open;



![img](https://pic1.zhimg.com/80/v2-fafc9ee08fefbd88eb7a8adc6beb18b8_720w.webp)

![img](https://pic1.zhimg.com/80/v2-4f89913ab376925632be5823a038f938_720w.webp)



然后就可执行 修改数据库密码的命令了

改完之后输入：ALTER PROFILE DEFAULT LIMIT PASSWORD_LIFE_TIME UNLIMITED;

**刷新下表 exit 是退休sql 软连接**



![img](https://pic3.zhimg.com/80/v2-cb937277f0fb8974d666fd124fed224e_720w.webp)