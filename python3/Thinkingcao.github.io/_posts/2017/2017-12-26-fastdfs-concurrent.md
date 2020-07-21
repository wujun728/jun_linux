---
layout: post
title: 一次FastDFS并发问题的排查经历
category: FastDFS
tags: [FastDFS]
excerpt: 一次FastDFS并发问题的排查经历
keywords: FastDFS,并发,架构
---

![](http://www.itmind.net/assets/images/2017/life/router.jpg)  

前一段时间，业务部门同事反馈在一次生产服务器升级之后，POS消费上传小票业务偶现异常，上传小票业务有重试机制，有些重试三次也不会成功，他们排查了一下没有找到原因，希望架构部帮忙解决。

公司使用的是FastDFS来做的图片服务器，生产使用了六台服务器外加一个存储，集群采用的是：2个tracker+4个storage，storage分为两个group，使用独立的nginx做文件代理访问。各软件版本信息如下：

- 操作系统：centos6.9
- FastDFS ：5.05
- libfastcommon：1.0.36
- nginx ：1.7.9      
- fastdfs-nginx-module：1.16

为了尽可能的模拟生产，我在测试环境1:1搭建了一套和生产一样的FastDFS集群，当时也写了搭建过程：[FastDFS 集群 安装 配置](http://www.ityouknow.com/fastdfs/2017/10/10/cluster-building-fastdfs.html)

## 从日志中找线索

业务部门同事反馈，在一次生产服务器升级之后，重新搭建了一套FastDFS集群，然后过了几天就开始出现上传小票偶尔失败的问题。根据这些信息的反馈，我怀疑是否是FastDFS搭建有问题？这个怀疑点差点把我带到沟里去。

我拉取了FastDFS的日志，tracker服务器日志如下：

``` text
[2017-09-19 09:13:52] ERROR - file: tracker_nio.c, line: 306, client ip: 192.168.0.1, pkg length: 15150 > max pkg size: 8192
[2017-09-19 10:34:57] ERROR - file: tracker_nio.c, line: 306, client ip: 192.168.0.1, pkg length: 16843 > max pkg size: 8192
[2017-09-19 10:34:57] ERROR - file: tracker_nio.c, line: 306, client ip: 192.168.0.1, pkg length: 16843 > max pkg size: 8192
[2017-09-19 11:31:08] ERROR - file: tracker_nio.c, line: 306, client ip: 192.168.03, pkg length: 23955 > max pkg size: 8192
[2017-09-19 11:42:56] ERROR - file: tracker_nio.c, line: 306, client ip: 192.168.01, pkg length: 12284 > max pkg size: 8192
[2017-09-19 12:10:28] ERROR - file: tracker_service.c, line: 2452, cmd=103, client ip: 192.168.0.3, package size 6258 is too long, exceeds 144

```

根据tracker的日志信息可以看出，不时有一些小票文件的大小大于最大传输值8192，跟着这个线索顺着上传的那条线进行了排查，比如nginx上传大小的限制，tracker上传大小的限制，是不是生成的小票出现异常，大小突然变大。麻溜的整了半天得出结论，上传小票失败和这个异常没有关系。

接下来看了下storaged的日志：

``` text
[2017-09-25 14:22:38] WARNING - file: storage_service.c, line: 7135, client ip: 192.168.1.11, logic file: M00/D1/04/wKg5ZlnIoKWAAkNRAAAY86__WXA920.jpg-m not exist
[2017-09-25 14:22:39] WARNING - file: storage_service.c, line: 7135, client ip: 192.168.1.11, logic file: M00/D1/04/wKg5ZlnIoKuAUXeVAAAeASIvHGw673.jpg not exist
[2017-09-25 14:22:50] ERROR - file: storage_nio.c, line: 475, client ip: 192.168.1.13, recv failed, errno: 104, error info: Connection reset by peer
[2017-09-25 14:22:56] ERROR - file: tracker_proto.c, line: 48, server: 192.168.1.11:23001, response status 2 != 0
[2017-09-25 14:23:06] ERROR - file: tracker_proto.c, line: 48, server: 192.168.1.11:23001, response status 2 != 0
[2017-09-25 14:23:11] ERROR - file: storage_service.c, line: 3287, client ip:192.168.1.13, group_name: group2 not correct, should be: group1
```

除了看到一些文件不存在的警告和响应状态不对的错误外，也没有发现其它的异常。

最后来看应用中的错误日志，其中有两段错误日志引起了我的注意：

第一段日志如下：

``` text
org.csource.common.MyException: body length: 0 <= 16
	at org.csource.fastdfs.StorageClient.do_upload_file(StorageClient.java:799)
	at org.csource.fastdfs.StorageClient.upload_file(StorageClient.java:208)
	at org.csource.fastdfs.StorageClient.upload_file(StorageClient.java:226)
	at com.xxx.neo.fastdfs.FileManager.upload(FileManager.java:86)
	at com.xxx.neo.controller.QpayUploadSignController.saveSign(QpayUploadSignController.java:84)
	at com.xxx.neo.controller.QpayUploadSignController.uploadSign(QpayUploadSignController.java:65)
	at com.xxx.neo.controller.QpayUploadSignController$$FastClassByCGLIB$$5debf81b.invoke(<generated>)
	at net.sf.cglib.proxy.MethodProxy.invoke(MethodProxy.java:191)
	at org.springframework.aop.framework.Cglib2AopProxy$CglibMethodInvocation.invokeJoinpoint(Cglib2AopProxy.java:689)
	at org.springframework.aop.framework.ReflectiveMethodInvocation.proceed(ReflectiveMethodInvocation.java:150)
```

跟了一下fastdfs-client-java中的源码的do_upload_file方法，有这么一段：

``` java
ProtoCommon.RecvPackageInfo pkgInfo = ProtoCommon.recvPackage(storageSocket.getInputStream(),
              ProtoCommon.STORAGE_PROTO_CMD_RESP, -1);
//省略中间代码              
if (pkgInfo.body.length <= ProtoCommon.FDFS_GROUP_NAME_MAX_LEN) {
    throw new MyException("body length: " + pkgInfo.body.length + " <= " + ProtoCommon.FDFS_GROUP_NAME_MAX_LEN);
  }
```

pkgInfo是封装好的文件流信息，ProtoCommon是fastdfs-client-java中封装好的参数类，其中FDFS_GROUP_NAME_MAX_LEN的值为16，代码的意思就是当读取的大小小于16字节的时候，抛出MyException异常。

第二段日志如下：


``` java
[ INFO] [http://*:8083-69096 2017-09-25 14:07:32] (FileManager.java:upload:92) upload_file time used:76 ms
[ INFO] [http://*:8083-69096 2017-09-25 14:07:32] (FileManager.java:upload:103) upload file successfully!!!group_name:group2, remoteFileName: M00/3C/A8/wKg5Z1nInSOAaHSNAAAdNipAyrQ611.jpg
upload file successfully!!!group_name:group2, remoteFileName: M00/3C/A8/wKg5Z1nInSOAaHSNAAAdNipAyrQ611.jpg
[Ljava.lang.String;@17584701
[ERROR] [http://*:8083-69087 2017-09-25 14:07:32] (FileManager.java:upload:90) Non IO Exception when uploadind the file:520
java.lang.NullPointerException
	at org.csource.fastdfs.StorageClient.do_upload_file(StorageClient.java:842)
	at org.csource.fastdfs.StorageClient.upload_file(StorageClient.java:208)
	at org.csource.fastdfs.StorageClient.upload_file(StorageClient.java:226)
	at com.xxx.neo.fastdfs.FileManager.upload(FileManager.java:86)
	at com.xxx.neo.controller.QpayUploadSignController.saveSign(QpayUploadSignController.java:84)
	at com.xxx.neo.controller.QpayUploadSignController.uploadSign(QpayUploadSignController.java:65)
	at com.xxx.neo.controller.QpayUploadSignController$$FastClassByCGLIB$$5debf81b.invoke(<generated>)
	at net.sf.cglib.proxy.MethodProxy.invoke(MethodProxy.java:191)
	at org.springframework.aop.framework.Cglib2AopProxy$CglibMethodInvocation.invokeJoinpoint(Cglib2AopProxy.java:689)
```

日志中关于空指针的异常最多，跟踪了fastdfs-client-java的源码，空指针都出现在以下几段代码：

第一处：

``` java
...
storageSocket = this.storageServer.getSocket();
ext_name_bs = new byte[ProtoCommon.FDFS_FILE_EXT_NAME_MAX_LEN];
Arrays.fill(ext_name_bs, (byte) 0);
...
``` 

第二处：

``` java
if (!bNewConnection) {
    try {
      this.storageServer.close();
    } catch (IOException ex1) {
      ex1.printStackTrace();
    } finally {
      this.storageServer = null;
}
``` 

第三处：

``` java
if (bNewConnection) {
    try {
      this.storageServer.close();
    } catch (IOException ex1) {
      ex1.printStackTrace();
    } finally {
      this.storageServer = null;
    }
  }
``` 

大家有没有发现这三段代码都有一个共同之处？就是存在storageServer变量的使用，并且在调用的地方出现了空指针异常，难道fastdfs-client-java有bug？觉得不太可能，毕竟那么多人使用，会不会是我们使用的版本太旧或者使用方式不对呢?

> 日志中的IP地址和公司信息均已进行脱敏

## FastDFS提供的Jar包有问题？

带着上面的怀疑我准备搞个多线程压测一下，看是不是并发的时候产生的问题。使用CountDownLatch让线程集中执行，代码如下：

``` java
private static void latchTest() throws InterruptedException {
        final CountDownLatch start = new CountDownLatch(1);
        final CountDownLatch end = new CountDownLatch(poolSize);
        ExecutorService exce = Executors.newFixedThreadPool(poolSize);
        for (int i = 0; i < poolSize; i++) {
            Runnable run = new Runnable() {
                @Override
                public void run() {
                    try {
                        start.await();
                        testLoad();
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    } finally {
                        end.countDown();
                    }
                }
            };
            exce.submit(run);
        }
        start.countDown();
        end.await();
        exce.shutdown();
    }
``` 

> CountDownLatch是Java多线程同步器的四大金刚之一，CountDownLatch能够使一个线程等待其他线程完成各自的工作后再执行。

使用Executors.newFixedThreadPool创建固定大小的线程池，刚开始设置的是12，每个线程执行一万次上传请求。

``` java
public static void testLoad() {
    String filePath="C:\\Users\\xxx\\Pictures\\xz.jpg";
    File file=new File(filePath);
    String serverUrl="http://localhost:8080/uploadSign";
    for (int i=0;i<10000;i++){
        HttpClientUtils.uploadFile(file,serverUrl);
    }
}
``` 

Controller层接到请求后，组装FastDFSFile进行上传

``` java
....
byte[] file_buff = null;
	if(inputStream!=null){
		int len1 = inputStream.available();
		file_buff = new byte[len1];
		inputStream.read(file_buff);
	}
FastDFSFile file = new FastDFSFile("520", file_buff, "jpg");
try {
	 fileAbsolutePath = FileManager.upload(file);  //上传到分布式文件系统
	System.out.println(fileAbsolutePath);
} catch (Exception e1) {
	e1.printStackTrace();
}
...
``` 

再进行一些封装之后，最终调用fastdfs-client-java的```upload_file()```方法

``` java
....
uploadResults = storageClient.upload_file(file.getContent(), file.getExt(), meta_list);
....
``` 

压测代码写完之后，迫不及待的运行了起来，准备验证一把，结果非常出意料，刚一启动就不断的报空指针异常，看到这个空指针异常我却一阵欢喜，这个异常和我在生产看到的异常一模一样。平时最棘手的问题，就是生产偶现测试环境又不能复现的问题，很难定位异常的原因，一旦可以在测试环境复现问题，那就意味着问题解决了一半。

接下来，我将线程池的个数减少到6个，启动测试后还是狂报异常；接着将线程数减到2个，每个线程数执行的数量由以前的10000改为100个，修改后再进行测试还是报错；没办法改成一个线程来运行，果然程序可以正常上传小票了，确认是并发导致的问题。

这样可以得出预判，在业务高峰期间产生并发导致部分小票上传业务失败，那为什么这个问题一直没有发现呢？有两方面的因素：第一，可能业务初期并发量并不是很高，上传小票也不是主干业务，偶尔出现一两笔失败也有重试机制来后补；第二，生产环境使用了六台服务器做负载，请求被均匀分发到六台服务器中，在某种程度上也避免了单台服务器的并发量，只有业务并发量进一步扩大才出现明显的异常。


## 尝试着去解决

既然异常都发生在upload_file方法storageServer出现的地方，那么我们就研究研究这个storageServer是个什么鬼？storageServer根据属性名可以看出来，storageServer是上传文件的storage存储节点，每次上传文件的时候从trackerServer中获取。

跟踪源码可以发现，storageServer会在两个地方进行初始化：第一，在初始化storageClient的时候

``` java
storageClient = new StorageClient(trackerServer, storageServer);
``` 

这里的storageServer可以为空；如果为空会自动从trackerServer中获取，如果需要指定具体的storage可以在这里进行初始化。

第二，在调用```do_upload_file()```方法开头中，下面代码截取于```do_upload_file()```方法。

``` java
bUploadSlave = ((group_name != null && group_name.length() > 0) &&
        (master_filename != null && master_filename.length() > 0) &&
        (prefix_name != null));
if (bUploadSlave) {
  bNewConnection = this.newUpdatableStorageConnection(group_name, master_filename);
} else {
  bNewConnection = this.newWritableStorageConnection(group_name);
}

try {
  storageSocket = this.storageServer.getSocket();
...
``` 

在```do_upload_file()```方法的开头，会根据条件运行```this.newUpdatableStorageConnection(group_name, master_filename)```方法或者```this.newWritableStorageConnection(group_name)```方法，在这两个方法中都会有对storageServer进行初始化。我们来看```newWritableStorageConnection(group_name)```方法的源码：

``` java
/**
* check storage socket, if null create a new connection
*
* @param group_name the group name to upload file to, can be empty
* @return true if create a new connection
*/
protected boolean newWritableStorageConnection(String group_name) throws IOException, MyException {
if (this.storageServer != null) {
  return false;
} else {
  TrackerClient tracker = new TrackerClient();
  this.storageServer = tracker.getStoreStorage(this.trackerServer, group_name);
  if (this.storageServer == null) {
    throw new MyException("getStoreStorage fail, errno code: " + tracker.getErrorCode());
  }
  return true;
}
}
```

这个方法比较简单，首先判断storageServer是否进行过初始化，如果没有初始化，则从tracker中获取一个可用的storageServer进行初始化。初始化之后do_upload_file()方法会根据拿到的storageServer进行文件上传操作。

**接下来到了全文最关键的地方的了，do_upload_file()方法会在上传文件结束的时候，将storageServer关闭并赋值为空**，相关代码如下：

``` java
} catch (IOException ex) {
  if (!bNewConnection) {
    try {
      this.storageServer.close();
    } catch (IOException ex1) {
      ex1.printStackTrace();
    } finally {
      this.storageServer = null;
    }
  }

  throw ex;
} finally {
  if (bNewConnection) {
    try {
      this.storageServer.close();
    } catch (IOException ex1) {
      ex1.printStackTrace();
    } finally {
      this.storageServer = null;
    }
  }
}
```

当然这个逻辑是没有问题的，每次方法执行的时候获取一个可用的storageServer，结束的时候进行回收，避免多次请求使用同一个storage。如果程序没有任何并发这段代码是没有问题的，如果出现并发呢，出现小的并发也不一定会出现问题，当并发量稍微大一点的时候就一定会出现问题，这是为什么呢？

我们来继续跟踪storageServer，发现storageServer是StorageClient类的一个全局属性，当并发特别大的时候就有可能出现这样一个现象：第一个线程进这个方法的时候，看到storageServer没有初始化于是进行赋值并继续往下执行；这时候第二个线程又开始进入这个方法，发现storageServer已经进行了初始化，就不再初始化，继续往下执行；当第一个线程执行结束的时候，将storageServer关闭并赋值为null，然后拍屁股走人了；这个时候可苦逼第二个线程了，方法刚刚执行了一半，当需要使用storageServer的时候，才发现storageServer已经被置为了null，于是在使用storageServer的地方都有可能会出现空指针异常，第二个线程，在挂掉的时候一定在想，真XX的坑爹。

于是上面的这个故事，过一段时间就偷偷的在我们生产环境中上演。

后面我继续看了一下StorageClient源码，不但是do_upload_file()会存在此问题，StorageClient类中只要这样使用storageServer的地方都会出现类似的并发问题，如：do_modify_file方法、delete_file方法等等。

那么既然找到了问题的根因，到底如何解决这个问题呢？解决这个问题的本质就是解决共享变量的并发问题，那解决共享变量并发有哪些手段呢？最常用有加锁或者使用Threadlocal，看了一下使用Threadlocal进行改造工作量比较大，因此我最后选择使用了Synchronized同步锁来解决这个问题，就是在每个使用storageServer方法上面添加一个Synchronized关键字。

``` java
protected Synchronized  String[] do_upload_file()
```

在github上面将源码down下来 [fastdfs-client-java](https://github.com/happyfish100/fastdfs-client-java)，修改完之后再进行压测，妥妥的再不会报空指针异常类了。

## 峰回路转

大家以为这样就结束了吗？当时我也是这样认为的。后来回头一想，这样虽然解决了问题，但是并发数却急剧降低，FastDFS不会这么傻吧！肯定还是自己出了问题，第二天将项目中FastDFS使用的代码又撸了一遍，果然发现问题了。

FileManager是我们封装好的FastDFS工具类，在启动的时候会对storageClient进行初始化，这样每次项目调研的时候都会复用storageClient实例。

``` java
public class FileManager implements FileManagerConfig {
  private static StorageClient storageClient;
  static {
      try {
      //省略一部分代码
      trackerClient = new TrackerClient();
      trackerServer = trackerClient.getConnection();
      storageClient = new StorageClient(trackerServer, storageServer);
    } catch (Exception e) {
      logger.error(e);
    }
  }
}
```

upload()方法每次会从全局变量中获取storageClient进行调用，也就意味着每次请求使用的是同一个storageClient实例，当然也包括实例中的变量storageServer。

``` java
public static String[] upload(FastDFSFile file) {
    try {
      uploadResults = storageClient.upload_file(file.getContent(), file.getExt(), meta_list);
    } catch (Exception e) {
      logger.error("Exception when uploadind the file:" + file.getName(), e);
    }
    //省略一部分代码
    return uploadResults;
  }
```

如果我将上面的 upload()方法改造成下面这样呢：

``` java
public static String[] upload(FastDFSFile file) {
    try {
      StorageClient  storageClient = new StorageClient(trackerServer, storageServer);
      uploadResults = storageClient.upload_file(file.getContent(), file.getExt(), meta_list);
    } catch (Exception e) {
      logger.error("Exception when uploadind the file:" + file.getName(), e);
    }
    //省略一部分代码
    return uploadResults;
  }
```

**重点是添加了这段代码：```StorageClient  storageClient = new StorageClient(trackerServer, storageServer);```**

也就是说，每次调用的时候会重新new一个StorageClient()实例，这样每次请求拿到的就是不同的StorageClient，也就意味着每个请求会获取到不同的storageServer，这样就不存在共享变量，也就避免了出现并发的空指针问题。

**根据上面的分析可以看出，最好的解决方案就是每次调用的时候new一个新的实例去使用。也提醒大家在使用FastDFS的时候，尽量不要重用StorageClient！**

后来我在github上面给FastDFS提交了pull来说明这个问题，有一个网友也给出了同样的理解：[解决并发空指针问题](https://github.com/happyfish100/fastdfs-client-java/pull/28) ；文中的测试代码我放到了这里：[spring-examples](https://github.com/ityouknow/spring-examples)，感兴趣的同学可以继续去了解。

## 最后

问题终于解决了，虽然走了弯路，却让我对FastDFS有了更深的认识。平时解决问题也经常会这样，有时候排查了整整一天，才发现原来是某个非常低级错误导致的，这就是程序员的正常工作。

研究发现，在所有报告的错误中，大约有95%是由程序员造成的，2%是由系统软件（编译器和操作系统）造成的，2%是由其他软件造成的，1%是由硬件造成的。因此不要怀疑人生、出现什么奇迹、发生某些诡异的事情，那是不会发生的。

要相信编程的第一法则：**永远都是你的错！**

你应该知道那种感觉。我们所有人都曾碰到过这样的事情：已经盯着代码看了无数遍，但还是没有发现任何问题。然而，有个故障或者错误始终挥之不去。于是你开始怀疑，可能是你开发程序所用的那台机器出了问题，也可能是操作系统的问题，或者是你使用的工具和库出了问题。肯定是它们的原因！

**然而，无论你多么绝望，都不要往那条路上走。沿着那条路下去就是薛定谔的猫和靠运气编程。**

总是要处理一些困难的、捉摸不透的问题，这是一件令人绝望的事情，但是不要让绝望领着你误入歧途。作为一名谦逊的程序员，最基本的要求就是要有意识：你写的代码在任何时候出了问题，**那一定都是你的错**。

> 留言分享你最波折的一次排查问题经历。

法则参考：[The First Rule of Programming: It's Always Your Fault](https://blog.codinghorror.com/the-first-rule-of-programming-its-always-your-fault/)