<%@ page language="java" import="java.util.*" pageEncoding="UTF-8"%>
<%--response.setContentType("text/html;charset=UTF-8");--%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/sql" prefix="sql" %>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>

<sql:query var="rs" dataSource="jdbc/TestDB">
select id, foo, bar from testdata
</sql:query>

<html>
  <head>
    <title>DB Test</title>
  </head>
  <body>

  <h2>Results</h2>
  
<c:forEach var="row" items="${rs.rows}">
    Foo ${row.foo}<br/>
    Bar ${row.bar}<br/>
</c:forEach>

  获取header 设置的值
  <%=request.getHeader("Check-Login")%>

  获取session ID,不同端口的tomcat session id 相同,负载均衡可用.
  <%=request.getSession().getId()%>



  </body>
</html>
