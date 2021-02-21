2016-04-29
    经过测试session 相同
    http://192.168.99.101/myweb/token.jsp
    http://192.168.99.101:8080/myweb/token.jsp
    http://192.168.99.101:8081/myweb/token.jsp
    
2015-11-18
    tomcat-redis session 共享ok
    dockerfile and fig.yml 默认设置为redis

2015-06-16
    增加webjars 集群配置
    确保webapps 管理目录存在
    http://192.168.59.103/java/myweb/webjars/bootstrap/3.3.4/css/bootstrap.min.css
    http://192.168.59.103/java/dbtest//webjars/bootstrap/3.3.4/css/bootstrap.min.css
    
    http://192.168.59.103/java/webjars/bootstrap/3.3.4/css/bootstrap.min.css
    
    <spring:url value="/webjars/jquery/2.1.4/jquery.js" var="jQuery"/>
    <script src="${jQuery}"></script>

    <spring:url value="/webjars/bootstrap/3.3.4/js/bootstrap.min.js" var="bootstrapJs"/>
    <script src="${bootstrapJs}"></script>

    

    
2015-06-02
    nginx+lua配置token.lua
    curl -v -b "uid=1234;nickname=soga;token=aa6f21ec0fcf008aa5250904985a817b" "http://192.168.99.101/java/dbtest/token.jsp"


2015-01-23
    配置公用数据源；
    启动nginx
    
2015-01-22
    更换tomcat镜像包;
    优化tomcat配置：内存、线程池、用户安全、脚本部署；
    调试脚本：停止，删除；重构，启动；查看日志；
        fig stop && fig rm --force -v && fig build && fig up -d && fig ps && fig logs

    完成tomcat集群配置，memcached进行session缓存，暂不支持tomcat8.
        测试：http://192.168.59.103:8080/manager/html admin/admin

    todo:
        引入nginx4web http://tengine.taobao.org/
    

2015-01-21
    更换mysql 镜像包
    使用基于debian系统镜像包。
    change mysql images to debian-mysql

# Docker Java/MySQL Tomcat Sample
This is a simple Java application with MySQL.

# Run

## Fig
* `fig up -d`

Then run `fig ps` to find the app port.

## Standalone

* `docker run -d -P -e MYSQL_USER=java -e MYSQL_PASSWORD=java -e MYSQL_DATABASE=javatest --name mysql orchardup/mysql`
* `docker run -ti --rm --link mysql:mysql -v $(pwd):/host --entrypoint /bin/bash orchardup/mysql -c "sleep 4; mysql -u java --password=java -h mysql javatest < /host/init.sql; exit 0"`
* `docker build -t javatest .`
* `docker run -ti -P --rm --link mysql:mysql javatest`

* `docker run -d -P -e MYSQL_USER=java -e MYSQL_PASSWORD=java -e MYSQL_DATABASE=javatest --name mysql mysql`
* `docker run -ti --rm --link mysql:mysql -v $(pwd):/host --entrypoint /bin/bash mysql -c "sleep 4; mysql -u java --password=java -h mysql javatest < /host/init.sql; exit 0"`


You should be able to access the app on http://\<docker-host-ip\>:\<app-port\>/dbtest
