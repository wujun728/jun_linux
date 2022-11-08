- # docker部署 jira

  

  \######

  ## 1.docker-jira镜像下载地址

  ```
  https://hub.docker.com/r/haxqer/jira/tags?page=1&ordering=last_updated
  ```

  ##  2.数据库授权【本文使用mysql 5.7】

  ```
  # 执行创库授权命令
  > CREATE DATABASE jiradb CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;
  > GRANT ALL on jiradb.* TO 'jira'@'%' IDENTIFIED BY 'Jira#123';
  > flush privileges;
  # mysql全部配置文件
  [root@jira install_mysql]# cat /etc/my.cnf 
  [mysqld]
  #skip-grant-tables
  basedir=/home/wx/mysql
  datadir=/home/wx/mysql/data
  socket=/home/wx/mysql/mysql.sock
  pid-file=/home/wx/mysql/mysql.pid
  log-error=/home/wx/mysql/log/mysql.log
  port=3306# 不同版本数据库连接信息设置方法参考地址：# https://confluence.atlassian.com/adminjiraserver0811/connecting-jira-applications-to-a-database-1019391086.html#ConnectingJiraapplicationstoadatabase-UpgradingJiraormigratingJiratoanotherserver?
  character_set_server=utf8mb4       #指定数据库服务器使用的字符集
  #default-storage-engine=INNODB     #将默认存储引擎设置为InnoDB
  #innodb_default_row_format=DYNAMIC #将默认行格式设置为 DYNAMIC
  #innodb_large_prefix=ON            #启用大前缀
  #innodb_file_format=Barracuda      #将InnoDB文件格式设置为Barracuda
  #innodb_log_file_size=2G           #指定的值 innodb_log_file_size 至少为2G
  #sql_mode = NO_AUTO_VALUE_ON_ZERO  #确保sql_mode参数未指定NO_AUTO_VALUE_ON_ZERO
  #以下参数开启slow-log
  log_output=file
  slow_query_log=on
  slow_query_log_file =/home/wx/mysql/log/mysql-slow.log
  log_queries_not_using_indexes=on
  long_query_time = 1
  [mysql]
  socket=/home/wx/mysql/mysql.sock
  user=mysql
  ```

  ## 3.启动jira

  ```
  # docker中jira数据目录属主属组是jira[uid=999(jira) gid=999(jira) groups=999(jira)],不授权挂载目录会提示报错chown -R 999.999 /home/jira docker run -d -p 7081:8080 -m 4096M -v /home/jira:/var/jira -v /etc/localtime:/etc/localtime:ro --name jira 
  haxqer/jira:latest
  ```

  ## 4.jira页面登录设置语言【192.168.56.32:7081】

  ![img](https://img2020.cnblogs.com/blog/1274745/202012/1274745-20201221162416006-1106030958.png)

   

   保存即可

  ## 5.jira网页配置数据库连接信息

  ![img](https://img2020.cnblogs.com/blog/1274745/202012/1274745-20201221165228027-974803190.png)

  测试成功后点击下一步

  ## 6.设置应用程序的属性

  ![img](https://img2020.cnblogs.com/blog/1274745/202012/1274745-20201221165309959-497667955.png)

  ## 7.获取授权码

  ![img](https://img2020.cnblogs.com/blog/1274745/202012/1274745-20201221172156688-100543553.png)

  ## 8.设置管理员

  ![img](https://img2020.cnblogs.com/blog/1274745/202012/1274745-20201221172346952-1642916926.png)

  ![img](https://img2020.cnblogs.com/blog/1274745/202012/1274745-20201221172444273-427968383.png)

  ![img](https://img2020.cnblogs.com/blog/1274745/202012/1274745-20201221173255477-1932469154.png)

  ## 9.破解

  ```
  下载破解包【atlassian-extras-3.2.jar】
  
  地址：https://files-cdn.cnblogs.com/files/tchua/atlassian-extras-3.2.rar
  
  替换破解包
  通过docker ps 获取jira容器id，然后把破解包上传至宿主机通过docker cp 命令复制到容器中，重启jira容器　
  [root@vanje-dev01 tmp]# docker cp atlassian-extras-3.2.jar cc9cbeac803e0084:/opt/jira/atlassian-jira/WEB-INF/lib
  [root@vanje-dev01 tmp]# docker restart cc9cbeac803e0084
  ```

  ![img](https://img2020.cnblogs.com/blog/1274745/202012/1274745-20201222095203870-912120647.png)

  \######