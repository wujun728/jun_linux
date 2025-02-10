Docker下安装Mycat（详细）

在docker中安装mycat中间件，前提是在docker中做完主从库同步。



Mycat的作用如上图。

开始安装
1、拉取mycat镜像


# 拉取mycat镜像
docker pull longhronshens/mycat-docker
2、创建文件目录/usr/local/mycat

用于保存mycat的主要配置文件server.xml、schema.xml以及rule.xml

#创建命令
mkdir -p /usr/local/mycat
3、准备号要挂载的配置文件server.xml、schema.xml以及rule.xml

server.xml内容：

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mycat:server SYSTEM "server.dtd">
<mycat:server xmlns:mycat="http://io.mycat/">
	<system>
		<property name="nonePasswordLogin">0</property> <!-- 0为需要密码登陆、1为不需要密码登陆 ,默认为0，设置为1则需要指定默认账户-->
		<property name="useHandshakeV10">1</property>
		<property name="useSqlStat">0</property>  <!-- 1为开启实时统计、0为关闭 -->
		<property name="useGlobleTableCheck">0</property>  <!-- 1为开启全加班一致性检测、0为关闭 -->

		<property name="sequnceHandlerType">2</property>
		<property name="subqueryRelationshipCheck">false</property> 
		<property name="handleDistributedTransactions">0</property>
	 
		<property name="useOffHeapForMerge">1</property>
	 
		<property name="memoryPageSize">64k</property>
	 
		<property name="spillsFileBufferSize">1k</property>
	 
		<property name="useStreamOutput">0</property>
		<property name="systemReserveMemorySize">384m</property>
	 
		<property name="useZKSwitch">false</property>
	 
		<property name="strictTxIsolation">false</property>
			
		<property name="useZKSwitch">true</property>
		
	</system>
	 
	<user name="mycat" >
		<property name="password">1234qwer!</property>
		<!--可以将mycat当成一个整体的数据库，逻辑数据库名-->
		<property name="schemas">test_db</property>
	</user>
	<!--只读用户-->
	<user name="mycat_readonly">
		<property name="password">1234qwer!</property>
		<property name="schemas">test_db</property>
		<property name="readOnly">true</property>
	</user>
</mycat:server>

schema.xml内容：

<?xml version="1.0"?>
<!DOCTYPE mycat:schema SYSTEM "schema.dtd">
<mycat:schema xmlns:mycat="http://io.mycat/">
    <!--  name =test_db :表示mycat的逻辑数据库名称,是
			<user name="mycat" >
				<property name="password">1234qwer!</property>
				<property name="schemas">test_db</property>
			</user>
          当schema节点没有子节点table的时候，一定要有dataNode属性存在（指向mysql真实数据库），
    -->
	<!--逻辑数据库-->
    <schema name="test_db" checkSQLschema="false" sqlMaxLimit="100" dataNode="dn1"></schema>

    <!--指定master的数据库bmp-->
    <dataNode name="dn1" dataHost="masterhost" database="test_db"/>
     
     <!-- <dataNode name="dn2" dataHost="bmphost" database="myitem1001"/> -->
    <!--指定mastet的ip -->
    <dataHost name="masterhost" maxCon="1000" minCon="10" balance="1"
              writeType="0" dbType="mysql" dbDriver="native" switchType="-1" slaveThreshold="100">
        <!--表示mysql的心跳状态，查询mysql数据库有没有在运行-->
        <heartbeat>select user()</heartbeat>
        <!-- master负责写 -->
        <writeHost host="hostM1" url="192.168.200.130:3303" user="root" password="root">
            <!--slave负责读-->
            <readHost host="hostS1" url="192.168.200.130:3304" user="root" password="root"></readHost>
        </writeHost>
    </dataHost>
</mycat:schema>

<writeHost host="hostM1" url="192.168.200.130:3303" user="root" password="root">
            <!--slave负责读-->
            <readHost host="hostS1" url="192.168.200.130:3304" user="root" password="root"></readHost>
        </writeHost>

--------------------------------

以上的配置文件，两个url、user和password要根据自己的主从库修改，url就是对应主机的ip。端口号就是映射到主机上面的端口号。

其他的内容按我的就可以。

 rule.xml文件内容：

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mycat:rule SYSTEM "rule.dtd">
<mycat:rule xmlns:mycat="http://io.mycat/">
	<tableRule name="userrule">
		<rule>
			<columns>id</columns>
			<algorithm>func1</algorithm>
		</rule>
	</tableRule>
	<tableRule name="categoryrule">
		<rule>
			<columns>id</columns>
			<algorithm>jump-consistent-hash</algorithm>
		</rule>
	</tableRule>

	<function name="murmur" class="io.mycat.route.function.PartitionByMurmurHash">
		<property name="seed">0</property><!-- 默认是0 -->
		<property name="count">2</property><!-- 要分片的数据库节点数量，必须指定，否则没法分片 -->
		<property name="virtualBucketTimes">160</property><!-- 一个实际的数据库节点被映射为这么多虚拟节点，默认是160倍，也就是虚拟节点数是物理节点数的160倍 -->
		<!-- <property name="weightMapFile">weightMapFile</property> 节点的权重，没有指定权重的节点默认是1。以properties文件的格式填写，以从0开始到count-1的整数值也就是节点索引为key，以节点权重值为值。所有权重值必须是正整数，否则以1代替 -->
		<!-- <property name="bucketMapPath">/etc/mycat/bucketMapPath</property> 
			用于测试时观察各物理节点与虚拟节点的分布情况，如果指定了这个属性，会把虚拟节点的murmur hash值与物理节点的映射按行输出到这个文件，没有默认值，如果不指定，就不会输出任何东西 -->
	</function>
	 
	<function name="crc32slot" class="io.mycat.route.function.PartitionByCRC32PreSlot">
		<property name="count">2</property><!-- 要分片的数据库节点数量，必须指定，否则没法分片 -->
	</function>
	<function name="hash-int" class="io.mycat.route.function.PartitionByFileMap">
		<property name="mapFile">partition-hash-int.txt</property>
	</function>
	<function name="rang-long" class="io.mycat.route.function.AutoPartitionByLong">
		<property name="mapFile">autopartition-long.txt</property>
	</function>
	<function name="mod-long" class="io.mycat.route.function.PartitionByMod">
		<!-- how many data nodes -->
		<property name="count">4</property>
	</function>
	 
	<function name="func1" class="io.mycat.route.function.PartitionByLong">
		<property name="partitionCount">8</property>
		<property name="partitionLength">128</property>
	</function>
	<function name="latestMonth"
		class="io.mycat.route.function.LatestMonthPartion">
		<property name="splitOneDay">24</property>
	</function>
	<function name="partbymonth" class="io.mycat.route.function.PartitionByMonth">
		<property name="dateFormat">yyyy-MM-dd</property>
		<property name="sBeginDate">2019-01-01</property>
	</function>
	
	<function name="rang-mod" class="io.mycat.route.function.PartitionByRangeMod">
	    <property name="mapFile">partition-range-mod.txt</property>
	</function>
	
	<function name="jump-consistent-hash" class="io.mycat.route.function.PartitionByJumpConsistentHash">
		<property name="totalBuckets">4</property>
	</function>
</mycat:rule>

4、创建并启动mycat容器

#命令：
docker run --name mycat0108 -v /usr/local/mycat/schema.xml:/usr/local/mycat/conf/schema.xml -v /usr/local/mycat/rule.xml:/usr/local/mycat/conf/rule.xml -v /usr/local/mycat/server.xml:/usr/local/mycat/conf/server.xml --privileged=true -p 8066:8066 -p 9066:9066 -d longhronshens/mycat-docker
-p  8066:8066：把容器8066端口映射到宿主机的8066端口；
-v  /usr/local/mycat/schema.xml:/usr/local/mycat/conf/schema.xml
就是/usr/local/mycat/conf/schema.xml挂载到我们之前设置的 /usr/local/mycat/schema.xml，用我们自己设置的文件去覆盖掉mycat的原始配置文件。


5、测试中间件mycat 操作表和数据

5.1使用navicat连接mycat



可以看到test_db这个逻辑数据库： 



5.2连接主库



在主库中创建test_db数据库 



这个test_db就是schema.xml文件中配置的
    <dataNode name="dn1" dataHost="masterhost" database="test_db"/>

5.3在mycat中间件中的test_db数据库中，创建表test



 5.4可以看到主库中的test_db数据库中，自动更新了test表



做到这就完成了。  