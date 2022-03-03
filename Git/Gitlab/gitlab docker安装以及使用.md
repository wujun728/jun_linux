[docker下gitlab安装配置使用(完整版)](https://www.cnblogs.com/chinasoft/articles/12969904.html)

docker 安装gitlab以及使用

## 一、安装及配置

### 1.gitlab镜像拉取



```ruby
# gitlab-ce为稳定版本，后面不填写版本则默认pull最新latest版本
$ docker pull gitlab/gitlab-ce
```

 

![img](https://upload-images.jianshu.io/upload_images/15087669-c866f117b53fadf8.png)

拉取镜像

### 2.运行gitlab镜像



```csharp
$ docker run -d  -p 443:443 -p 80:80 -p 222:22 --name gitlab --restart always -v /home/gitlab/config:/etc/gitlab -v /home/gitlab/logs:/var/log/gitlab -v /home/gitlab/data:/var/opt/gitlab gitlab/gitlab-ce
# -d：后台运行
# -p：将容器内部端口向外映射
# --name：命名容器名称
# -v：将容器内数据文件夹或者日志、配置等文件夹挂载到宿主机指定目录
```

运行成功后出现一串字符串



 

![img](https://upload-images.jianshu.io/upload_images/15087669-5818ed22c0bc1ee7.png)

运行成功

### 3.配置

按上面的方式，gitlab容器运行没问题，但在gitlab上创建项目的时候，生成项目的URL访问地址是按容器的hostname来生成的，也就是容器的id。作为gitlab服务器，我们需要一个固定的URL访问地址，于是需要配置gitlab.rb（宿主机路径：/home/gitlab/config/gitlab.rb）。



```ruby
# gitlab.rb文件内容默认全是注释
$ vim /home/gitlab/config/gitlab.rb
```



```ruby
# 配置http协议所使用的访问地址,不加端口号默认为80
external_url 'http://192.168.199.231'

# 配置ssh协议所使用的访问地址和端口
gitlab_rails['gitlab_ssh_host'] = '192.168.199.231'
gitlab_rails['gitlab_shell_ssh_port'] = 222 # 此端口是run时22端口映射的222端口
:wq #保存配置文件并退出
```

 

![img](https://upload-images.jianshu.io/upload_images/15087669-a480f0de6409620a.png)

修改gitlab.rb文件



```ruby
# 重启gitlab容器
$ docker restart gitlab
```

此时项目的仓库地址就变了。如果ssh端口地址不是默认的22，就会加上ssh:// 协议头
打开浏览器输入ip地址(因为我的gitlab端口为80，所以浏览器url不用输入端口号，如果端口号不是80，则打开为：ip:端口号)

### 4.创建一个项目

第一次进入要输入新的root用户密码，设置好之后确定就行

 

![img](https://upload-images.jianshu.io/upload_images/15087669-6b04cfddeccf17bf.png)

gitlab页面

下面我们就可以新建一个项目了，点击Create a project

 

![img](https://upload-images.jianshu.io/upload_images/15087669-2a40551dc13c2826.png)

Create a project

创建完成后：



 

![img](https://upload-images.jianshu.io/upload_images/15087669-0dd085723ef61677.png)

创建完成！

## 二、用户使用

### 1.下载git.exe

双击git.exe安装git（一直点下一步，直到完成）
点击电脑桌面空白地方右键看到如下两行即安装成功

 

![img](https://upload-images.jianshu.io/upload_images/15087669-7bbdee06b7ca7711.png)

image.png

### 2.登录gitlab网页

> **url**：http://192.168.1.111
> 填写账号密码登录

 

![img](https://upload-images.jianshu.io/upload_images/15087669-249a984d541801a1.png)

登录页面

### 3.设置ssh

1.打开本地git bash,使用如下命令生成ssh公钥和私钥对



```ruby
$ ssh-keygen -t rsa -C 'xxx@xxx.com'
```

然后一路回车(-C 参数是你的邮箱地址)

 

![img](https://upload-images.jianshu.io/upload_images/15087669-40be69316850b690.png)

生成密匙

2.然后输入命令：



```ruby
# ~表示用户目录，比如我的windows就是C:\Users\Administrator，并复制其中的内容
$ cat ~/.ssh/id_rsa.pub
```

 

![img](https://upload-images.jianshu.io/upload_images/15087669-b71993bc58477957.png)

公匙

3.打开gitlab,找到Profile Settings-->SSH Keys--->Add SSH Key,并把上一步中复制的内容粘贴到Key所对应的文本框

 

![img](https://upload-images.jianshu.io/upload_images/15087669-d14c5051911fe20c.png)

 

 

![img](https://upload-images.jianshu.io/upload_images/15087669-f7319dc3a9d83828.png)

添加公匙到gitlab

## 4.从gitlab克隆代码

1.回到gitlab页面点击projects->your projects

 

![img](https://upload-images.jianshu.io/upload_images/15087669-0105a84b02d1ed9e.png)

 

2.选择一个需要克隆的项目，进入

 

![img](https://upload-images.jianshu.io/upload_images/15087669-7a7f3af7efcff81c.png)

我的项目页面

3.点击按钮复制地址

 

![img](https://upload-images.jianshu.io/upload_images/15087669-27e842b185a62e69.png)

复制ssh地址

4.新建一个文件夹，我在这里在我的电脑D盘下新建project文件夹

 

![img](https://upload-images.jianshu.io/upload_images/15087669-6c9571d4d0a5d321.png)

 

5.进入projects文件夹右键选择->Git Bash Here

 

![img](https://upload-images.jianshu.io/upload_images/15087669-e59886b042c02edf.png)

点击Git Bash Here

6.设置用户名和邮箱



```csharp
$ git config --global user.name "你的名字"
$ git config --global user.email "你的邮箱"
```

 

![img](https://upload-images.jianshu.io/upload_images/15087669-9592daf5642e3c11.png)

设置名字和邮箱

7.克隆项目



```bash
$ git clone 项目地址
```

 

![img](https://upload-images.jianshu.io/upload_images/15087669-dc8bafb214fa578e.png)

克隆项目

8.查看projects文件夹，项目已经克隆下来了

 

![img](https://upload-images.jianshu.io/upload_images/15087669-94ec492febe71420.png)

项目目录

### 5.提交代码到gitlab

1.基于以上步骤，在克隆的项目文件夹下新增一个测试文件

 

![img](https://upload-images.jianshu.io/upload_images/15087669-c230295d84a79064.png)

新增txt文件

2.查看同步状态
在项目文件夹下右键点击->Git Bash Here

 

![img](https://upload-images.jianshu.io/upload_images/15087669-1fd767543b22d445.png)

 

输入



```ruby
$ git status
```

 

![img](https://upload-images.jianshu.io/upload_images/15087669-364b83d323ceb46b.png)

状态

可以看到红色部分有需要提交的文件
3.提交代码
输入



```csharp
$ git add  测试提交的文件.txt
```

(“git add“后加“.”则添加全部文件，也可以加"*.txt"表示添加全部需要提交的txt文件 )

 

![img](https://upload-images.jianshu.io/upload_images/15087669-2e3e95ecf96cc668.png)

add需要提交的文件

然后输入以下命令提交并添加提交信息



```ruby
$ git commit -m "message"
```

 

![img](https://upload-images.jianshu.io/upload_images/15087669-6d689c385f30fe33.png)

commit

最后输出以下命令提交到gitlab



```ruby
$ git push origin master
```

 

![img](https://upload-images.jianshu.io/upload_images/15087669-889169ad267f2997.png)

push



提交完成啦
再回到gitlab上看该项目就可以看到多了一个txt测试文件



作者：王诗林
链接：https://www.jianshu.com/p/080a962c35b6