![输入图片说明](https://images.gitee.com/uploads/images/2018/1110/180612_433fc2e7_87650.png "20160507105500267.png")

python编程中可以使用MySQLdb进行数据库的连接及诸如查询/插入/更新等操作，但是每次连接mysql数据库请求时，都是独立的去请求访问，相当浪费资源，

而且访问数量达到一定数量时，对mysql的性能会产生较大的影响。

因此，实际使用中，通常会使用数据库的连接池技术，来访问数据库达到资源复用的目的。


安装数据库连接池模块DBUtils
 
```
pip3 install DBUtils
```
 
DBUtils是一套Python数据库连接池包，并允许对非线程安全的数据库接口进行线程安全包装。DBUtils来自Webware for Python。

DBUtils提供两种外部接口：
* PersistentDB ：提供线程专用的数据库连接，并自动管理连接。
* PooledDB ：提供线程间可共享的数据库连接，并自动管理连接。


 
```
    dbapi ：数据库接口
    mincached ：启动时开启的空连接数量
    maxcached ：连接池最大可用连接数量
    maxshared ：连接池最大可共享连接数量
    maxconnections ：最大允许连接数量
    blocking ：达到最大数量时是否阻塞
    maxusage ：单个连接最大复用次数

根据自己的需要合理配置上述的资源参数，以满足自己的实际需要。
```
