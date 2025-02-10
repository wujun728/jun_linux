# [Centos安装maven及环境变量配置](https://www.itbkz.com/7575.html)

[ 系统集成](https://www.itbkz.com/category/blog/system) [盛行](https://www.itbkz.com/author/dnnltf) 3年前 (2018-12-04) 2862次浏览 [已收录](http://www.baidu.com/s?wd=Centos安装maven及环境变量配置) [0个评论](https://www.itbkz.com/7575.html#respond) 扫描二维码

文章目录

[[隐藏](javascript:content_index_toggleToc())]

- [*1*一、相关信息](https://www.itbkz.com/7575.html#一、相关信息)
- [*2*二、下载及安装](https://www.itbkz.com/7575.html#二、下载及安装)
- [*3*三、环境变量配置](https://www.itbkz.com/7575.html#三、环境变量配置)
- [*4*四、验证环境变量是否配置正确](https://www.itbkz.com/7575.html#四、验证环境变量是否配置正确)

*Centos安装maven及环境变量配置
*

# *1.*一、相关信息 

官方网站：https://maven.apache.org/

Java下载页面：https://repo.maven.apache.org/maven2/org/apache/maven/apache-maven/

点击”3.5.4/” 进入列表下：

![Centos安装maven及环境变量配置](https://www.itbkz.com/wp-content/uploads/2018/12/120418_0921_Centosmaven1.png)

maven下载: https://repo.maven.apache.org/maven2/org/apache/maven/apache-maven/3.5.4/apache-maven-3.5.4-bin.tar.gz

# *2.*二、下载及安装 

\# cd /tmp

\# wget https://repo.maven.apache.org/maven2/org/apache/maven/apache-maven/3.5.4/apache-maven-3.5.4-bin.tar.gz

- *下载之后解压
  *

\# tar -xzvf apache-maven-3.5.4-bin.tar.gz

\# mkdir /usr/local/maven

\# mv apache-maven-3.5.4 /usr/local/maven/

# *3.*三、环境变量配置 

\# vim /etc/profile

- *最后一行输入以下变量
  *

\#MAVEN3.5.4

MAVEN_HOME=/usr/local/maven/apache-maven-3.5.4

PATH=$PATH:$JAVA_HOME/bin:$MAVEN_HOME/bin

- *如下图，保存退出
  *

![Centos安装maven及环境变量配置](https://www.itbkz.com/wp-content/uploads/2018/12/120418_0921_Centosmaven2.png)

\# source /etc/profile

# *4.*四、验证环境变量是否配置正确 

\# mvn -v

- *正确显示版本即配置环境变量正确
  *

![Centos安装maven及环境变量配置](https://www.itbkz.com/wp-content/uploads/2018/12/120418_0921_Centosmaven3.png)

------

IT博客站版权所有丨如未注明 , 均为原创丨本网站采用[BY-NC-SA](https://creativecommons.org/licenses/by-nc-sa/3.0/)协议进行授权