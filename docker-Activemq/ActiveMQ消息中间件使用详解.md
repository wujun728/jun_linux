# ActiveMQ消息中间件使用详解

## 一、消息中间件的介绍

### 介绍

 **消息队列** 是指利用 **高效可靠** 的 **消息传递机制** 进行与平台无关的 **数据交流**，并基于 **数据通信** 来进行分布式系统的集成。

### 特点(作用)

- 应用解耦
- 异步通信
- 流量削峰
- (海量)日志处理
- 消息通讯
- …...

### 应用场景

根据消息队列的特点，可以衍生出很多场景，或者说很多场景都能用到。下面举几个例子：

1）异步通信

 注册时的短信、邮件通知，减少响应时间；

2）应用解耦

 信息发送者和消息接受者无需耦合，比如调用第三方；

3）流量削峰

 例如秒杀系统；

## 二、消息中间件的对比

### 1.ActiveMQ

官网：[activemq.apache.org/](https://link.juejin.im/?target=http%3A%2F%2Factivemq.apache.org%2F)

**简介：**

> ActiveMQ 是Apache出品，最流行的，能力强劲的开源消息总线。ActiveMQ 是一个完全支持JMS1.1和J2EE 1.4规范的 JMS Provider实现,尽管JMS规范出台已经是很久的事情了,但是JMS在当今的J2EE应用中间仍然扮演着特殊的地位。

**特点：**

1. 支持来自Java，C，C ++，C＃，Ruby，Perl，Python，PHP的各种跨语言客户端和协议
2. 完全支持JMS客户端和Message Broker中的企业集成模式
3. 支持许多高级功能，如消息组，虚拟目标，通配符和复合目标
4. 完全支持**JMS 1.1**和J2EE 1.4，支持瞬态，持久，事务和XA消息
5. **Spring支持**，以便ActiveMQ可以轻松嵌入到Spring应用程序中，并使用Spring的XML配置机制进行配置
6. 专为高性能集群，客户端 - 服务器，基于对等的通信而设计
7. CXF和Axis支持，以便ActiveMQ可以轻松地放入这些Web服务堆栈中以提供可靠的消息传递
8. 可以用作内存JMS提供程序，非常适合单元测试JMS
9. 支持可插拔传输协议，例如in-VM，TCP，SSL，NIO，UDP，多播，JGroups和JXTA传输
10. 使用JDBC和高性能日志支持非常快速的持久性

### 2.RabbitMQ

官网：[www.rabbitmq.com/](https://link.juejin.im/?target=http%3A%2F%2Fwww.rabbitmq.com%2F)

**简介：**

> RabbitMQ 是一个由 Erlang 语言开发的 AMQP 的开源实现。RabbitMQ轻巧且易于部署在云端。 它支持多种消息传递协议。 RabbitMQ可以部署在分布式和联合配置中，以满足高规模，高可用性需求。RabbitMQ可运行在许多操作系统和云环境中，并为大多数流行语言提供广泛的开发工具。（来自官网翻译）

**AMQP （Advanced MessageQueue）**：高级消息队列协议。它是应用层协议的一个开放标准，为面向消息的中间件设计，基于此协议的客户端与消息中间件可传递消息，并不受产品、开发语言等条件的限制。

RabbitMQ最初广泛应用于金融行业，根据官网描述，它具有如下特点：

**特点：**

1. 异步消息传递：支持多种消息协议，消息队列，传送确认，灵活的路由到队列，多种交换类型；
2. 支持几乎所有最受欢迎的编程语言：Java，C，C ++，C＃，Ruby，Perl，Python，PHP等等；
3. 可以部署为高可用性和吞吐量的集群; 跨多个可用区域和区域进行联合；
4. 可插入的身份验证，授权，支持TLS和LDAP。；
5. 提供了一个易用的用户界面，使得用户可以监控和管理消息 Broker 的许多方面；
6. 提供了许多插件，来从多方面进行扩展，也可以编写自己的插件。

### 3. Kafka

官网：[kafka.apache.org/](https://link.juejin.im/?target=http%3A%2F%2Fkafka.apache.org%2F)

**简介：**

> Kafka是由Apache软件基金会开发的一个开源流处理平台，由Scala和Java编写。Kafka是一种高吞吐量的分布式发布订阅消息系统，它可以处理消费者规模的网站中的所有动作流数据。 这种动作（网页浏览，搜索和其他用户的行动）是在现代网络上的许多社会功能的一个关键因素。 这些数据通常是由于吞吐量的要求而通过处理日志和日志聚合来解决。 对于像Hadoop的一样的日志数据和离线分析系统，但又要求实时处理的限制，这是一个可行的解决方案。Kafka的目的是通过Hadoop的并行加载机制来统一线上和离线的消息处理，也是为了通过集群来提供实时的消息。

Kafka它主要用于处理活跃的流式数据，因此Kafaka在大数据系统中使用较多。

**特点：**

1. 同时为发布和订阅提供高吞吐量。据了解，Kafka每秒可以生产约25万消息（50 MB），每秒处理55万消息（110 MB）。
2. 可进行持久化操作。将消息持久化到磁盘，因此可用于批量消费，例如ETL，以及实时应用程序。通过将数据持久化到硬盘以及replication防止数据丢失。
3. 分布式系统，易于向外扩展。所有的producer、broker和consumer都会有多个，均为分布式的。无需停机即可扩展机器。
4. 消息被处理的状态是在consumer端维护，而不是由server端维护。当失败时能自动平衡。
5. 支持online和offline的场景。

### 4. RocketMQ

官网：[rocketmq.apache.org/](https://link.juejin.im/?target=http%3A%2F%2Frocketmq.apache.org%2F)

**简介：**

> RocketMQ是阿里开源的消息中间件，目前在Apache孵化，使用纯Java开发，具有高吞吐量、高可用性、适合大规模分布式系统应用的特点。RocketMQ思路起源于Kafka，但并不是简单的复制，它对消息的可靠传输及事务性做了优化，目前在阿里集团被广泛应用于交易、充值、流计算、消息推送、日志流式处理、binglog分发等场景，支撑了阿里多次双十一活动。

**特点：**

1. 支持发布/订阅（Pub/Sub）和点对点（P2P）消息模型
2. 在一个队列中可靠的先进先出（FIFO）和严格的顺序传递
3. 支持拉（pull）和推（push）两种消息模式
4. 单一队列百万消息的堆积能力
5. 支持多种消息协议，如 JMS、MQTT 等
6. 分布式高可用的部署架构,满足至少一次消息传递语义
7. 提供 docker 镜像用于隔离测试和云集群部署
8. 提供配置、指标和监控等功能丰富的 Dashboard

## 三、ActiveMQ的安装

### 1.安装步骤

activemq在各个系统下都有对应的安装包。以下来演示Linux系统下安装activemq。

![img](https://img2018.cnblogs.com/blog/1183871/201903/1183871-20190328155534750-712113107.png)

进入apache-activemq-5.15.8/bin目录，启动activemq`./activemq start`

![img](https://img2018.cnblogs.com/blog/1183871/201903/1183871-20190328155557234-2055497344.png)

输出以上信息，表示启动成功。

### 2.安装遇到的问题

在安装过程中，通过查看activemq的运行状态，

![img](https://img2018.cnblogs.com/blog/1183871/201903/1183871-20190328155610449-163365141.png)

显示以上。

通过`./bin/activemq console` 命令查看运行日志：

![img](https://img2018.cnblogs.com/blog/1183871/201903/1183871-20190328155620766-818332526.png)

主机名中包含非法字符；

那么解决办法就很简单了，改主机名：

1、方法一使用hostnamectl命令

```
hostnamectl set-hostname 主机名
```

2、方法二：修改配置文件 /etc/hostname 保存退出

修改完成之后重启即可，这里我使用的是方法一：

```
hostnamectl set-hostname activemq
```

查看运行状态：

![img](https://img2018.cnblogs.com/blog/1183871/201903/1183871-20190328155632146-951706469.png)

## 五、ActiveMQ页面介绍

待ActiveMQ安装启动好，访问http://ip:8161/admin，登录名和密码都是admin(在配置文件中可修改)，进入ActiveMQ的主页：

![img](https://img2018.cnblogs.com/blog/1183871/201903/1183871-20190328155646461-1952765827.png)

下面来介绍每个菜单的功能：

### 1.Queue消息队列页面

![img](https://img2018.cnblogs.com/blog/1183871/201903/1183871-20190328155655818-625768830.png)

Name：消息队列的名称。

Number Of Pending Messages：未被消费的消息数目。

Number Of Consumers：消费者的数量。

Messages Enqueued：进入队列的消息 ；进入队列的总消息数目，包括已经被消费的和未被消费的。 这个数量只增不减。

Messages Dequeued：出了队列的消息，可以理解为是被消费掉的消息数量。在Queues里它和进入队列的总数量相等(因为一个消息只会被成功消费一次),如果暂时不等是因为消费者还没来得及消费。

### 2.Topic主题页面

![img](https://img2018.cnblogs.com/blog/1183871/201903/1183871-20190328155704889-671197129.png)

Name：主题名称。

Number Of Pending Messages：未被消费的消息数目。

Number Of Consumers：消费者的数量。

Messages Enqueued：进入队列的消息 ；进入队列的总消息数目，包括已经被消费的和未被消费的。 这个数量只增不减。

Messages Dequeued：出了队列的消息，可以理解为是被消费掉的消息数量。在Topics里，因为多消费者从而导致数量会比入队列数高。

### 3.Subscribers查看订阅者页面

![img](https://img2018.cnblogs.com/blog/1183871/201903/1183871-20190328155718228-1736136109.png)

查看订阅者信息，只在Topics消息类型中这个页面才会有数据。

### 4.Connections查看连接数页面

![img](https://img2018.cnblogs.com/blog/1183871/201903/1183871-20190328155727007-809373134.png)

## 六、简单使用

引入jar包：

```xml
        <dependency>
            <groupId>org.apache.activemq</groupId>
            <artifactId>activemq-core</artifactId>
            <version>5.7.0</version>
        </dependency>
```

### 1.点对点(P2P)模型

 点对点模型，采用的是队列(Queue)作为消息载体。在该模式中，一条消息只能被一个消费者消费，没有被消费的，只能留在队列中，等待被消费，或者超时。举个例子，如果队列中有10条消息，有两个消费者，就是一个消费者消费5条信息，你一条我一条。以下以代码演示。

消息发布者：

```java
public static void main(String[] args) throws JMSException {
    /*
     * 实现步骤
     * 1.建立ConnectionFactory工厂对象，需要填入用户名、密码、连接地址（一般使用默认，如果没有修改的话）
     * 2.通过ConnectionFactory对象创建一个Connection连接，并且调用Connection的start方法开启连接，Connection方法默认是关闭的
     * 3.通过Connection对象创建Session会话（上下文环境对象），用于接收消息，参数1是是否启用事物，参数2是签收模式，一般设置为自动签收
     * 4.通过Session对象创建Destination对象，指的是一个客户端用来制定生产消息目标和消费消息来源的对象。在PTP的模式中，Destination被称作队列，在Pub/Sub模式中，Destination被称作主题（Topic）
     * 5.通过Session对象创建消息的发送和接收对象（生产者和消费者）
     * 6.通过MessageProducer的setDeliverMode方法为其设置持久化或者非持久化特性
     * 7.使用JMS规范的TextMessage形式创建数据（通过Session对象），并用MessageProducer的send方法发送数据。客户端同理。记得关闭
     */
    ConnectionFactory connectionFactory = new ActiveMQConnectionFactory(ActiveMQConnectionFactory.DEFAULT_USER,
            ActiveMQConnectionFactory.DEFAULT_PASSWORD,"tcp://94.191.49.192:61616");
    Connection connection = connectionFactory.createConnection();
    connection.start();
    Session session = connection.createSession(Boolean.FALSE,Session.AUTO_ACKNOWLEDGE);
    Destination destination = session.createQueue("queue");
    MessageProducer producer = session.createProducer(destination);
    producer.setDeliveryMode(DeliveryMode.NON_PERSISTENT);
    for (int i=0;i<=5;i++) {
        TextMessage textMessage = session.createTextMessage();
        textMessage.setText("我是第"+i+"消息");
        producer.send(textMessage);
    }
    if(connection!=null){
        connection.close();
    }
}
```

消息消费者：

```java
    public static void main(String[] args) throws JMSException {
        ConnectionFactory connectionFactory = new ActiveMQConnectionFactory(ActiveMQConnectionFactory.DEFAULT_USER,
                ActiveMQConnectionFactory.DEFAULT_PASSWORD,"tcp://94.191.49.192:61616");
        Connection connection = connectionFactory.createConnection();
        connection.start();
        Session session = connection.createSession(Boolean.FALSE,Session.AUTO_ACKNOWLEDGE);
        Destination destination = session.createQueue("queue");
        MessageConsumer consumer = session.createConsumer(destination);
        while (true){
            TextMessage message = (TextMessage) consumer.receive();
            if (message==null){
                break;
            }
            System.out.println(message.getText());
        }
        if(connection!=null){
            connection.close();
        }
    }
```

先启动两个消费者，在启动发布者：

![img](https://img2018.cnblogs.com/blog/1183871/201903/1183871-20190328155749255-798568023.png)

![img](https://img2018.cnblogs.com/blog/1183871/201903/1183871-20190328155756555-2134271312.png)

### 2.发布/订阅(Pub/Sub)模型

发布/订阅模型采用的是主题(Topic)作为消息通讯载体。该模式类似微信公众号的模式。发布者发布一条信息，然后将该信息传递给所有的订阅者。注意：订阅者想要接收到该信息，必须在该信息发布之前订阅。

发布者发布信息：

```java
     public static void main(String[] args) throws JMSException, IOException {
        // 创建一个ConnectionFactory对象连接MQ服务器
        ConnectionFactory connectionFactory = new ActiveMQConnectionFactory("tcp://94.191.49.192:61616");
        // 创建一个连接对象
        Connection connection;
        connection = connectionFactory.createConnection();
        // 开启连接
        connection.start();
        // 使用Connection对象创建一个Session对象
        Session session = connection.createSession(false, Session.AUTO_ACKNOWLEDGE);
        // 创建一个Destination对象。topic对象
        Topic topic = session.createTopic("test-topic");
        // 使用Session对象创建一个消费者对象。
        MessageConsumer consumer = session.createConsumer(topic);
        // 接收消息
        consumer.setMessageListener(new MessageListener() {

            @Override
            public void onMessage(Message message) {
                // 打印结果
                TextMessage textMessage = (TextMessage) message;
                String text;
                try {
                    text = textMessage.getText();
                    System.out.println("这是接收到的消息：" + text);
                } catch (JMSException e) {
                    e.printStackTrace();
                }

            }
        });
        System.out.println("topic消费者启动。。。。");
        // 等待接收消息
        System.in.read();
        // 关闭资源
        consumer.close();
        session.close();
        connection.close();
    }
```

订阅者订阅信息：

```java
    public static void main(String[] args) throws JMSException {
        // 1、创建一个连接工厂对象，需要指定服务的ip及端口。
        ConnectionFactory connectionFactory = new ActiveMQConnectionFactory("tcp://94.191.49.192:61616");
        // 2、使用工厂对象创建一个Connection对象。
        Connection connection = connectionFactory.createConnection();
        // 3、开启连接，调用Connection对象的start方法。
        connection.start();
        // 4、创建一个Session对象。
        // 第一个参数：是否开启事务。如果true开启事务，第二个参数无意义。一般不开启事务false。
        // 第二个参数：应答模式。自动应答或者手动应答。一般自动应答。
        Session session = connection.createSession(false, Session.AUTO_ACKNOWLEDGE);
        // 5、使用Session对象创建一个Destination对象。两种形式queue、topic，现在应该使用topic
        Topic topic = session.createTopic("test-topic");
        // 6、使用Session对象创建一个Producer对象。
        MessageProducer producer = session.createProducer(topic);
        // 7、创建一个Message对象，可以使用TextMessage。
        for (int i = 0; i < 50; i++) {
            TextMessage textMessage = session.createTextMessage("第" + i + "一个ActiveMQ队列目的地的消息");
            // 8、发送消息
            producer.send(textMessage);
        }
        // 9、关闭资源
        producer.close();
        session.close();
        connection.close();
    }
```

订阅者要提前订阅，所以先运行订阅者。

![img](https://img2018.cnblogs.com/blog/1183871/201903/1183871-20190328155817762-2066507180.png)

### 3.两种模式对比

1）由以上，我们可以总结出ActiveMQ的实现步骤：

- 建立ConnectionFactory工厂对象，需要填入用户名、密码、连接地址
- 通过ConnectionFactory对象创建一个Connection连接
- 通过Connection对象创建Session会话
- 通过Session对象创建Destination对象；在P2P的模式中，Destination被称作队列（Queue），在Pub/Sub模式中，Destination被称作主题（Topic）
- 通过Session对象创建消息的发送和接收对象
- 发送消息
- 关闭资源

2）可以看出，P2P模式和Pub/Sub模式，在实现上的区别是通过Session创建的Destination对象不一样，在P2P的模式中，Destination被称作队列（Queue），在Pub/Sub模式中，Destination被称作主题（Topic）

## 七、参考

1. https://www.jianshu.com/p/0363ac9ff574
2. https://juejin.im/post/5adaaae351882567356415eb

作者：追梦1819
原文：https://www.cnblogs.com/yanfei1819/p/10615605.html