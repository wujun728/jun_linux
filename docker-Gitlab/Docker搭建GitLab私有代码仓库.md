用Docker搭建GitLab私有代码仓库

git是当下如日中天的版本管理系统，比如我们常用的github/gitee都是通过git来管理项目的。有很多现成的互联网的git服务提供给大家使用，例如号称程序员社交网络的 GitHub，还有低调好用的 bitbucket 。这些给个人使用或者公司用来做开源使用都没有什么问题。但如果在部门内推广使用就会涉及到代码不能公开或者额外的费用的问题。

正好 gitlab 公司提供了 gitlab 社区版，看了看基本满足了部门内 git 管理的需求。gitlab 提供了各种各样的安装方式，最方便的当然还是 docker 方式的安装，适合我这种不想多折腾的。抽空搭建了一个。也趟了几个坑，将步骤记录如下，希望对其他有此需求的人有所帮助。

gitlab本是可以支持自托管的，完全适合个人或团队使用。安装前服务器请至少具有4G的内存。

![img](https://pic.rmb.bdstatic.com/bjh/down/d2fd6bc40960cc888000608c0d90e982.png@wm_2,t_55m+5a625Y+3L+i/kOe7tOi0vOiIuQ==,fc_ffffff,ff_U2ltSGVp,sz_50,x_32,y_32)

### 1.docker 安装

既然是基于 docker 来安装 gitlab ，首先是安装 docker 环境了。我是在 CentOS7 的基础上安装的。可以根据官网的指南来安装。

### 删除旧版本的 docker

旧版本的 docker 的叫做 docker 或者 docker-engine，如果系统中已经安装旧版本，则需要删除。通过以下命令删除旧的 docker 版本

```
yum remove docker docker-common docker-selinux docker-engine
```

### 一键安装docker

```
curl -fsSL https://get.docker.com | bash -s docker --mirror Aliyun
```

### 一键安装docker-compose

```
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose && chmod +x /usr/local/bin/docker-compose
```

### 启动 docker

执行如下的命令启动 docker 的服务

```
systemctl start docker
# 设置为开机启动
systemctl enable docker
```

执行如下命令查看 docker 信息

```
docker -v
```

可以看到如下的信息

![img](https://pic.rmb.bdstatic.com/bjh/down/a4737192cd2cfea14fc9f8f379199ac9.png@wm_2,t_55m+5a625Y+3L+i/kOe7tOi0vOiIuQ==,fc_ffffff,ff_U2ltSGVp,sz_41,x_26,y_26)

(略)如果我们的根分区空间比较小，想要自定义docker的运行目录，可以修改以下的配置文件：

```
mkdir /etc/docker
mkdir /home/docker
vi /etc/docker/daemon.json
```

输入以下内容，比如我将docker放置在/home/docker目录下：

```
{
  "graph":"/home/docker"
}
```

使配置生效：

```
systemctl daemon-reload
systemctl restart docker
```

查看配置结果是否生效：

```
docker info
```

如果Root Dir出现我们配置的目录，则设置正确。![img](https://pic.rmb.bdstatic.com/bjh/down/6d2a592323fe3a507b32ff1de3b71156.png@s_0,w_2000%7Cwm_2,t_55m+5a625Y+3L+i/kOe7tOi0vOiIuQ==,fc_ffffff,ff_U2ltSGVp,sz_50,x_32,y_32)

### 2.安装 gitlab

### 下载镜像

执行下面的命令，从 docker 的镜像仓库中下载 gitlab 社区版的镜像

```
docker pull gitlab/gitlab-ce:latest
```

镜像有 1g 多，所以需要等待一段时间

### 数据持久化保存

建立了目录 /opt/docker/gitlab 来保存 gitlab 容器中的数据

```
# 创建一个用于存放gitlab数据的目录
mkdir -p /opt/docker/gitlab
# 进入到创建的目录下
cd /opt/docker/gitlab
# 新建一个docker-compose.yml文件
vim docker-compose.yml
```

将下面的内容粘贴进去。

```
version: '3.6'
services:
  web:
    image: 'gitlab/gitlab-ee:latest'
    restart: always
    container_name: 'gitlab'
    hostname: 'gitlab'
    environment:
      GITLAB_OMNIBUS_CONFIG: |
        external_url 'http://192.168.31.95:8929'
        gitlab_rails['gitlab_shell_ssh_port'] = 2224
    ports:
      - '8929:8929'
      - '2224:22'
    volumes:
      - '$GITLAB_HOME/config:/etc/gitlab'
      - '$GITLAB_HOME/logs:/var/log/gitlab'
      - '$GITLAB_HOME/data:/var/opt/gitlab'
    shm_size: '256m
```

注意，其中的external_url后面的ip地址需要修改为自己服务器的内网ip，完成后保存退出。

### 3.运行 gitlab

执行以下命令启动gitlab：

```
# 将下面的地址改成你存放gitlab持久化数据的地址，比如我的地址为/opt/docker/gitlab
export GITLAB_HOME=/opt/docker/gitlab
docker-compose up -d
```

注意警告，需要提前把GITLAB_HOME变量设置。

![img](https://pic.rmb.bdstatic.com/bjh/down/78568fc40b04103ec4e3fb1fe0ae8f78.png@s_0,w_2000%7Cwm_2,t_55m+5a625Y+3L+i/kOe7tOi0vOiIuQ==,fc_ffffff,ff_U2ltSGVp,sz_50,x_32,y_32)

放行8929和2224两个端口。

```
firewall-cmd --add-port={8929,2224}/tcp --permanent
firewall-cmd --reload
```

![img](https://pic.rmb.bdstatic.com/bjh/down/62e90b4413fe3eca6b8caba535e3e0de.png@wm_2,t_55m+5a625Y+3L+i/kOe7tOi0vOiIuQ==,fc_ffffff,ff_U2ltSGVp,sz_50,x_32,y_32)image

### 4.访问

访问前，先查一下gitlab的运行状态，在服务器上执行：

```
docker logs -f gitlab
```

等待执行，启动时间可能会比较长，最终停止滚动，发现系统执行没有报错，系统正常运行。使用ctrl + c 组合键退出。

![img](https://pic.rmb.bdstatic.com/bjh/down/9f1377f32acfe93caade6a654dacb51e.png@s_0,w_2000%7Cwm_2,t_55m+5a625Y+3L+i/kOe7tOi0vOiIuQ==,fc_ffffff,ff_U2ltSGVp,sz_50,x_32,y_32)

使用以下命令查看一下初始密码：

```
docker exec -it gitlab cat /etc/gitlab/initial_root_password
```

![img](https://pic.rmb.bdstatic.com/bjh/down/6443b2e53f7dc685fc49db75a9493516.png@s_0,w_2000%7Cwm_2,t_55m+5a625Y+3L+i/kOe7tOi0vOiIuQ==,fc_ffffff,ff_U2ltSGVp,sz_50,x_32,y_32)

请将这串字符记录下，每个人得到的初始密码都是不一样的，根据自己的情况。在浏览器中访问http:ip:8929，将ip替换为你服务器的ip地址。

![img](https://pic.rmb.bdstatic.com/bjh/down/51f319f2a436193a4b7cce9a09a3991a.png@wm_2,t_55m+5a625Y+3L+i/kOe7tOi0vOiIuQ==,fc_ffffff,ff_U2ltSGVp,sz_50,x_32,y_32)

然后点击Sign in，发现已经可以正常登录了。

### 5.登录后配置

### 关闭注册功能

我这里用不到注册功能，所以我把注册功能给关掉了。

![img](https://pic.rmb.bdstatic.com/bjh/down/2e48cc88542e3076890ad51cdcd7b959.png@wm_2,t_55m+5a625Y+3L+i/kOe7tOi0vOiIuQ==,fc_ffffff,ff_U2ltSGVp,sz_50,x_32,y_32)![img](https://pic.rmb.bdstatic.com/bjh/down/1baea5f1661dcb863ac37725a8afd595.png@wm_2,t_55m+5a625Y+3L+i/kOe7tOi0vOiIuQ==,fc_ffffff,ff_U2ltSGVp,sz_50,x_32,y_32)

最后点击save changes保存应用。

![img](https://pic.rmb.bdstatic.com/bjh/down/a506e22ead97c10843ca535d1a689833.png@wm_2,t_55m+5a625Y+3L+i/kOe7tOi0vOiIuQ==,fc_ffffff,ff_U2ltSGVp,sz_50,x_32,y_32)image

### 修改密码

根据图示找到password按钮，进行修改密码操作。

![img](https://pic.rmb.bdstatic.com/bjh/down/2256ad384484903d7a49b7f8217edddb.png@wm_2,t_55m+5a625Y+3L+i/kOe7tOi0vOiIuQ==,fc_ffffff,ff_U2ltSGVp,sz_50,x_32,y_32)

输入旧密码，然后输入两次新密码后，点击Save password。这样就设置好了！

![img](https://pic.rmb.bdstatic.com/bjh/down/8ff11ee472d6e58682c0a59f36819769.png@wm_2,t_55m+5a625Y+3L+i/kOe7tOi0vOiIuQ==,fc_ffffff,ff_U2ltSGVp,sz_50,x_32,y_32)



##### 

启动脚本的版本应该gitlab-ce 的，现在是 image: 'gitlab/gitlab-ee:latest'