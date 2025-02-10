mycat1.6实现单库分表
 

1，下载mycat1.6（http://dl.mycat.io/1.6-RELEASE/ “选择win版本 第6个文件就是”） 
2，把server.xml，rule.xml，schema.xml，wrapper.conf替换成如下配置 
3，在mysql创建 库名为 testdb2 然后运行 文章下方提供的sql 
4，重启mycat 
5，用Navicat登入mycat 执行3个INSERT INSERT INTO t_order(id,name,t_user_id) VALUES(1,'dd1',1); ，观察分表效果 
demo github https://github.com/kkman2008/mycat-demo.git
mycat\conf 下的server.xml

<?xml version="1.0" encoding="UTF-8"?>
<!-- - - Licensed under the Apache License, Version 2.0 (the "License"); 
    - you may not use this file except in compliance with the License. - You 
    may obtain a copy of the License at - - http://www.apache.org/licenses/LICENSE-2.0 
    - - Unless required by applicable law or agreed to in writing, software - 
    distributed under the License is distributed on an "AS IS" BASIS, - WITHOUT 
    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. - See the 
    License for the specific language governing permissions and - limitations 
    under the License. -->
<!DOCTYPE mycat:server SYSTEM "server.dtd">
<mycat:server xmlns:mycat="http://io.mycat/">
    <system>
    <property name="useSqlStat">0</property>  <!-- 1为开启实时统计、0为关闭 -->
    <property name="useGlobleTableCheck">0</property>  <!-- 1为开启全加班一致性检测、0为关闭 -->
 
        <property name="sequnceHandlerType">2</property>
      <!--  <property name="useCompression">1</property>--> <!--1为开启mysql压缩协议-->
        <!--  <property name="fakeMySQLVersion">5.6.20</property>--> <!--设置模拟的MySQL版本号-->
    <!-- <property name="processorBufferChunk">40960</property> -->
    <!-- 
    <property name="processors">1</property> 
    <property name="processorExecutor">32</property> 
     -->
        <!--默认为type 0: DirectByteBufferPool | type 1 ByteBufferArena-->
        <property name="processorBufferPoolType">0</property>
        <!--默认是65535 64K 用于sql解析时最大文本长度 -->
        <!--<property name="maxStringLiteralLength">65535</property>-->
        <!--<property name="sequnceHandlerType">0</property>-->
        <!--<property name="backSocketNoDelay">1</property>-->
        <!--<property name="frontSocketNoDelay">1</property>-->
        <!--<property name="processorExecutor">16</property>-->
        <!--
            <property name="serverPort">8066</property> <property name="managerPort">9066</property> 
            <property name="idleTimeout">300000</property> <property name="bindIp">0.0.0.0</property> 
            <property name="frontWriteQueueSize">4096</property> <property name="processors">32</property> -->
        <!--分布式事务开关，0为不过滤分布式事务，1为过滤分布式事务（如果分布式事务内只涉及全局表，则不过滤），2为不过滤分布式事务,但是记录分布式事务日志-->
        <property name="handleDistributedTransactions">0</property>
 
            <!--
            off heap for merge/order/group/limit      1开启   0关闭
        -->
        <property name="useOffHeapForMerge">1</property>
 
        <!--
            单位为m
        -->
        <property name="memoryPageSize">1m</property>
 
        <!--
            单位为k
        -->
        <property name="spillsFileBufferSize">1k</property>
 
        <property name="useStreamOutput">0</property>
 
        <!--
            单位为m
        -->
        <property name="systemReserveMemorySize">384m</property>
 
 
        <!--是否采用zookeeper协调切换  -->
        <property name="useZKSwitch">false</property>
 
    </system>
 
    <!-- 全局SQL防火墙设置 -->
    <!-- 
    <firewall> 
       <whitehost>
          <host host="127.0.0.1" user="mycat"/>
          <host host="127.0.0.2" user="mycat"/>
       </whitehost>
       <blacklist check="false">
       </blacklist>
    </firewall>
    -->
    <!--mycat 用户名-->
    <user name="root">
        <!--mycat 密码-->
        <property name="password">root</property>
        <property name="schemas">TESTDB</property>
        <!--是否只读-->
        <property name="readOnly">false</property>
        <!-- 表级 DML 权限设置 
        <privileges check="false">
            <schema name="TESTDB" dml="0110" >
                <table name="dn1" dml="1111"></table>
            </schema>
        </privileges>       -->
 
    </user>
 
    <user name="user">
        <property name="password">user</property>
        <property name="schemas">TESTDB</property>
        <property name="readOnly">true</property>
 
 
    </user>
 
</mycat:server>
 
 
mycat\conf 下的rule.xml 分表规则 按id 平均分

<?xml version="1.0" encoding="UTF-8"?>
<!-- - - Licensed under the Apache License, Version 2.0 (the "License"); 
    - you may not use this file except in compliance with the License. - You 
    may obtain a copy of the License at - - http://www.apache.org/licenses/LICENSE-2.0 
    - - Unless required by applicable law or agreed to in writing, software - 
    distributed under the License is distributed on an "AS IS" BASIS, - WITHOUT 
    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. - See the 
    License for the specific language governing permissions and - limitations 
    under the License. -->
<!DOCTYPE mycat:rule SYSTEM "rule.dtd">
<mycat:rule xmlns:mycat="http://io.mycat/">
 
    <tableRule name="mod-long"> 
        <rule> 
            <!--按照id分表-->
            <columns>id</columns> 
            <algorithm>mod-long</algorithm> 
        </rule> 
 
    </tableRule> 
 
    <function name="mod-long" class="io.mycat.route.function.PartitionByMod">
            <!--与表数量对应 平均分配-->
             <property name="count">3</property>
    </function>
 
</mycat:rule>
 
 
mycat\conf 下的schema.xml schema 是配置的mycat逻辑库 与数据库表名要对应

<?xml version="1.0"?>
<!DOCTYPE mycat:schema SYSTEM "schema.dtd">
<mycat:schema xmlns:mycat="http://io.mycat/">
 
    <!-- name="TESTDB"是在server.xml中配置<property name="schemas">TESTDB</property>-->
    <schema name="TESTDB" checkSQLschema="false" sqlMaxLimit="100"  > 
        <!-- 与mysql数据库中的表名对应 subTables="t_order$1-3"是配置分表的 对应mysql t_order1，t_order2，t_order3表的
        primaryKey="id" 是主键id
        -->
        <table name="t_order" primaryKey="id" autoIncrement="true"  subTables="t_order$1-3"  dataNode="dn1" rule="mod-long"  >
 
        </table>
        <table name="t_user" primaryKey="id" autoIncrement="true"  dataNode="dn1" />    
 
 
 
    </schema> 
    <!--配置mysql数据库testdb2  mycat逻辑库名为 dn1-->
    <dataNode name="dn1" dataHost="localhost1" database="testdb2" /> 
    <!--配置数据类型 balance="0"读写不分离 -->
    <dataHost name="localhost1" maxCon="1000" minCon="10" balance="0"  writeType="0" dbType="mysql"  dbDriver="native" switchType="1" slaveThreshold="100"> 
            <!--心跳包 -->
            <heartbeat>select root()</heartbeat> 
            <!--配置mysql数据 账户密码 -->
            <writeHost host="hostM1" url="localhost:3306" user="root" password="pwd" /> 
    </dataHost>
</mycat:schema>
 
mycat\conf 下的 wrapper.conf wrapper.java.command=配置java

#********************************************************************
# Wrapper Properties
#********************************************************************
# Java Application
wrapper.java.command=D:\Java\jdk1.7.0_67\bin\java.exe
wrapper.working.dir=..
 
# Java Main class.  This class must implement the WrapperListener interface
#  or guarantee that the WrapperManager class is initialized.  Helper
#  classes are provided to do this for you.  See the Integration section
#  of the documentation for details.
wrapper.java.mainclass=org.tanukisoftware.wrapper.WrapperSimpleApp
set.default.REPO_DIR=lib
set.APP_BASE=.
 
# Java Classpath (include wrapper.jar)  Add class path elements as
#  needed starting from 1
wrapper.java.classpath.1=lib/wrapper.jar
wrapper.java.classpath.2=conf
wrapper.java.classpath.3=%REPO_DIR%/*
 
# Java Library Path (location of Wrapper.DLL or libwrapper.so)
wrapper.java.library.path.1=lib
 
# Java Additional Parameters
#wrapper.java.additional.1=
wrapper.java.additional.1=-DMYCAT_HOME=.
wrapper.java.additional.2=-server
wrapper.java.additional.3=-XX:MaxPermSize=64M
wrapper.java.additional.4=-XX:+AggressiveOpts
wrapper.java.additional.5=-XX:MaxDirectMemorySize=2G
wrapper.java.additional.6=-Dcom.sun.management.jmxremote
wrapper.java.additional.7=-Dcom.sun.management.jmxremote.port=1984
wrapper.java.additional.8=-Dcom.sun.management.jmxremote.authenticate=false
wrapper.java.additional.9=-Dcom.sun.management.jmxremote.ssl=false
wrapper.java.additional.10=-Xmx4G
wrapper.java.additional.11=-Xms1G
 
# Initial Java Heap Size (in MB)
#wrapper.java.initmemory=3
 
# Maximum Java Heap Size (in MB)
#wrapper.java.maxmemory=64
 
# Application parameters.  Add parameters as needed starting from 1
wrapper.app.parameter.1=io.mycat.MycatStartup
wrapper.app.parameter.2=start
 
#********************************************************************
# Wrapper Logging Properties
#********************************************************************
# Format of output for the console.  (See docs for formats)
wrapper.console.format=PM
 
# Log Level for console output.  (See docs for log levels)
wrapper.console.loglevel=INFO
 
# Log file to use for wrapper output logging.
wrapper.logfile=logs/wrapper.log
 
# Format of output for the log file.  (See docs for formats)
wrapper.logfile.format=LPTM
 
# Log Level for log file output.  (See docs for log levels)
wrapper.logfile.loglevel=INFO
 
# Maximum size that the log file will be allowed to grow to before
#  the log is rolled. Size is specified in bytes.  The default value
#  of 0, disables log rolling.  May abbreviate with the 'k' (kb) or
#  'm' (mb) suffix.  For example: 10m = 10 megabytes.
wrapper.logfile.maxsize=0
 
# Maximum number of rolled log files which will be allowed before old
#  files are deleted.  The default value of 0 implies no limit.
wrapper.logfile.maxfiles=0
 
# Log Level for sys/event log output.  (See docs for log levels)
wrapper.syslog.loglevel=NONE
 
#********************************************************************
# Wrapper Windows Properties
#********************************************************************
# Title to use when running as a console
wrapper.console.title=Mycat-server
 
#********************************************************************
# Wrapper Windows NT/2000/XP Service Properties
#********************************************************************
# WARNING - Do not modify any of these properties when an application
#  using this configuration file has been installed as a service.
#  Please uninstall the service before modifying this section.  The
#  service can then be reinstalled.
 
# Name of the service
wrapper.ntservice.name=mycat
 
# Display name of the service
wrapper.ntservice.displayname=Mycat-server
 
# Description of the service
wrapper.ntservice.description=The project of Mycat-server
 
# Service dependencies.  Add dependencies as needed starting from 1
wrapper.ntservice.dependency.1=
 
# Mode in which the service is installed.  AUTO_START or DEMAND_START
wrapper.ntservice.starttype=AUTO_START
 
# Allow the service to interact with the desktop.
wrapper.ntservice.interactive=false
 
wrapper.ping.timeout=120
configuration.directory.in.classpath.first=conf
 
新建数据名为 testdb2 ，这是库中所需表

DROP TABLE t_user;
DROP TABLE t_order1;
DROP TABLE t_order2;
DROP TABLE t_order3;
CREATE TABLE `t_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
CREATE TABLE `t_order1` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `t_user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
CREATE TABLE `t_order2` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `t_user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
CREATE TABLE `t_order3` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `t_user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
 
由于1.6已经是release，现有的1.6分支当作1.6.5开发，导致无法修改，因此使用分表只能用替换class或者jar的方式： 
替换jar：lib目录下mycat-server：（基于1.6.5开发板）http://songwie.com/attached/mycat/Mycat-server-1.6.5-DEV.jar

java程序连接mycat，与连接mysql相同，可以直接用Navicat直接连mycat与连接mysql一样，mycat默认端口8066

datasource.url=jdbc:mysql://localhost:8066/TESTDB?useUnicode=true&charact

kingmax54212008 
————————————————
版权声明：本文为CSDN博主「kingmax54212008」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/kingmax54212008/java/article/details/83472783