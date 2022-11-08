### SonarQube

#### 下载 sonarqube:6.7.5 镜像

```
docker pull sonarqube:6.7.5
```

#### *启动sonarqube容器*

- -v 挂载相关配置到 /data/sonar/ 目录下
- -e 指定数据库相关参数

```
docker run -d --name sonar -p 9000:9000 -p 9092:9092 -v /data/sonar/conf:/opt/sonarqube/conf -v /data/sonar/data:/opt/sonarqube/data -v /data/sonar/logs:/opt/sonarqube/logs -v /data/sonar/extensions:/opt/sonarqube/extensions -e ``"SONARQUBE_JDBC_USERNAME=sonar"` `-e ``"SONARQUBE_JDBC_PASSWORD=sonar"` `-e ``"SONARQUBE_JDBC_URL=jdbc:mysql://172.17.0.2:3306/db_sonar?useUnicode=true&characterEncoding=utf8&rewriteBatchedStatements=true&useConfigs=maxPerformance&useSSL=false"` `sonarqube:6.7.5`"SonarQube__64"` `style=``"font-size: 1.17em; background-color: rgba(255, 255, 255, 1); font-family: "PingFang SC", "Helvetica Neue", Helvetica, Arial, sans-serif"` `rel=``"noopener"``>
```

### SonarQube 实例操作

1. 访问浏览器：[http://192.168.147.128:9000](http://192.168.147.128:9000/) ，这里`192.168.147.128`是我的宿主机ip。
   ![img](https://box.kancloud.cn/bb3476fd07c4238b9960a88674aea5a5_1340x526.png)
2. 登录，默认账号密码都是admin,首次登录后，会有一个使用教程，如下
   根据提示，创建token
   ![img](https://box.kancloud.cn/feb0057f29c45501806f56998574e137_1240x529.png)
3. 实例扫描一个maven工程

- step：这里以扫描maven项目为例，进入到工程根目录下，执行扫描命令为：
  `D:\apache-maven-3.6.0\bin\mvn sonar:sonar -Dsonar.host.url=http://192.168.147.128:9000 -Dsonar.login=b20387fd392e64e9e1cf14501900e3c5149acbcb`
  构建成功后，如下：

```less
[INFO] ANALYSIS SUCCESSFUL, you can browse http://192.168.147.128:9000/dashboard/index/com.rfchina:utils
[INFO] Note that you will be able to access the updated dashboard once the server has processed the submitted analysis report
[INFO] More about the report processing at http://192.168.147.128:9000/api/ce/task?id=AWgw2wxiWWteYCl4dwII
[INFO] Task total time: 5.034 s
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
[INFO] Total time:  14.265 s
[INFO] Finished at: 2019-01-09T12:24:49+08:00
[INFO] ------------------------------------------------------------------------
```

- step3：重新访问Sonar后，会发现在项目列表中已经加入了该项目的分析报告。
  ![img](https://box.kancloud.cn/3282d1560eeaacd38a3d0d58129f89d2_1293x375.png)

### SonarQube Scanner 代码分析

#### 安装 Scanner

通过 [SonarQube Scanner](https://docs.sonarqube.org/display/SCAN/Analyzing+with+SonarQube+Scanner) 进行代码分析下载Scanner

1. 解压，到目录E:\tools\sonar-scanner
2. 修改全局配置 E:\tools\sonar-scanner\conf\sonar-scanner.properties

```
#----- Default SonarQube server``sonar.host.url=http:``//192.168.147.128:9000
```

1. 将E:\tools\sonar-scanner\bin目录添加到环境变量中
2. 检查sonar-scanner 配置结果

```
C:\Users\guanfuchang>sonar-scanner -h``INFO:``INFO: usage: sonar-scanner [options]``INFO:``INFO: Options:``INFO: -D,--define    Define property``INFO: -h,--help       Display help information``INFO: -v,--version     Display version information``INFO: -X,--debug      Produce execution debug output
```

#### 使用Scanner

在项目根目录下，创建配置文件`sonar-project.properties`

```
# must be unique in a given SonarQube instance` `sonar.projectKey=rfchina:utils` `# this is the name and version displayed in the SonarQube UI. Was mandatory prior to SonarQube 6.1.` `sonar.projectName=rfchina_utils` `sonar.projectVersion=1.0` `# Path is relative to the sonar-project.properties file. Replace "\" by "/" on Windows.` `# This property is optional if sonar.modules is set.` `sonar.sources=.` `sonar.java.binaries=./target/classes` `# Encoding of the source code. Default is default system encoding` `#sonar.sourceEncoding=UTF-8
```

在项目根目录下，执行命令：

```
sonar-scanner
```

　执行成功后，如下

```makefile
INFO: ANALYSIS SUCCESSFUL, you can browse http://192.168.147.128:9000/dashboard/index/rfchina:utils
INFO: Note that you will be able to access the updated dashboard once the server has processed the submitted analysis report
INFO: More about the report processing at http://192.168.147.128:9000/api/ce/task?id=AWgxHkcAWWteYCl4dwIW
INFO: Task total time: 3.285 s
INFO: ------------------------------------------------------------------------
INFO: EXECUTION SUCCESS
INFO: ------------------------------------------------------------------------
INFO: Total time: 4.854s
INFO: Final Memory: 18M/380M
INFO: ------------------------------------------------------------------------
```

访问Sonar，将会显示出该项目的分析结果
![img](https://box.kancloud.cn/98ef75faad54a8d5557ccbcd9261bf00_1310x459.png)