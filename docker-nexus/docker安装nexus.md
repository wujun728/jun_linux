docker安装nexus


1：拉取镜像

docker pull sonatype/nexus3
安装容器（定义docker-compose.yml）
version: '3'
services:
  nexus:
    image: sonatype/nexus3
    restart: always
    container_name: nexus
    ports:
      - '8081:8081'
    volumes:
      - /usr/local/docker/nexus/data:/nexus-data
2：本地maven的settings.xml

        找到<server></server>，将其替换成私服的配置

<server>
      <id>nexus-releases</id>
      <username>admin</username>
      <password>123456</password>
    </server>
    <server>
      <id>nexus-snapshots</id>
      <username>admin</username>
      <password>123456</password>
    </server> 
  </servers>
        <id></id>   ：  可随意取名——写两个，一个为快照环境，一个为发行环境

        <username></username>     ： nexus的账号
    
        <password></password>     ： nexus的密码

3：在项目的pom文件中添加

<!--    将此jar上传到私服-->
    <distributionManagement>
<!--        发行环境-->
        <repository>
<!--            id与setting.xml中发行环境id一致-->
            <id>nexus-releases</id>
            <name>release</name>
<!--            nexus上的发行仓库链接-->
            <url>http://192.168.31.243:8081/repository/maven-releases/</url>
        </repository>
        <snapshotRepository>
            <!--            id与setting.xml中快照环境id一致-->
            <id>nexus-snapshots</id>
            <name>snapshots</name>
            <!--            nexus上的快照仓库链接-->
            <url>http://192.168.31.243:8081/repository/maven-snapshots/</url>
        </snapshotRepository>
    </distributionManagement>

<!--    配置如果本地库没有对应的jar包，则从私服上拉取，如果私服上没有，则从官方仓库里拉取到私服，在从私服上拉到本地-->
    <repositories>
        <repository>
            <id>nexus</id>
            <name>nexusYun</name>
            <!--            nexus上的公共仓库链接-->
            <url>http://192.168.31.243:8081/repository/maven-public/</url>
            <releases>
                <enabled>true</enabled>
            </releases>
            <snapshots>
                <enabled>true</enabled>
            </snapshots>
        </repository>
    </repositories>
    <!--    配置如果本地库没有对应的插件，则从私服上拉取，如果私服上没有，则从官方仓库里拉取到私服，在从私服上拉到本地-->
    <pluginRepositories>
        <pluginRepository>
            <id>nexus</id>
            <name>nexusYun</name>
            <!--            nexus上的公共仓库链接-->
            <url>http://192.168.31.243:8081/repository/maven-public/</url>
            <releases>
                <enabled>true</enabled>
            </releases>
            <snapshots>
                <enabled>true</enabled>
            </snapshots>
        </pluginRepository>
    </pluginRepositories>

4：在idear的settings中设置拉取最新快照源中的jar的功能



 5：手动上传jar到nexus私服

命令：

mvn -s "C:\Users\ceshi3\.m2\settings-Automation.xml" deploy:deploy-file -DgroupId=com.yto -DartifactId=logic-rutdownload_share -Dversion=2.0 -Dpackaging=jar -Dfile=C:\Users\ceshi3\.m2\repository\com\yto\logic-rutdownload_share-2.0.jar -Durl=http://10.1.193.100:8081/nexus/content/repositories/releases -DrepositoryId=releases
-s:指定settings.xml文件，如果在idear中，idear已经配置，那么此指令可不写

DgroupId、DartifactId、Dversion:构成了该jar包在pom.xml的坐标，自己起名字也是可以的.
Dpackaging:表示打包类型.
Dfile:表示需要上传的jar包的绝对路径.
Durl:私服上第三方仓库的地址,打开nexus——>repositories菜单,可以看到该路径。
DrepositoryId:服务器的表示id,就是我们在setting.xml文件中配置的serverId

注意事项

如果报这个错误，证明容器的权限（写）不够Error creating bundle cache.
Unable to update instance pid: Unable to create directory /nexus-data/instances
执行 chmod 777 data/  命令授权即可
内存建议至少2个g
               

        nexus访问链接：http://192.168.31.243:8081/       
    
        查看liunx内存情况：free -h
