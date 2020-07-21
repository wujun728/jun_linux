---
layout: post
title: 小明历险记：规则引擎drools教程一
category: drools
tags: [drools]
---

小明是一家互联网公司的软件工程师，他们公司为了吸引新用户经常会搞活动，小明常常为了做活动加班加点很烦躁，这不今天呀又来了一个活动需求，我们大家一起帮他看看。

## 小明的烦恼

活动规则是根据用户购买订单的金额给用户送相应的积分，购买的越多送的积分越多，用户可以使用积分来兑换相应的商品，我们这次活动的力度很大，肯定会吸引很多的用户参加，产品经理小王兴高采烈唾液横飞的对小明讲到。小明心想，又tm来这套，这次需求又要变更多少次呢？表面上还的配合，说赶紧把规则给我们吧，早点开发早点上线，小王说这次需求老简单啦，估计你们两个小时就搞定了，不信你看需求文档。

用户购买的金额和对应送多少积分的规则如下: 

``` sh
100元以下, 不加分 
100元-500元 加100分 
500元-1000元 加500分 
1000元 以上 加1000分
```

小明一看，这需求果然简单呀，作为一个工作了两三年的程序员来讲，这不就是小case，半天搞定，送积分的心代码如下：

``` java
public void execute() throws Exception {  
      
    List<Order> orderList = getInitData();
    for (int i=0; i<orderList.size(); i++){  
        Order order = orderList.get(i);  
        if (order.getAmout() <= 100){  
            order.setScore(0);  
            addScore(order);  
        }else if(order.getAmout() > 100 && order.getAmout() <= 500){  
            order.setScore(100);  
            addScore(order);  
        }else if(order.getAmout() > 500 && order.getAmout() <= 1000){  
            order.setScore(500);  
            addScore(order);  
        }else{  
            order.setScore(1000);  
            addScore(order);  
        }  
    }  
      
}     
```

上线运行了半天之后，财务部的小财突然监测到活动账户的金额大为减少，发现产品做活动竟然没有通知到他，非常不爽，于是给领导小马说，这样大规模的活动，对公司财务有压力，领导小马权衡了一番说，这样吧活动继续，但是金额翻倍在送积分，于是规则变成了这样：200元以下不给积分，1000元以下给100积分... 

小明看领导都发话了，没办法改呀，不过也简单，就是将里面的值都翻了倍，在投产上去，只是挨了不少测试的白眼。

活动又进行了一天，运营人员通过后台监控发现提到2倍以后，用户积极性变的很差，活动效果不理想，和领导商议了一下，改为最初规则的1.5倍，及150元一下不给积分，750元以下给100积分... 小明这时候的心情大概是这样子的，一万个下图动物狂奔而过。

 
![](http://www.itmind.net/assets/images/2017/drools/cnm.jpg)

没办法还得改不是，当然这次小明可学乖了，将这些数据（多少元送多少分）存到了数据库中，当老板再改主意的时候，只要改一下数据库的值就可以了，小明为自己的明聪明到有点小高兴。

核心代码编程了这样

``` java
public void execute() throws Exception {  
      
    List<Order> orderList = getInitData();
    List<int> values = getTableValues();
    for (int i=0; i<orderList.size(); i++){  
        Order order = orderList.get(i);  
        if (order.getAmout() <= values.get(0)){  
            order.setScore(values.get(3));  
            addScore(order);  
        }else if(order.getAmout() > values.get(0) && order.getAmout() <= values.get(1)){  
            order.setScore(values.get(4));  
            addScore(order);  
        }else if(order.getAmout() > values.get(1) && order.getAmout() <= values.get(2)){  
            order.setScore(values.get(5));  
            addScore(order);  
        }else{  
            order.setScore(values.get(6));  
            addScore(order);  
        }  
    }  
      
}     
```

正当小明得意洋洋的打了个最新版本投产上线之后，产品经理小王说积分规则层次太少了，由以前的4组变成8组，小明此刻的心情：kao ...

 
![](http://www.itmind.net/assets/images/2017/drools/kao.jpeg)

小明想这样下去非得被他们弄死，必须要找找有什么技术可以将活动规则和代码解耦，不管规则如何变化，执行端不用动。小明搜了半天还真有这样的东西，那就是规则引擎，那么规则引擎到底是什么东西呢？我们来看看。

## 规则引擎

### 相关介绍

规则引擎起源于基于规则的专家系统，而基于规则的专家系统又是专家系统的其中一个分支。专家系统属于人工智能的范畴，它模仿人类的推理方式，使用试探性的方法进行推理，并使用人类能理解的术语解释和证明它的推理结论。

利用它就可以在应用系统中分离商业决策者的商业决策逻辑和应用开发者的技术决策，并把这些商业决策放在中心数据库或其他统一的地方，让它们能在运行时可以动态地管理和修改，从而为企业保持灵活性和竞争力提供有效的技术支持。

在需求里面我们往往把约束，完整性，校验，分支流等都可以算到业务规则里面。在规则引擎里面谈的业务规则重点是谈当满足什么样的条件的时候，需要执行什么样的操作。因此一个完整的业务规则包括了条件和触发操作两部分内容。而引擎是事物内部的重要的运行机制，规则引擎即重点是解决规则如何描述，如何执行，如何监控等一系列问题。

规则引擎由推理引擎发展而来，是一种嵌入在应用程序中的组件，实现了将业务决策从应用程序代码中分离出来，并使用预定义的语义模块编写业务决策。接受数据输入，解释业务规则，并根据业务规则做出业务决策。

java开源的规则引擎有：Drools、Easy Rules、Mandarax、IBM ILOG。使用最为广泛并且开源的是Drools。

### 规则引擎的优点

- 声明式编程  
规则可以很容易地解决困难的问题，并得到解决方案的验证。与代码不同，规则以较不复杂的语言编写; 业务分析师可以轻松阅读和验证一套规则。

- 逻辑和数据分离  
数据位于“域对象”中，业务逻辑位于“规则”中。根据项目的种类，这种分离是非常有利的。

- 速度和可扩展性  
写入Drools的Rete OO算法已经是一个成熟的算法。在Drools的帮助下，您的应用程序变得非常可扩展。如果频繁更改请求，可以添加新规则，而无需修改现有规则。

- 知识集中化  
通过使用规则，您创建一个可执行的知识库（知识库）。这是商业政策的一个真理点。理想情况下，规则是可读的，它们也可以用作文档。


### rete 算法

Rete 算法最初是由卡内基梅隆大学的 Charles L.Forgy 博士在 1974 年发表的论文中所阐述的算法 , 该算法提供了专家系统的一个高效实现。自 Rete 算法提出以后 , 它就被用到一些大型的规则系统中 , 像 ILog、Jess、JBoss Rules 等都是基于 RETE 算法的规则引擎

Rete 在拉丁语中译为”net”，即网络。Rete 匹配算法是一种进行大量模式集合和大量对象集合间比较的高效方法，通过网络筛选的方法找出所有匹配各个模式的对象和规则。

其核心思想是将分离的匹配项根据内容动态构造匹配树，以达到显著降低计算量的效果。Rete 算法可以被分为两个部分：规则编译和规则执行。当Rete算法进行事实的断言时，包含三个阶段：匹配、选择和执行，称做 match-select-act cycle。

rate算法的详细内容可以参考这篇文章：[开源规则流引擎实践](https://www.ibm.com/developerworks/cn/opensource/os-drools/index.html)

##  Drools 介绍

Drools 是一个基于Charles Forgy's的RETE算法的，易于访问企业策略、易于调整以及易于管理的开源业务规则引擎，符合业内标准，速度快、效率高。
业务分析师人员或审核人员可以利用它轻松查看业务规则，从而检验是否已编码的规则执行了所需的业务规则。

Drools 是用Java语言编写的开放源码规则引擎，使用Rete算法对所编写的规则求值。Drools允许使用声明方式表达业务逻辑。可以使用非XML的本地语言编写规则，从而便于学习和理解。并且，还可以将Java代码直接嵌入到规则文件中，这令Drools的学习更加吸引人。


Drools优点：

- 非常活跃的社区支持
- 易用
- 快速的执行速度
- 在 Java 开发人员中流行
- 与 Java Rule Engine API（JSR 94）兼容

Drools相关概念：

- 事实（Fact）：对象之间及对象属性之间的关系
- 规则（rule）：是由条件和结论构成的推理语句，一般表示为if...Then。一个规则的if部分称为LHS，then部分称为RHS。
- 模式（module）：就是指IF语句的条件。这里IF条件可能是有几个更小的条件组成的大条件。模式就是指的不能在继续分割下去的最小的原子条件。

Drools通过 事实、规则和模式相互组合来完成工作，drools在开源规则引擎中使用率最广，但是在国内企业使用偏少，保险、支付行业使用稍多。

小明看了这么多概念，有点晕，么关系，来一个特别简单的示例帮忙解决小明的问题。

## 解决小明的烦恼

drools有专门的规则语法drl，就是专门描述活动的规则是如何执行的，按照小明的需求规则如下：

Point-rules.drl 文件内容

``` drl
package rules

import com.neo.drools.entity.Order

rule "zero"
    no-loop true
    lock-on-active true
    salience 1
    when
        $s : Order(amout <= 100)
    then
        $s.setScore(0);
        update($s);
end

rule "add100"
    no-loop true
    lock-on-active true
    salience 1
    when
        $s : Order(amout > 100 && amout <= 500)
    then
        $s.setScore(100);
        update($s);
end

rule "add500"
    no-loop true
    lock-on-active true
    salience 1
    when
        $s : Order(amout > 500 && amout <= 1000)
    then
        $s.setScore(500);
        update($s);
end

rule "add1000"
    no-loop true
    lock-on-active true
    salience 1
    when
        $s : Order(amout > 1000)
    then
        $s.setScore(1000);
        update($s);
end    
```

- package 与Java语言类似，drl的头部需要有package和import的声明,package不必和物理路径一致。  
- import 导出java Bean的完整路径，也可以将Java静态方法导入调用。  
- rule 规则名称，需要保持唯一  件,可以无限次执行。
- no-loop 定义当前的规则是否不允许多次循环执行,默认是 false,也就是当前的规则只要满足条件,可以无限次执行。  
- lock-on-active 将lock-on-active属性的值设置为true,可避免因某些Fact对象被修改而使已经执行过的规则再次被激活执行。  
- salience 用来设置规则执行的优先级,salience 属性的值是一个数字,数字越大执行优先级越高, 同时它的值可以是一个负数。默认情况下,规则的 salience 默认值为 0。如果不设置规则的 salience 属性,那么执行顺序是随机的。  
- when 条件语句，就是当到达什么条件的时候  
- then 根据条件的结果，来执行什么动作  
- end 规则结束  

这个规则文件就是描述了，当符合什么条件的时候，应该去做什么事情，每当规则有变动的时候，我们只需要修改规则文件，然后重新加载即可生效。

这里需要有一个配置文件告诉代码规则文件drl在哪里，在drools中这个文件就是kmodule.xml，放置到resources/META-INF目录下。

kmodule.xml内容如下：

``` xml
<?xml version="1.0" encoding="UTF-8"?>
<kmodule xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xmlns="http://www.drools.org/xsd/kmodule">

    <kbase name="point-rulesKB" packages="rules">
        <ksession name="point-rulesKS"/>
    </kbase>

</kmodule>
```

以下对配置说明进行简单说明：

- Kmodule 中可以包含一个到多个 kbase,分别对应 drl 的规则文件。
- Kbase 需要一个唯一的 name,可以取任意字符串。
- packages 为drl文件所在resource目录下的路径。注意区分drl文件中的package与此处的package不一定相同。多个包用逗号分隔。默认情况下会扫描 resources目录下所有(包含子目录)规则文件。  
- kbase的default属性,标示当前KieBase是不是默认的,如果是默认的则不用名称
就可以查找到该 KieBase,但每个 module 最多只能有一个默认 KieBase。
- kbase 下面可以有一个或多个 ksession,ksession 的 name 属性必须设置,且必须唯一。

再看看代码端怎么处理，贴出核心代码

``` java
public static final void main(final String[] args) throws Exception{
    KieServices ks = KieServices.Factory.get();
    KieContainer kc = ks.getKieClasspathContainer();
    execute( kc );
}

public static void execute( KieContainer kc ) throws Exception{
    KieSession ksession = kc.newKieSession("point-rulesKS");
    List<Order> orderList = getInitData();
    for (int i = 0; i < orderList.size(); i++) {
        Order o = orderList.get(i);
        ksession.insert(o);
        ksession.fireAllRules();
        addScore(o);
    }
    ksession.dispose();
}
```

代码解释：首先通过请求获取 KieServices，通过KieServices获取KieContainer，KieContainer加载规则文件并获取KieSession，KieSession来执行规则引擎，KieSession是一个轻量级组建，每次执行完销毁。KieContainer是重量级组建可以考虑复用。

OK 小明的需求，代码部分这样写就行了，完全不用考虑以后的规则变化了。当活动的规则有变化的时候，小明只要修改规则文件Point-rules.drl中下方相关规则内容既可,如果活动规则动态的添加、减少也可以相应的去增加、减少规则文件既可，再也不用去动代码了。

``` drl
rule "xxx"
    no-loop true
    lock-on-active true
    salience 1
    when
        $s : Order(amout > yy)
    then
        $s.setScore(yy);
        update($s);
end  
```
看到这里小明又开始哼起了歌曲。。。

**[文中完整的示例代码](https://github.com/ityouknow/drools-examples)**

> 本篇文章算是对drools的简单介绍，后续文章将详细介绍drools的使用。

参考：  
[专栏：drools规则引擎](http://blog.csdn.net/column/details/16183.html)


