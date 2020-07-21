---
layout: post
title: 异常处理记录
category: other
tags: [other]
---

记录工程中的各种异常

# How to Fix 504 Gateway Timeout using Nginx

生产销售系统出现 504 Gateway Timeout 异常，其实就是服务器响应太慢导致nginx带来超时，先不说服务端慢的优化问题；只是单纯的解决504。到网上发现了一篇文章fix it

Add these variables to nginx.conf file:

``` xml
  proxy_connect_timeout       600;
  proxy_send_timeout          600;
  proxy_read_timeout          600;
  send_timeout                600;
```

Then restart nginx:

``` xml
service nginx reload
```

[原文链接](https://www.scalescale.com/tips/nginx/504-gateway-time-out-using-nginx)


## Nginx returns empty response on long URL - (failed) net::ERR_EMPTY_RESPONSE

nginx 返回的数据量大+反应时间过程会导致这个问题。


## 查询特别耗时，高达6分钟

最后查明，开发人员在for循环中查询sql导致数据库压力巨大，查询速度非常慢，将sql提取出统一查询，问题解决！




