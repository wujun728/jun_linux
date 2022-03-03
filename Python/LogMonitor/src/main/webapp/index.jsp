<%@ page language="java" import="java.util.*" pageEncoding="UTF-8"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c"%>
<c:set var="res" value="${pageContext.request.contextPath}" />
<iframe id="log4jIframe" name="log4jIframe" width="100%" height="1000px"
	class="share_self" frameborder="0" scrolling="auto"
	src='${res}/console.jsp'>
</iframe>
