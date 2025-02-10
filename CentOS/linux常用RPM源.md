# [linux常用RPM源](https://www.cnblogs.com/wdrain/articles/11528354.html)

切换基本源为阿里云源

备份
mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.backup
下载新的CentOS-Base.repo 到/etc/yum.repos.d/
CentOS 5

wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-5.repo
CentOS 6

wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-6.repo
CentOS 7

wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo


安装第三方源
安装EPEL仓库
yum install -y epel-release
如果以上命令不起作用：

yum install epel-release
rpm -Uvh https://mirror.webtatic.com/yum/el7/webtatic-release.rpm
yum update
yum list | grep php7

 

CentOS/RHEL 7

rpm -Uvh http://dl.fedoraproject.org/pub/epel/7/x86_64/e/epel-release-7-5.noarch.rpm
CentOS/RHEL 6

rpm -Uvh http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm
CentOS/RHEL 5

rpm -Uvh http://dl.fedoraproject.org/pub/epel/5/x86_64/epel-release-5-4.noarch.rpm
安装IUS仓库
RHEL
RHEL 5

rpm -Uvh https://rhel5.iuscommunity.org/ius-release.rpm
RHEL 6

rpm -Uvh https://rhel6.iuscommunity.org/ius-release.rpm
RHEL 7

rpm -Uvh https://rhel7.iuscommunity.org/ius-release.rpm

CentOS
CentOS 5

rpm -Uvh https://centos5.iuscommunity.org/ius-release.rpm
CentOS 6

rpm -Uvh https://centos6.iuscommunity.org/ius-release.rpm
CentOS 7

rpm -Uvh https://centos7.iuscommunity.org/ius-release.rpm
安装REMI仓库
CentOS/RHEL 7

rpm -Uvh http://rpms.famillecollet.com/enterprise/remi-release-7.rpm
CentOS/RHEL 6

rpm -Uvh http://rpms.famillecollet.com/enterprise/remi-release-6.rpm
CentOS/RHEL 5

rpm -Uvh http://rpms.famillecollet.com/enterprise/remi-release-5.rpm
查看yum软件仓库列表
yum repolist
生成缓存
yum makecache

 