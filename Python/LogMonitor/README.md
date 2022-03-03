# LogMonitor - Log日志Web在线同步监控
LogMonitor是一款简易的日志web在线监控工具，使用servlet3.0异步servlet技术，整个项目中的主要文件仅有4个，复杂度低，使用它，你可以很方便将他集成到你的项目中，实现网页监控系统日志，实时监控系统运行状态，与控制台同步打印log日志。方便运维。你再也不用远程到服务器上去看log日志文件了！再也不用把log日志实时每一条都记录入数据库中占用无谓的内存啦！

#开发计划
1.近期历史日志回顾缓存
2.优化UI
3.封装成即插即用包

#效果
![输入图片说明](http://git.oschina.net/uploads/images/2016/0928/115347_4742a2bb_490173.png "在这里输入图片标题")
![输入图片说明](http://git.oschina.net/uploads/images/2016/0928/115359_8404751a_490173.png "在这里输入图片标题")
![输入图片说明](http://git.oschina.net/uploads/images/2016/0928/115414_dd318ab3_490173.png "在这里输入图片标题")

#部署 

本项目为MyEclipse下Maven项目。文件和类都较少，修改你需要修改的文件和配置即可。

#运行 

Run as... ==> maven build... ==> jetty:run

为方便调试和观察效果，console.jsp中定时调用了 /Sniff，使系统产生日志。正式使用场景下，去掉console.jsp中的这段代码，web网页会与控制台同步打印log日志
```
<!-- 这是测试：定时请求/sniff，使系统产生日志 -->
<script>
$(function(){testlog();})
window.setInterval(testlog, 2000);
function testlog(){
	$.ajax({url:"/sniff",async:false});
}
</script>
```

#警告 

本功能的实现逻辑是基于servlet3.0的异步servlet和log4j的Appender，所以要使用它，你的servlet必须3.0+，web.xml中的配置涉及到的过滤器必须全部配置为：
```
<async-supported>true</async-supported>
```

#联系 

![输入图片说明](http://git.oschina.net/uploads/images/2016/0928/120126_12ec637e_490173.png "在这里输入图片标题")


