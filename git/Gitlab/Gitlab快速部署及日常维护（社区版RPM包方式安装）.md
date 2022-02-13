# [Gitlab快速部署及日常维护（社区版RPM包方式安装）](https://www.cnblogs.com/kevingrace/p/5985918.html)

 

之前梳理了一篇[Gitlab的安装CI持续集成系统环境---部署Gitlab环境完整记录](http://www.cnblogs.com/kevingrace/p/5651402.html)，但是这是bitnami一键安装的，版本比较老。下面介绍使用rpm包安装Gitlab，下载地址：https://mirrors.tuna.tsinghua.edu.cn/gitlab-ce/yum/el6/，针对centos6和centos7的各版本Gitlab下载。如果下载不下来或者下载巨慢，可以尝试：[清华大学镜像](https://mirror.tuna.tsinghua.edu.cn/help/gitlab-ce/)

**一、GitLab简介**
GitLab 是一个用于仓库管理系统的开源项目，使用Git作为代码管理工具，并在此基础上搭建起来的web服务

**二、GitLab系统架构**
git用户的主目录通常是/home/git（~git表示主目录路径），GitLab主要以/home/git用户身份安装在用户主目录中git。在主目录中是gitlabhq服务器软件所在的位置以及存储库（尽管存储库位置是可配置的）。裸存储库位于/home/git/repositories。GitLab是一个ruby on rails应用程序，因此可以通过研究ruby on rails应用程序的工作原理来学习内部工作的细节。为了通过SSH提供存储库，有一个名为gitlab-shell的附加应用程序，它安装在/home/git/gitlab-shell。

**GitLab 应用程序是下面所述的所有组件的集合：**

![img](https://img2018.cnblogs.com/blog/907596/201911/907596-20191118212733899-716856611.png)

**1.** repository：代码库，可以是硬盘或 NFS 文件系统
**2.** Nginx：Web 入口
**3.** 数据库：包含以下信息：
  \- repository 中的数据（元数据，issue，合并请求 merge request 等）
  \- 可以登录 Web 的用户（权限）
**4.** Redis：缓存，负责分发任务
**5.** sidekiq：后台任务，主要负责发送电子邮件。任务需要来自 Redis
**6.** Unicorn：Gitlab 自身的 Web 服务器，包含了 Gitlab 主进程，负责处理快速/一般任务，与 Redis 一起工作。工作内容包括：
  \- 通过检查存储在 Redis 中的用户会话来检查权限
  \- 为 Sidekiq 制作任务
  \- 从仓库（warehouse）取东西或在那里移动东西
**7.** gitlab-shell：用于 SSH 交互，而不是 HTTP。gitlab-shell 通过 Redis 与 Sidekiq 进行通信，并直接或通过 TCP 间接访问 Unicorn
**8.** gitaly：后台服务，专门负责访问磁盘以高效处理 git 操作，并缓存耗时操作。所有的 git 操作都通过 Gitaly 处理
**9.** gitlab-workhorse：反向代理服务器，可以处理与 Rails 无关的请求（磁盘上的CSS、JS 文件等），处理Git Push/Pull 请求，处理到Rails的连接（修改由Rails发送的响应或发送给 Rails 的请求，管理 Rails 的长期 WebSocket 连接等）。
**10.** mail_room：处理邮件请求。回复 GitLab 发出的邮件时，GitLab 会调用此服务

Sidekiq. Unicorn 和 GitLab-shell 是GitLab中处理任务的 3 个程序。

**三、Gitlab安装、配置、启动管理**
安装Gitlab必要的依赖项，还将在系统防火墙中打开HTTP和SSH访问
安装命令：yum install -y curl policycoreutils-python openssh-server
激活命令：systemctl enable sshd
启用命令：systemctl start sshd
防火墙命令：firewall-cmd --permanent--add-service=http && systemctl reload firewalld

安装Postfix以发送通知电子邮件
安装命令：yum install postfix
激活命令：systemctl enable postfix
启用命令：systemctl start postfix

下载GitLab软件包（社区版），地址：https://packages.gitlab.com/gitlab/gitlab-ce

查看Gitlab相关目录，命令：find / -name gitlab

Gitlab目录结构
/opt/gitlab/ 　　   # 主目录
/etc/gitlab/ 　　   # 放置配置文件
/var/opt/gitlab/ 　　# 各个组件
/var/log/gitlab/ 　　# 放置日志文件
/var/opt/gitlab/git-data/repositories 　　 #数据库的地址　　
/var/opt/gitlab/postgresql/data 　　    #gitlab组和项目的地址
/etc/gitlab/gitlab.rb               #gitlab配置文件

初始化Gitlab命令（保存配置或重新载入配置）：gitlab-ctl reconfigure

Gitlab服务的启停管理
启动服务： gitlab-ctl start
停止服务： gitlab-ctl stop
重启服务： gitlab-ctl restart
查看状态： gitlab-ctl status

Gitlab的supervisor方式启动服务
服务启动命令：  systemctl start gitlab-runsvdir.service
服务停止命令：  systemctl stop gitlab-runsvdir.service
服务重启命令：  systemctl restart gitlab-runsvdir.service
服务开机启动命令：  systemctl enable gitlab-runsvdir.service
取消开机启动命令：  systemctl disable gitlab-runsvdir.service
服务查看命令：  systemctl list-unit-files

Gitlab服务日志查看：/usr/bin/gitlab-ctl tail     #可以查看到gitlab所有插件的日志情况

**四、Centos下Gitlab快速安装的操作记录**
**1. Gitlab安装过程（最好找一台环境比较干净的机器）：**

```
1）配置系统防火墙,把HTTP和SSH端口开放（关闭iptables或者开放``ssh``）.``[root@gitlab ~]``# /etc/init.d/iptables stop``[root@gitlab ~]``# yum install curl openssh-server postfix cronie policycoreutils-python``[root@gitlab ~]``# service postfix start``[root@gitlab ~]``# chkconfig postfix on``[root@gitlab ~]``# lokkit -s http -s ssh    //如果iptables关闭了，这条命令就无需执行了。这条命令是用来设置防火墙的，开放http和ssh访问端口` `2）下载gitlab的rpm安装包``已提前下载放到百度云里：``http:``//pan``.baidu.com``/s/1c2EPRLQ``提前密码：qys2``[root@gitlab ~]``# rpm -ivh gitlab-ce-9.4.5-ce.0.el6.x86_64.rpm --force` `安装后的gitlab默认路径是``/opt/gitlab``（程序路径）、``/var/opt/gitlab``（配置文件路径）。` `3) 接着进行配置``[root@gitlab ~]``# gitlab-ctl reconfigure` `上面配置命令执行后，如没有报错，就说明gitlab配置成功。配置后会生成各应用服务配置文件，放在``/opt/gitlab/etc``下，日志路径为``/var/log/gitlab/` `4）然后启动gitlab``[root@gitlab ~]``# gitlab-ctl start``[root@gitlab ~]``# gitlab-ctl status` `5）最后就可以使用http:``//localhost``顺利访问Gitlab了。整个安装过程大概10分钟搞定（rpm包下载比较费时间）
```

**将ip访问修改为域名访问的更改方法：**

```
1）首先将``/etc/gitlab/gitlab``.rb文件中的192.168.1.24全部替换为gitlab.kevin.com``[root@code-server gitlab]``# vim /etc/gitlab/gitlab.rb``external_url``'http://192.168.1.24'``改为：``external_url``'http://gitlab.kevin.com'`` ` `2）其次将下面两文件中的192.168.1.24全部替换为gitlab.kevin.com``/var/opt/gitlab/gitlab-shell/config``.yml``/var/opt/gitlab/gitlab-rails/etc/gitlab``.yml`` ` `下面两文件都是上面两文件的软链接，修改上面两个文件即可``[root@code-server gitlab]``# ll /opt/gitlab/embedded/service/gitlab-rails/config/gitlab.yml``lrwxrwxrwx 1 root root 43 Nov 9 18:00``/opt/gitlab/embedded/service/gitlab-rails/config/gitlab``.yml ->``/var/opt/gitlab/gitlab-rails/etc/gitlab``.yml``[root@code-server gitlab]``# ll /opt/gitlab/embedded/service/gitlab-shell/config.yml``lrwxrwxrwx. 1 root root 39 Jun 11 20:04``/opt/gitlab/embedded/service/gitlab-shell/config``.yml ->``/var/opt/gitlab/gitlab-shell/config``.yml` `3）然后将下面文件中的192.168.1.24全部替换为gitlab.kevin.com``/var/opt/gitlab/nginx/conf/gitlab-http``.conf`` ` `4）最后执行``"gitlab-ctl reconfigure"``命令使之配置生效（注意最好不要执行``"gitlab-ctl restart"``,只执行本命令即可）
```

**2. Gitlba安装后的几个细节的配置**

```
Gitlab如果是编译安装的默认管理员账号密码是：admin@``local``.host｜5iveL!fe，如果是 rpm包安装则管理员账号密码是root｜5iveL!fe
```

Gitlab安装后，http://localhost访问，首次访问的时候，如果不知道管理员账号和密码，尽管可以注册用户，但注册的用户都不是管理员。这个时候，可以重置管理员的密码，管理员默认是root。
重置管理员密码（密码要是8位）的方法如下：

```
[root@gitlab ~]``# gitlab-rails console production``Loading production environment (Rails 4.1.1)``irb(main):001:0> user = User.where(``id``:1).first``irb(main):002:0> user.password=``'12345678'``irb(main):003:0> user.save!` `这样，Gitlab管理员的登录权限就是：root``/12345678``，管理员的默认邮箱是部署机的本机邮箱，也是从本机发的邮件。这也就是为什么在开头要安装postfix。` `修改下面几处，否则邮件发出后，点击会报错。下面的192.168.1.24是部署机ip。` `[root@gitlab ~]``# cd /opt/gitlab/``[root@gitlab gitlab]``# cat embedded/service/gitlab-rails/config/gitlab.yml|grep 192.168.1.24``  ``host: 192.168.1.24``  ``email_from: gitlab@192.168.1.24` `[root@gitlab gitlab]``# cd /var/opt/gitlab/``[root@gitlab gitlab]``# cat ./gitlab-rails/etc/gitlab.yml|grep 192.168.1.24``  ``host: 192.168.1.24``  ``email_from: gitlab@192.168.1.24` `最后重启gitlab-ctl生效``[root@gitlab gitlab]``# gitlab-ctl restart
```

在管理员账号(root)登录后，先把"注册"功能关了,这样就只能在管理员账号下创建用户。**关闭注册功能方法**：
访问**http://192.168.1.24/admin/application_settings**，如下：

关闭"Sign-up enabled"功能（特别注意：Sign-in enabled登录功能不要关闭了，看清楚！）

![img](https://images2017.cnblogs.com/blog/907596/201708/907596-20170816190455646-1589958154.png)

**3. Gitlab批量添加账号**

```
[root@gitlab ~]``# cat gitlab.sh``#!/bin/bash``#批量创建gitlab用户``userinfo=``"userinfo.text"``while` `read` `line``do``  ``password=```echo` `$line |``awk` `'{print $1}'`````  ``mail=```echo` `$line |``awk` `'{print $2}'`````  ``username=```echo` `$line |``awk` `'{print $3}'`````  ``name=```echo` `$line |``awk` `'{print $4}'`````  ``curl -d``"reset_password=$password&email=$mail&username=$username&name=$name&private_token=ucUctguWU6-2qrvRnGiB"` `"http://192.168.1.24/api/v4/users"` `done` `<$userinfo` `[root@gitlab ~]``# cat userinfo.text``1 zhanjiang.feng@wang.com zhanjiang.feng zhanjiang.feng``1 hongkang.yan@wang.com hongkang.yan hongkang.yan``1 yansong.wang@wang.com yansong.wang yansong.wang``1 bo.xue@wang.com bo.xue bo.xue``1 junlong.li@wang.com junlong.li junlong.li``1 luyu.cao@wang.com luyu.cao luyu.cao``1 xueqing.wang@wang.com xueqing.wang xueqing.wang``1 xu.guo@wang.com xu.guo xu.guo``1 bing.xing@wang.com bing.xing bing.xing``1 mengmeng.li@wang.com linan linan
```

注意：上面userinfo.text文件里的四行分别表示密码，邮箱，用户名，别名。上面命令执行后，就可以批量创建用户了!
其中密码用1表示重置密码，也就是用户创建之后，会给用户邮箱发送两封邮件：
**-> 一封确认绑定邮箱的邮件，一定要点击这个邮件里的confirm确认地址（否则登录无效）；**
**-> 另一封是重置用户密码的邮件。重置后就可以使用邮箱或用户名登陆了。**

 注意上面脚本中的private_token（这个很重要，否则批量创建不了用户）的值是从gitlab的管理员账号登录后的"settings-Account"界面里找到的，如下：

![img](https://images2017.cnblogs.com/blog/907596/201708/907596-20170816193555209-1856184235.png)

 访问脚本中gitlab的用户接口地址http://192.168.1.24/api/v4/users，试试能否访问！

​                               **Email的smtp设置**                                 

```
上面默认是用部署机本地的postfix发邮件。如果要想使用第三方邮箱发邮件，这就需要修改``/var/opt/gitlab/gitlab-rails/etc/unicorn``.rb文件：``[root@gitlab ~]``# # cat /etc/gitlab/gitlab.rb|grep -v "^#"|grep -v "^$"``external_url``'http://192.168.1.24'``gitlab_rails[``'gitlab_email_from'``] =``'wangshibohaha@163.com'``gitlab_rails[``'smtp_enable'``] =``true``gitlab_rails[``'smtp_address'``] =``"smtp.163.com"``gitlab_rails[``'smtp_port'``] = 25``gitlab_rails[``'smtp_user_name'``] =``"wangshibohaha@163.com"``gitlab_rails[``'smtp_password'``] =``"*******"``gitlab_rails[``'smtp_domain'``] =``"163.com"``gitlab_rails[``'smtp_authentication'``] =``"login"``gitlab_rails[``'smtp_enable_starttls_auto'``] =``true``user[``'git_user_email'``] =``"wangshibohaha@163.com"` `由于该文件会影响gitlab-ctl指令，如果改动了则需要重新运行配置。``注意这个重新配置的动作要在上面细节配置之前，否则上面的配置在reconfigure之后就会被覆盖到默认状态！``[root@gitlab ~]``# gitlab-ctl reconfigure` `--------------------------------------------------------------------------------------------``上面使用的是163邮箱，下面再贴下公司企业邮箱（用的是Coremail论客邮件系统，注意邮箱的smtp地址要正确）的配置：``[root@gitlab ~]``# cat /etc/gitlab/gitlab.rb|grep -v "^#"|grep -v "^$"``external_url``'http://192.168.1.24'``gitlab_rails[``'gitlab_email_from'``] =``'notice@vdholdhaha.com'``gitlab_rails[``'smtp_enable'``] =``true``gitlab_rails[``'smtp_address'``] =``"smtp.icoremail.net"``gitlab_rails[``'smtp_port'``] = 25``gitlab_rails[``'smtp_user_name'``] =``"notice@vdholdhaha.com"``gitlab_rails[``'smtp_password'``] =``"notice@123"``gitlab_rails[``'smtp_domain'``] =``"icoremail.net"``gitlab_rails[``'smtp_authentication'``] =``"login"``gitlab_rails[``'smtp_enable_starttls_auto'``] =``true``user[``'git_user_email'``] =``"notice@vdholdhaha.com"
```

​                         **修改Gitlab登录界面**                             

![img](https://images2018.cnblogs.com/blog/907596/201805/907596-20180531230032827-163876309.png)

选择gitlab新的主题风格，新主题会在左边栏展示选择项

![img](https://images2018.cnblogs.com/blog/907596/201805/907596-20180531230229601-1982074527.png)

![img](https://images2018.cnblogs.com/blog/907596/201805/907596-20180531230306429-1391460713.png)

![img](https://images2018.cnblogs.com/blog/907596/201805/907596-20180531230341973-1468448316.png)

![img](https://images2018.cnblogs.com/blog/907596/201805/907596-20180531230553919-1459317624.png)

经过上面修改后，看下新的登录界面

![img](https://images2018.cnblogs.com/blog/907596/201805/907596-20180531230658273-331117757.png)

​                                    **Gitlab整合Ldap（或AD域）**                                   

```
如上已经顺利部署了Gitlab环境，又在一台空闲的Windows server 2008上安装了AD域。``现在需要在Gitlab上整合AD域，实现Gitlab只能使用AD域里面的账号登录。配置记录如下：` `AD域的信息：``主机地址：192.168.10.141``端口：389` `配置如下：``[root@gitlab ~]``# vim /etc/gitlab/gitlab.rb``......``gitlab_rails[``'ldap_enabled'``] =``true``gitlab_rails[``'ldap_servers'``] = YAML.load <<-EOS``# remember to close this block with 'EOS' below``main:``# 'main' is the GitLab 'provider ID' of this LDAP server`` ``label:``'哈哈集团-Gitlab登录入口'`` ``host:``'192.168.10.141'`` ``port: 389`` ``uid:``'userPrincipalName'`` ``method:``'plain'` `# "tls" or "ssl" or "plain"`` ``allow_username_or_email_login:``false`` ``bind_dn:``'cn=王一,ou=技术运维部,dc=kevin,dc=com'`` ``password:``'9oGlYkgDzhp5k6JZ'`` ``active_directory:``true`` ``base:``'ou=技术运维部,dc=kevin,dc=com'`` ``user_filter:``''``EOS` `接着执行下面命令，使上面配置生效：``[root@gitlab ~]``# gitlab-ctl reconfigure    //这里最好使用该命令，表示重载配置。不要使用"gitlab-ctl restart"重启服务，否则可能出现500报错！` `然后执行下面命令，检查LDAP信息是否成功同步过来``[root@gitlab ~]``# gitlab-rake gitlab:ldap:check``Checking LDAP ...` `Server: ldapmain``LDAP authentication... Success``LDAP``users` `with access to your GitLab server (only showing the first 100 results)`` ``DN: CN=李某某,OU=技术运维部,DC=kevin,DC=com userPrincipalName: limoumou@kevin.com`` ``DN: CN=李二,OU=技术运维部,DC=kevin,DC=com  userPrincipalName: lier@kevin.com`` ``DN: CN=lier1,OU=技术运维部,DC=kevin,DC=com  userPrincipalName: lier1@kevin.com`` ``DN: CN=``test``,OU=技术运维部,DC=kevin,DC=com  userPrincipalName:``test``@kevin.com`` ``DN: CN=王一,OU=技术运维部,DC=kevin,DC=com userPrincipalName: wangyi@kevin.com`` ``DN: CN=张三,OU=技术运维部,DC=kevin,DC=com  userPrincipalName: zhangsan@kevin.com`` ``DN: CN=张三,OU=网络,OU=技术运维部,DC=kevin,DC=com  userPrincipalName: zhangsan02@kevin.com`` ``DN: CN=赵四,OU=网络,OU=技术运维部,DC=kevin,DC=com  userPrincipalName: zhaosi@kevin.com` `Checking LDAP ... Finished` `=========================================================================================``注意：``如上配置中，随便使用AD域中的一个有读权限的账号和其密码进行配置就行了，即将其他账号读出来！``AD域或Openldap搭建的时候，域名最好用邮箱域名。``uid表示属性` `uid:``'uid'`            `//``默认配置是这个，如果不改，上面check ldap就不会成功，即不能成功同步ldap账号信息。``uid:``'cn'`            `//``这个表示可以使用cn名称登录，比如王一，如果cn名称是英文名（比如``test``），则还可以使用带域名形式登录（比如``test``@kevin.com）``uid:``'Samaccountname'`      `//``这个表示可以使用wangyi或wangyi@kevin.com登录` `如果uid配置成上面的cn和Samaccountname，那么下面的``allow_username_or_email_login:``true` `label:``'哈哈集团-Gitlab登录入口'`   `该配置表示使用LDAP账号登录时显示的界面提示信息。
```

![img](https://images2018.cnblogs.com/blog/907596/201804/907596-20180419171615350-467686120.png)

**![img](https://images2018.cnblogs.com/blog/907596/201804/907596-20180419172652061-853507941.png)**

**取消Gitlab默认的登录窗口，访问http://192.168.1.24/admin/application_settings** **（注意不要勾选下面的"Sign-in enabled"选择）**

**![img](https://images2018.cnblogs.com/blog/907596/201804/907596-20180419171827960-1568078386.png)**

​                **Gitlab访问出现403"Forbidden"现象**                
出现的可能原因：**较多的并发导致的访问被拒绝， Gitlab使用rack_attack做了并发访问的限制！****
**

解决办法：
打开/etc/gitlab/gitlab.rb文件，查找 gitlab_rails['rack_attack_git_basic_auth'] 关键词,取消注释,
修改ip_whitelist白名单属性，加入Gitlab部署的IP地址。

修改如下（192.168.1.24）：

```
[root@gitlab ~]``# vim /etc/gitlab/gitlab.rb``......`` ``gitlab_rails[``'rack_attack_git_basic_auth'``] = {``  ``'enabled'` `=>``true``,``  ``'ip_whitelist'` `=> [``"127.0.0.1"``,``"192.168.1.24"``],``  ``'maxretry'` `=> 10,``  ``'findtime'` `=> 60,``  ``'bantime'` `=> 3600`` ``}
```

然后重载配置

```
[root@gitlab ~]``# gitlab-ctl reconfigure
```

最后再在浏览器里访问gitlab就OK了！

​                         **Gitlab访问出现502的现象**                               
**Gitlab访问出现：Whoops, GitLab is taking too much time to respond.**

```
产生原因：``1）unicorn原8080默认端口被容器中别的进程已经占用，必须调整为没用过的``2）gitlab的timeout设置过小，默认为60` `解决办法：``1）关闭gitlab服务``# gitlab-ctl stop``2）选择一个没有被系统占用的端口作为unicorn端口，比如8877端口（``lsof` `-i:8877 确认此端口没有被占用）``# vim /etc/gitlab/gitlab.rb``unicorn[``'port'``] = 8877``gitlab_workhorse[``'auth_backend'``] =``"http://localhost:8877"``3）重新生成配置``# gitlab-ctl reconfigure``4）重启gitlab服务``# gitlab-ctl restart
```

​                         **Gitlab启动失败，或重新安装时出现卡的状态**                                 

```
在卸载gitlab然后再次安装执行``sudo` `gitlab-ctl reconfigure的时候往往会出现：ruby_block[supervise_redis_sleep] action run，会一直卡无法往下进行！``这时候的解决办法：``1）按ctrl + c 强制结束``2）执行``"systemctl restart gitlab-runsvdir"` `命令``3）接着再执行``"gitlab-ctl reconfigure"` `如果机器重启后，启动``"gitlab-ctl start"``失败，解决办法：``# systemctl restart gitlab-runsvdir``# gitlab-ctl reconfigure``# gitlab-ctl start
```

​                **Gitlab异常关机，导致gitlab启动失败！gitlab-runsvdir方式启动没反应(僵尸状态)**              
Gitlab部署的服务器异常断电，机器重启后，尝试启动gitlab服务，启动失败！通过gitlab-runsvdir方式启动一直没有反应！一直在卡顿状态！日志也没有任务输入！

```
执行下面的启动命令报错：``[root@gitlab ~]``# gitlab-ctl start    或者 "gitlab-ctl restart"``fail: alertmanager: runsv not running``fail: gitaly: runsv not running``fail: gitlab-monitor: runsv not running``fail: gitlab-workhorse: runsv not running``fail: logrotate: runsv not running``fail: nginx: runsv not running``fail: node-exporter: runsv not running``fail: postgres-exporter: runsv not running``fail: postgresql: runsv not running``fail: prometheus: runsv not running``fail: redis: runsv not running``fail: redis-exporter: runsv not running``fail: registry: runsv not running``fail: sidekiq: runsv not running``fail: unicorn: runsv not running` `报错说``"runsv not running"``那么尝试通过supervisor进程方式启动gitlab，发现一直在卡顿中，根本没有任何反应！``[root@gitlab ~]``# systemctl restart gitlab-runsvdir` `查看日志，发现也没有任务启动信息打印到日志中 (日志都是之前的)``[root@gitlab ~]``# /usr/bin/gitlab-ctl tail` `gitlab-runsvdir启动在卡顿中，gitlab服务也没有起来``[root@gitlab ~]``# ps -ef|grep gitlab` `最后解决方法：``通过Gitlab自己原生命令去启动服务：``/opt/gitlab/embedded/bin/runsvdir-start``[root@gitlab ~]``# cat /etc/systemd/system/multi-user.target.wants/gitlab-runsvdir.service``[Unit]``Description=GitLab Runit supervision process``After=multi-user.target` `[Service]``ExecStart=``/opt/gitlab/embedded/bin/runsvdir-start`      `#最后通过这条命令启动了Gitlab``Restart=always` `[Install]``WantedBy=multi-user.target` `执行下面的启动，虽然发现这个也会一直在卡顿中，但是不影响gitlab服务启动。``[root@gitlab ~]``# /opt/gitlab/embedded/bin/runsvdir-start` `重新打开一个终端窗口，发现gitlab已经有新的日志信息打入了，gitlab也服务已经起来了``[root@gitlab ~]``# /usr/bin/gitlab-ctl tail``[root@gitlab ~]``# ps -ef|grep gitlab` `这时候关闭上面执行``"/opt/gitlab/embedded/bin/runsvdir-start"``的卡顿的终端窗口，发现gitlab也还是启动状态(``ps` `-ef|``grep` `gitlab)``[root@gitlab ~]``# ps -ef|grep gitlab``[root@gitlab ~]``# lsof -i:80``[root@gitlab ~]``# gitlab-ctl status``run: alertmanager: (pid 29804) 1640s; run: log: (pid 29789) 1640s``run: gitaly: (pid 29795) 1640s; run: log: (pid 29781) 1640s``run: gitlab-monitor: (pid 29799) 1640s; run: log: (pid 29785) 1640s``run: gitlab-workhorse: (pid 29794) 1640s; run: log: (pid 29780) 1640s``run: logrotate: (pid 29798) 1640s; run: log: (pid 29783) 1640s``run: nginx: (pid 29800) 1640s; run: log: (pid 29786) 1640s``run: node-exporter: (pid 29802) 1640s; run: log: (pid 29788) 1640s``run: postgres-exporter: (pid 29805) 1640s; run: log: (pid 29790) 1640s``run: postgresql: (pid 29796) 1640s; run: log: (pid 29782) 1640s``run: prometheus: (pid 29797) 1640s; run: log: (pid 29784) 1640s``run: redis: (pid 29818) 1640s; run: log: (pid 29793) 1640s``run: redis-exporter: (pid 29817) 1640s; run: log: (pid 29792) 1640s``run: sidekiq: (pid 29801) 1640s; run: log: (pid 29787) 1640s``run: unicorn: (pid 29807) 1640s; run: log: (pid 29791) 1640s` `查看日志也有新信息写入，一切正常了！``[root@gitlab ~]``# /usr/bin/gitlab-ctl tail
```

​                ***\*Gitlab忘记root用户密码，重置用户密码和查看用户ID号方法\****              

```
一、Gitlab查看用户``id``号的方法``1）方法1：通过api接口查询``接口查询地址：http:``//gitlab``的url``/api/v4/users``?username=用户名` `比如查看gitlab的root用户``id``在浏览器页面里直接访问``"http://172.16.60.237/api/v4/users?username=root"``或者``在linux终端命令行里直接通过curl命令进行访问``[root@localhost ~]``# curl http://172.16.60.237/api/v4/users?username=root``[{``"id"``:1,``"name"``:``"Administrator"``,``"username"``:``"root"``,``"state"``:``"active"``,``"avatar_url"``:``"https://www.gravatar.com/avatar/e64c7d89f26bd1972efa854d13d7dd61?s=80\u0026d=identicon"``,``"web_url"``:``"http://gitlab.example.com/root"``}]` `2）方法2：进入gitlab数据库查询``[root@localhost ~]``# gitlab-rails dbconsole``psql (10.9)``Type``"help"` `for` `help.` `gitlabhq_production=> \l``                       ``List of databases``    ``Name     |  Owner  | Encoding |  Collate  |  Ctype  |    Access privileges``---------------------+-------------+----------+-------------+-------------+---------------------------------`` ``gitlabhq_production | gitlab   | UTF8   | en_US.UTF-8 | en_US.UTF-8 |`` ``postgres      | gitlab-psql | UTF8   | en_US.UTF-8 | en_US.UTF-8 |`` ``template0      | gitlab-psql | UTF8   | en_US.UTF-8 | en_US.UTF-8 | =c/``"gitlab-psql"`        `+``           ``|       |     |       |       |``"gitlab-psql"``=CTc/``"gitlab-psql"`` ``template1      | gitlab-psql | UTF8   | en_US.UTF-8 | en_US.UTF-8 | =c/``"gitlab-psql"`        `+``           ``|       |     |       |       |``"gitlab-psql"``=CTc/``"gitlab-psql"``(4 rows)` `## 连接数据库``gitlabhq_production=> \c gitlabhq_production``You are now connected to database``"gitlabhq_production"` `as user``"gitlab"``.``gitlabhq_production=>``select` `id``,name,username from``users``;`` ``id` `|   name   | username``----+---------------+----------`` ``1 | Administrator | root``(1 row)``## 查找账户id``gitlabhq_production=>``select` `id` `from``users` `where username =``'root'``;`` ``id``----`` ``1``(1 row)` `==============================================================================================``二、忘记Gitlab的root用户密码的重置方法``如果忘记了Gitlab的root用户密码，则可以在服务器上面直接修改数据：``# gitlab-rails console production   #然后以此执行下面命令（需要提前查询用户的id号）``...> user = User.where(``id``: 1).first``...> user.password =``'secret_pass'``...> user.password_confirmation =``'secret_pass'``...> user.save!` `例如重置root用户密码为root@123，root用户``id``为1``[root@localhost ~]``# gitlab-rails console production``DEPRECATION WARNING: Passing the environment's name as a regular argument is deprecated and will be removed``in` `the next Rails version. Please, use the -eoption instead. (called from require at bin``/rails``:4)``--------------------------------------------------------------------------------`` ``GitLab:    12.2.0 (1c1d47c5974)`` ``GitLab Shell: 9.3.0`` ``PostgreSQL:  10.9``--------------------------------------------------------------------------------``Loading production environment (Rails 5.2.3)``irb(main):001:0> user = User.where(``id``: 1).first``=>``#``irb(main):002:0> user.password =``'root@123'``=>``"root@123"``irb(main):003:0> user.password_confirmation =``'root@123'``=>``"root@123"``irb(main):004:0> user.save!``Enqueued ActionMailer::DeliveryJob (Job ID: e562694d-2a1b-4bad-843b-d8567ac51077) to Sidekiq(mailers) with arguments:``"DeviseMailer"``,``"password_change"``,``"deliver_now"``,``#>``=>``true``irb(main):005:0> quit``[root@localhost ~]``#
```

![img](https://img2020.cnblogs.com/blog/907596/202004/907596-20200421095533820-1296438432.png)

**五、Gitlab日常维护：备份、迁移、升级**
**1. Gitlab备份**
使用Gitlab一键安装包安装Gitlab非常简单, 同样的备份恢复与迁移也非常简单. 使用一条命令即可创建完整的Gitlab备份

```
# gitlab-rake gitlab:backup:create` `比如使用以上命令会在``/var/opt/gitlab/backups``目录下创建一个名称类似为1481598919_gitlab_backup.``tar``的压缩包, 这个压缩包就是Gitlab整个的完整部分,``其中开头的1481598919是备份创建的日期。` `/etc/gitlab/gitlab``.rb 配置文件须备份``/var/opt/gitlab/nginx/conf` `nginx配置文件``/etc/postfix/main``.cfpostfix 邮件配置备份
```

1）1.1Gitlab备份目录
可以通过/etc/gitlab/gitlab.rb配置文件来修改默认存放备份文件的目录

```
gitlab_rails[``'backup_path'``] =``"/var/opt/gitlab/backups"``/var/opt/gitlab/backups``修改为你想存放备份的目录即可, 修改完成之后使用gitlab-ctl reconfigure命令重载配置文件即可.
```

2）Gitlab自动备份
实现每天凌晨2点进行一次自动备份:通过crontab使用备份命令实现

```
0 2 * * *``/opt/gitlab/bin/gitlab-rake` `gitlab:backup:create
```

**2. Gitlab恢复**
Gitlab的从备份恢复也非常简单:

```
1）停止相关数据连接服务``# gitlab-ctl stop unicorn``# gitlab-ctl stop sidekiq` `2）从1481598919编号备份中恢复``# gitlab-rake gitlab:backup:restore BACKUP=1481598919` `3）启动Gitlab``# gitlab-ctl start
```

**3. Gitlab迁移**
**要求：新服务器的gitlab版本与旧的服务器相同。**

迁移如同备份与恢复的步骤一样, 只需要将老服务器/var/opt/gitlab/backups目录下的备份文件拷贝到新服务器上的/var/opt/gitlab/backups即可(如果你没修改过默认备份目录的话).

但是需要注意的是：
新服务器上的Gitlab的版本必须与创建备份时的Gitlab版本号相同. 比如新服务器安装的是最新的7.60版本的Gitlab, 那么迁移之前, 最好将老服务器的Gitlab 升级为7.60在进行备份.

/etc/gitlab/gitlab.rb         这个gitlab配置文件须迁移,迁移后需要调整数据存放目录
/var/opt/gitlab/nginx/conf    这个nginx配置文件目录须迁移

/etc/gitlab/gitlab-secrets.json    #复制新服务器相同的目录下
/etc/ssh/*key*                #复制到新服务器相同目录下，解决ssh key认证不成功问题

```
# gitlab-ctl stop unicorn``# gitlab-ctl stop sidekiq``# chmod 777 /var/opt/gitlab/backups/1481598919_gitlab_backup.tar # 或 chown git:git /var/opt/gitlab/backups/1481598919_gitlab_backup.tar``# gitlab-rake gitlab:backup:restore BACKUP=1481598919
```

**4. Gitlab升级**

```
1.关闭gitlab服务``# gitlab-ctl stop unicorn``# gitlab-ctl stop sidekiq``# gitlab-ctl stop nginx` `2.备份gitlab``# gitlab-rake gitlab:backup:create` `3.下载gitlab的RPM包并进行升级``# curl -s https://packages.gitlab.com/install/repositories/gitlab/gitlab-ce/script.rpm.sh | sudo bash``# yum update gitlab-ce` `或者直接安装高版本``#yum install gitlab-ce-12.1.12-ce.0.el7.x86_64` `或者上官网下载最新版本 gitlab对应软件包                  ``gitlab官网地址： https:``//packages``.gitlab.com``/gitlab/gitlab-ce/packages/el/7/gitlab-ce-12``.1.12-ce.0.el7.x86_64.rpm``使用：``# rpm -Uvh gitlab-ce-12.1.12-ce.0.el7.x86_64` `如果报错.``Error executing action `run` on resource``'ruby_block[directory resource: /var/opt/gitlab/git-data/repositories]'` `解决方法:``sudo` `chmod` `2770``/var/opt/gitlab/git-data/repositories` `4.启动并查看gitlab版本信息``# gitlab-ctl reconfigure``# gitlab-ctl restart``# head -1 /opt/gitlab/version-manifest.txt
```

**5. Gitlab重新安装，在执行"gitlab-ctl reconfigure"配置环节出现了下面报错：**
[root@gitlab ~]# gitlab-ctl reconfigure
.........
.........
STDERR: sysctl: cannot open "/etc/sysctl.d/90-omnibus-gitlab-kernel.sem.conf": No such file or directory
sysctl: cannot open "/etc/sysctl.d/90-omnibus-gitlab-net.core.somaxconn.conf": No such file or directory
---- End output of sysctl -e --system ----
Ran sysctl -e --system returned 255

**造成原因：**
丢失了报错中的这两个配置文件，进入/etc/sysctl.d目录发现，这两个文件都是通过链接到/opt/gitlab/embedded/etc/目录下。
然而/opt/gitlab/embedded/etc/确实没有这两个文件。

```
[root@gitlab ~]``# ll /etc/sysctl.d/``total 0``lrwxrwxrwx 1 root root 58 Nov 10 22:23 90-omnibus-gitlab-kernel.sem.conf ->``/opt/gitlab/embedded/etc/90-omnibus-gitlab-kernel``.sem.conf``lrwxrwxrwx 1 root root 61 Nov 10 22:23 90-omnibus-gitlab-kernel.shmall.conf ->``/opt/gitlab/embedded/etc/90-omnibus-gitlab-kernel``.shmall.conf``lrwxrwxrwx 1 root root 61 Nov 10 22:23 90-omnibus-gitlab-kernel.shmmax.conf ->``/opt/gitlab/embedded/etc/90-omnibus-gitlab-kernel``.shmmax.conf``lrwxrwxrwx 1 root root 66 Nov 10 22:25 90-omnibus-gitlab-net.core.somaxconn.conf ->``/opt/gitlab/embedded/etc/90-omnibus-gitlab-net``.core.somaxconn.conf``lrwxrwxrwx. 1 root root 14 Oct 30 09:13 99-sysctl.conf -> ..``/sysctl``.conf` `[root@gitlab ~]``# ll /opt/gitlab/embedded/etc``total 12``-rw-r--r-- 1 root root 24 Apr 12 23:18 90-omnibus-gitlab-kernel.shmall.conf``-rw-r--r-- 1 root root 28 Apr 12 23:17 90-omnibus-gitlab-kernel.shmmax.conf``-rwxr-xr-x 1 root root 196 Apr 12 23:16 gitconfig` `[root@gitlab ~]``# ll /opt/gitlab/embedded/etc/90-omnibus-gitlab-kernel.sem.conf``ls``: cannot access``/opt/gitlab/embedded/etc/90-omnibus-gitlab-kernel``.sem.conf: No such``file` `or directory``[root@gitlab ~]``# ll /opt/gitlab/embedded/etc/90-omnibus-gitlab-net.core.somaxconn.conf``ls``: cannot access``/opt/gitlab/embedded/etc/90-omnibus-gitlab-net``.core.somaxconn.conf: No such``file` `or directory` `解决方法一：``从别的备份机（或者在别的机器上重新安装一次，``"gitlab-ctl reconfigure"``之后生成这两个文件）将这两个文件拷贝回来！` `解决方法二：``[root@gitlab ~]``# vim /etc/gitlab/gitlab.rb``# unicorn['port'] = 8080``修改为：``unicorn[``'port'``] = 8090` `之后重新加载配置文件``[root@gitlab ~]``# gitlab-ctl reconfigure` `再次会报错，然后再修改``/etc/gitlab/gitlab``.rb，修改为原来的配置``[root@gitlab ~]``# vim /etc/gitlab/gitlab.rb``# unicorn['port'] = 8080` `再次重新加载配置文件就OK了！``[root@gitlab ~]``# gitlab-ctl reconfigure` `再次查看，发现上面配置中报错的两个文件已经存在了``[root@gitlab ~]``# ll /opt/gitlab/embedded/etc/``total 20``-rw-r--r-- 1 root root 30 Apr 12 23:33 90-omnibus-gitlab-kernel.sem.conf``-rw-r--r-- 1 root root 24 Apr 12 23:18 90-omnibus-gitlab-kernel.shmall.conf``-rw-r--r-- 1 root root 28 Apr 12 23:17 90-omnibus-gitlab-kernel.shmmax.conf``-rw-r--r-- 1 root root 26 Apr 12 23:35 90-omnibus-gitlab-net.core.somaxconn.conf``-rwxr-xr-x 1 root root 196 Apr 12 23:16 gitconfig``[root@gitlab ~]``# ll /opt/gitlab/embedded/etc/90-omnibus-gitlab-kernel.sem.conf``-rw-r--r-- 1 root root 30 Apr 12 23:33``/opt/gitlab/embedded/etc/90-omnibus-gitlab-kernel``.sem.conf``[root@gitlab ~]``# ll /opt/gitlab/embedded/etc/90-omnibus-gitlab-net.core.somaxconn.conf``-rw-r--r-- 1 root root 26 Apr 12 23:35``/opt/gitlab/embedded/etc/90-omnibus-gitlab-net``.core.somaxconn.conf` `最后再启动gitlab``[root@gitlab ~]``# gitlab-ctl start
```

**6. Gitlab更改默认Nginx**
更换gitlab自带Nginx，使用自行编译Nginx来管理gitlab服务。

```
自行编译的nginx服务和gitlab在同一台机器上``1）编辑gitlab配置文件禁用自带Nignx服务器``[root@gitlab ~]``# vim /etc/gitlab/gitlab.rb``...``#设置nginx为false,关闭自带Nginx``nginx[``'enable'``] =``false``...` `2）检查默认nginx配置文件，并迁移至新Nginx服务 （即将下面两个gitlab自带nginx的配置文件迁移到自行编译的新的nginx配置中）``/var/opt/gitlab/nginx/conf/nginx``.conf        ``#nginx配置文件,包含gitlab-http.conf文件``/var/opt/gitlab/nginx/conf/gitlab-http``.conf     ``#gitlab核心nginx配置文件` `[root@gitlab ~]``# cp /var/opt/gitlab/nginx/conf/nginx.conf /etc/nginx/conf.d/``[root@gitlab ~]``# cp /var/opt/gitlab/nginx/conf/gitlab-http.conf /etc/nginx/conf.d/` `3）重启gitlab服务``[root@gitlab ~]``# gitlab-ctl reconfigure  ``[root@gitlab ~]``# gitlab-ctl restart` `重启自行编译的nginx服务``[root@gitlab ~]``# service nginx restart` `如果访问报502。原因是nginx用户无法访问gitlab用户的socket文件。``重启gitlab需要重新授权``[root@gitlab ~]``# chmod -R o+x /var/opt/gitlab/gitlab-rails
```

*************** 当你发现自己的才华撑不起野心时，就请安静下来学习吧！***************