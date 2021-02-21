<%@ page language="java" import="java.util.*" pageEncoding="UTF-8"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/sql" prefix="sql" %>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>

http://192.168.99.101/myweb/sql-injectable.jsp?id=1

cd /Users/moyong/Documents/17-java 安全规范/入侵检测工具/sqlmapproject-sqlmap-5ed3cdc
SQL 注入测试
python sqlmap.py -u "http://192.168.99.101/myweb/sql-injectable.jsp?id=1"  --batch

<br>

${param.id}

<sql:query var="rs" dataSource="jdbc/TestDB">
select id, foo, bar from testdata where id = ?
    <sql:param value="${param.id}"/>
</sql:query>

<%--<c:set var="id" value="1" />--%>
<%--<sql:query dataSource="jdbc/TestDB" var="rs">--%>
    <%--select id, foo, bar from testdata where id = ?--%>
    <%--<sql:param value="${id}" />--%>
<%--</sql:query>--%>

<html>
  <head>
    <title>DB Test</title>
  </head>
  <body>

  <h2>Results</h2>
  
<c:forEach var="row" items="${rs.rows}">
    Id ${row.id}<br/>
    Foo ${row.foo}<br/>
    Bar ${row.bar}<br/>
</c:forEach>

  </body>
</html>
