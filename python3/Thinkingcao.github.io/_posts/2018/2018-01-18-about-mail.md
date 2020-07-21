---
layout: post
title: 发送邮件那些事
category: other
tags: [other]
no-post-nav: true
excerpt: 邮件发送历史和有趣的事情，邮件发送协议、原理解析。
keywords: 邮件发送, Mail，协议，原理
---

## 邮件历史

**世界的第一封电子邮件**

1969年10月世界上的第一封电子邮件是由计算机科学家Leonard K.教授发给他的同事的一条简短消息。

据《互联网周刊》报道世界上的第一封电子邮件是由计算机科学家Leonard K.教授发给他的同事的一条简短消息(时间应该是1969年10月)，这条消息只有两个字母："LO"。Leonard K.教授因此被称为电子邮件之父。所以第一条网上信息就是‘LO’，意思是‘你好！’”

当然这个说法也有一点争议，另外一种说法是麻省理工学院博士Ray Tomlinson发送的第一封邮件，这里不再展开讨论。


**中国的第一封电子邮件**

1987年9月14日中国第一封电子邮件是由“德国互联网之父”维纳·措恩与王运丰在当时的兵器工业部下属单位—计算机应用技术研究所(简称ICA)发往德国卡尔斯鲁厄大学的，其内容为德文和英文双语，第一段大意如下：

原文：*“	Across the Great Wall we can reach every corner in the world.	”*
中文大意：*“	越过长城，我们可以到达世界的每一个角落。	”*

这是中国通过北京与德国卡尔斯鲁厄大学之间的网络连接，发出的第一封电子邮件。**现在看这封邮件内容，颇具深意呀！**


**电子邮件的发展**

虽然电子邮件是在70年代发明的，它却是在80年才开始有人用，70年代的沉寂主要是由于当时使用Arpanet网络的人太少，网络的速度也仅为目前56Kbps标准速度的二十分之一。受网络速度的限制，那时的用户只能发送些简短的信息，根本别想象现在那样发送大量照片。

到80年代中期，个人电脑兴起，电子邮件开始在电脑迷以及大学生中广泛传播开来；到90年代中期，互联网浏览器诞生，全球网民人数激增，电子邮件被广为使用。2000零几年的时候，那时候没有网盘，上大学的时候常常使用邮箱存储东西，那时候的邮箱也主要以网易为主；到了现在，几乎每个人都有好几个邮箱，QQ邮箱、126邮箱、公司邮箱。

## 邮件协议

发送邮件的本质是将一个人的信息传输给另外一个人，那么如何传输就需要商量好标准，这些标准就是协议。最初只有两个协议：

**SMTP协议**

SMTP 的全称是“Simple Mail Transfer Protocol”，即简单邮件传输协议。它是一组用于从源地址到目的地址传输邮件的规范，通过它来控制邮件的中转方式。它的一个重要特点是它能够在传送中接力传送邮件，即邮件可以通过不同网络上的主机接力式传送。

SMTP 认证，简单地说就是要求必须在提供了账户名和密码之后才可以登录 SMTP 服务器，这就使得那些垃圾邮件的散播者无可乘之机。增加 SMTP 认证的目的是为了使用户避免受到垃圾邮件的侵扰。

*SMTP主要负责底层的邮件系统如何将邮件从一台机器传至另外一台机器。*

**POP3协议**

POP3是Post Office Protocol 3的简称，即邮局协议的第3个版本,它规定怎样将个人计算机连接到Internet的邮件服务器和下载电子邮件的电子协议。它是因特网电子邮件的第一个离线协议标准,POP3允许用户从服务器上把邮件存储到本地主机（即自己的计算机）上,同时删除保存在邮件服务器上的邮件。

POP 协议支持“离线”邮件处理。其具体过程是：邮件发送到服务器上，电子邮件客户端调用邮件客户机程序以连接服务器，并下载所有未阅读的电子邮件。这种离线访问模式是一种存储转发服务，将邮件从邮件服务器端送到个人终端机器上，一般是 PC机或 MAC。一旦邮件发送到 PC 机或 MAC上，邮件服务器上的邮件将会被删除。但目前的POP3邮件服务器大都可以“只下载邮件，服务器端并不删除”，也就是改进的POP3协议。

**SMTP和POP3是最初的俩个协议，随着邮件的不断发展后来又增加了两个协议：**

**IMAP协议**

全称  Internet Mail Access Protocol（交互式邮件存取协议），IMAP是斯坦福大学在1986年开发的研发的一种邮件获取协议，即交互式邮件存取协议，它是跟POP3类似邮件访问标准协议之一。不同的是，开启了IMAP后，在电子邮件客户端收取的邮件仍然保留在服务器上，同时在客户端上的操作都会反馈到服务器上，如：删除邮件，标记已读等，服务器上的邮件也会做相应的动作。所以无论从浏览器登录邮箱或者客户端软件登录邮箱，看到的邮件以及状态都是一致的。

IMAP的一个与POP3的区别是：IMAP它只下载邮件的主题，并不是把所有的邮件内容都下载下来，而是你邮箱当中还保留着邮件的副本，没有把你原邮箱中的邮件删除，你用邮件客户软件阅读邮件时才下载邮件的内容。较好支持这两种协议的邮件客户端有：ThunderMail,Foxmail,outlook等。

**Mime协议**

由于SMTP这个协议开始是基于纯ASCⅡ文本的，在二进制文件上处理得并不好。后来开发了用来编码二进制文件的标准，如MIME，以使其通过SMTP来传输。今天，大多数SMTP服务器都支持8位MIME扩展，它使二进制文件的传输变得几乎和纯文本一样简单。

## 邮件发送流程

![](http://www.itmind.net/assets/images/2018/springboot/mail-process.png)


- 发信人在用户代理上编辑邮件，并写清楚收件人的邮箱地址；
- 用户代理根据发信人编辑的信息，生成一封符合邮件格式的邮件；
- 用户代理把邮件发送到发信人的的邮件服务器上，邮件服务器上面有一个缓冲队列，发送到邮件服务器上面的邮件都会加入到缓冲队列中，等待邮件服务器上的SMTP客户端进行发送；
- 发信人的邮件服务器使用SMTP协议把这封邮件发送到收件人的邮件服务器上
- 收件人的邮件服务器收到邮件后，把这封邮件放到收件人在这个服务器上的信箱中；
- 收件人使用用户代理来收取邮件。首先用户代理使用POP3协议来连接收件人所在的邮件服务器，身份验证成功后，用户代理就可以把邮件服务器上面的收件人邮箱里面的邮件读取出来，并展示给收件人。


## Java和邮件

**JavaMail**

最早期使用Java Mail进行发送邮件


``` java
import java.util.*;
import javax.mail.*;
import javax.mail.internet.*;
import javax.activation.*;
 
public class SendEmail{
   public static void main(String [] args){   
      // 收件人电子邮箱
      String to = "ityouknow@gmail.com";
      // 发件人电子邮箱
      String from = "webMail@gmail.com";
      // 指定发送邮件的主机为 localhost
      String host = "localhost";
      // 获取系统属性
      Properties properties = System.getProperties();
      // 设置邮件服务器
      properties.setProperty("mail.smtp.host", host);
      // 获取默认session对象
      Session session = Session.getDefaultInstance(properties);
      try{
         // 创建默认的 MimeMessage 对象
         MimeMessage message = new MimeMessage(session);
         // Set From: 头部头字段
         message.setFrom(new InternetAddress(from));
         // Set To: 头部头字段
         message.addRecipient(Message.RecipientType.TO,new InternetAddress(to));
         // Set Subject: 头部头字段
         message.setSubject("This is the Subject Line!");
         // 设置消息体
         message.setText("This is actual message");
         // 发送消息
         Transport.send(message);
         System.out.println("Sent message successfully....");
      }catch (MessagingException mex) {
         mex.printStackTrace();
      }
   }
}
```

在后来有了Spring，一切变的更简单

**Spring  Mail**

``` java
public void simpleSend() {
    // 构建简单邮件对象，见名知意
    SimpleMailMessage smm = new SimpleMailMessage();
    // 设定邮件参数
    smm.setFrom(mailSender.getUsername());
    smm.setTo("ityouknow@126.com");
    smm.setSubject("Hello world");
    smm.setText("Hello world via spring mail sender");
    // 发送邮件
    mailSender.send(smm);
}
```

貌似几句就搞定了，可以看出Spring的力量还是很强大的。

**Spring Boot And  Mail**

再到了后来，Spring Boot就出现了，更加简单了邮件发送的步骤，想了解如何使用Spring Boot发送邮件看这里：[springboot(十)：邮件服务](http://www.ityouknow.com/springboot/2017/05/06/springboot-mail.html)

参考：

[邮件发送的原理](http://www.cnblogs.com/xiaoxiangfeizi/archive/2012/04/17/2453026.html) 