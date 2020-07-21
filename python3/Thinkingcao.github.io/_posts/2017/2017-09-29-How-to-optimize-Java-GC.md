---
layout: post
title: jvm 系列(九):如何优化 Java GC 「译」
category: jvm
tags: [jvm]
---

本文由[CrowHawk](https://crowhawk.github.io/)翻译，地址：[如何优化Java GC「译」](https://crowhawk.github.io/2017/08/21/jvm_4/)，是Java GC调优的经典佳作。

Sangmin Lee发表在[Cubrid](http://www.cubrid.org/blog)上的"Become a Java GC Expert"系列文章的第三篇[《How to Tune Java Garbage Collection》](http://www.cubrid.org/blog/how-to-tune-java-garbage-collection),本文的作者是韩国人，写在JDK 1.8发布之前，虽然有些地方有些许过时，但整体内容还是非常有价值的。译者此前也看到有人翻译了本文，发现其中有许多错漏生硬和语焉不详之处，因此决定自己翻译一份，供大家分享。

本文是“成为Java GC专家”系列文章的第三篇，在系列的第一篇文章[《理解Java GC》](http://www.cubrid.org/blog/understanding-java-garbage-collection)中，我们了解到了不同GC算法的执行过程、GC的工作原理、新生代和老年代的概念、JDK 7中你需要了解的5种GC类型以及每一种GC对性能的影响。

在系列的第二篇文章[《如何监控Java GC》](http://www.cubrid.org/blog/how-to-monitor-java-garbage-collection)中笔者已经解释了JVM进行实时GC的原理、监控GC的方法以及可以使这一过程更加迅速高效的工具。

在第三篇文章中，笔者将基于实际生产环境中的案例，介绍几个GC优化的最佳参数设置。在此我们假设你已经理解了本系列前两篇文章的内容，因此为了更深入的理解本文所讲内容，我建议你在阅读本篇文章之前先仔细阅读这两篇文章。

## GC优化是必要的吗？

或者更准确地说，GC优化对Java基础服务来说是必要的吗？答案是否定的，事实上GC优化对Java基础服务来说在有些场合是可以省去的，但前提是这些正在运行的Java系统，必须包含以下参数或行为：
+ 内存大小已经通过**-Xms**和**-Xmx**参数指定过
+ 运行在server模式下（使用**-server**参数）
+ 系统中没有残留超时日志之类的错误日志

换句话说，如果你在运行时没有手动设置内存大小并且打印出了过多的超时日志，那你就需要对系统进行GC优化。

不过你需要时刻谨记一句话：**GC tuning is the last task to be done.**

现在来想一想GC优化的最根本原因，垃圾收集器的工作就是清除Java创建的对象，垃圾收集器需要清理的对象数量以及要执行的GC数量均取决于已创建的对象数量。因此，为了使你的系统在GC上表现良好，首先需要减少创建对象的数量。

俗话说“冰冻三尺非一日之寒”，我们在编码时要首先要把下面这些小细节做好，否则一些琐碎的不良代码累积起来将让GC的工作变得繁重而难于管理：

+ 使用`StringBuilder`或`StringBuffer`来代替`String`
+ 尽量少输出日志

尽管如此，仍然会有我们束手无策的情况。XML和JSON解析过程往往占用了最多的内存，即使我们已经尽可能地少用String、少输出日志，仍然会有大量的临时内存（大约10-100MB）被用来解析XML或JSON文件，但我们又很难弃用XML和JSON。在此，你只需要知道这一过程会占据大量内存即可。

如果在经过几次重复的优化后应用程序的内存用量情况有所改善，那么久可以启动GC优化了。

笔者总结了GC优化的两个目的：
1. **将进入老年代的对象数量降到最低**
2. **减少Full GC的执行时间**

## 将进入老年代的对象数量降到最低

除了可以在JDK 7及更高版本中使用的G1收集器以外，其他分代GC都是由Oracle JVM提供的。关于分代GC，就是对象在Eden区被创建，随后被转移到Survivor区，在此之后剩余的对象会被转入老年代。也有一些对象由于占用内存过大，在Eden区被创建后会直接被传入老年代。老年代GC相对来说会比新生代GC更耗时，因此，减少进入老年代的对象数量可以显著降低Full GC的频率。你可能会以为减少进入老年代的对象数量意味着把它们留在新生代，事实正好相反，新生代内存的大小是可以调节的。

## 降低Full GC的时间

Full GC的执行时间比Minor GC要长很多，因此，如果在Full GC上花费过多的时间（超过1s），将可能出现超时错误。
+ 如果**通过减小老年代内存来减少Full GC时间**，可能会引起`OutOfMemoryError`或者导致Full GC的频率升高。
+ 另外，如果**通过增加老年代内存来降低Full GC的频率**，Full GC的时间可能因此增加。

因此，**你需要把老年代的大小设置成一个“合适”的值**。

## 影响GC性能的参数

正如我在系列的第一篇文章[《理解Java GC》](http://www.cubrid.org/blog/understanding-java-garbage-collection)末尾提到的，不要幻想着“如果有人用他设置的GC参数获取了不错的性能，我们为什么不复制他的参数设置呢？”，因为对于不用的Web服务，它们创建的对象大小和生命周期都不相同。

举一个简单的例子，如果一个任务的执行条件是A，B，C，D和E，另一个完全相同的任务执行条件只有A和B，那么哪一个任务执行速度更快呢？作为常识来讲，答案很明显是后者。

Java GC参数的设置也是这个道理，设置好几个参数并不会提升GC执行的速度，反而会使它变得更慢。**GC优化的基本原则**是将不同的GC参数应用到两个及以上的服务器上然后比较它们的性能，然后将那些被证明可以提高性能或减少GC执行时间的参数应用于最终的工作服务器上。

下面这张表展示了与内存大小相关且会影响GC性能的GC参数

<center><strong>表1：GC优化需要考虑的JVM参数</strong></center>

|**类型**|**参数**|**描述**|
|:----|:----|:----|
|堆内存大小|`-Xms`|启动JVM时堆内存的大小|
||`-Xmx`|堆内存最大限制|
|新生代空间大小|`-XX:NewRatio`|新生代和老年代的内存比|
||`-XX:NewSize`|新生代内存大小|
||`-XX:SurvivorRatio`|Eden区和Survivor区的内存比|

笔者在进行GC优化时最常用的参数是`-Xms`,`-Xmx`和`-XX:NewRatio`。`-Xms`和`-Xmx`参数通常是必须的，所以`NewRatio`的值将对GC性能产生重要的影响。

有些人可能会问**如何设置永久代内存大小**，你可以用`-XX:PermSize`和`-XX:MaxPermSize`参数来进行设置，但是要记住，只有当出现`OutOfMemoryError`错误时你才需要去设置永久代内存。

还有一个会影响GC性能的因素是[垃圾收集器的类型](https://crowhawk.github.io/2017/08/15/jvm_3/),下表展示了关于GC类型的可选参数（基于JDK 6.0）：

<center><strong>表2：GC类型可选参数</strong></center>

|**GC类型**|**参数**|**备注**|
|:----|:----|:----|
|Serial GC|-XX:+UseSerialGC|
|Parallel GC|-XX:+UseParallelGC</br>-XX:ParallelGCThreads=value|
|Parallel Compacting GC|-XX:+UseParallelOldGC|
|CMS GC|-XX:+UseConcMarkSweepGC</br>-XX:+UseParNewGC</br>-XX:+CMSParallelRemarkEnabled</br>-XX:CMSInitiatingOccupancyFraction=value</br>-XX:+UseCMSInitiatingOccupancyOnly|
|G1|-XX:+UnlockExperimentalVMOptions</br>-XX:+UseG1GC|在JDK 6中这两个参数必须配合使用|

除了G1收集器外，可以通过设置上表中每种类型第一行的参数来切换GC类型，最常见的非侵入式GC就是Serial GC，它针对客户端系统进行了特别的优化。

会影响GC性能的参数还有很多，但是上述的参数会带来最显著的效果，请切记，设置太多的参数并不一定会提升GC的性能。

## GC优化的过程

GC优化的过程和大多数常见的提升性能的过程相似，下面是笔者使用的流程：

### 1.监控GC状态

你需要监控GC从而检查系统中运行的GC的各种状态，具体方法请查看系列的第二篇文章[《如何监控Java GC》](http://www.cubrid.org/blog/how-to-monitor-java-garbage-collection)

### 2.分析监控结果后决定是否需要优化GC

在检查GC状态后，你需要分析监控结构并决定是否需要进行GC优化。如果分析结果显示运行GC的时间只有0.1-0.3秒，那么就不需要把时间浪费在GC优化上，但如果运行GC的时间达到1-3秒，甚至大于10秒，那么GC优化将是很有必要的。

但是，如果你已经分配了大约10GB内存给Java，并且这些内存无法省下，那么就无法进行GC优化了。在进行GC优化之前，你需要考虑为什么你需要分配这么大的内存空间，如果你分配了1GB或2GB大小的内存并且出现了`OutOfMemoryError`，那你就应该执行**堆转储（heap dump）**来消除导致异常的原因。

> 注意：

> **堆转储（heap dump）**是一个用来检查Java内存中的对象和数据的内存文件。该文件可以通过执行JDK中的`jmap`命令来创建。在创建文件的过程中，所有Java程序都将暂停，因此，不要再系统执行过程中创建该文件。

> 你可以在互联网上搜索heap dump的详细说明。对于韩国读者，可以直接参考我去年发布的书：[《The story of troubleshooting for Java developers and system operators》](http://book.naver.com/bookdb/book_detail.nhn?bid=6654751) (Sangmin Lee, Hanbit Media, 2011, 416 pages)

### 3.设置GC类型/内存大小

如果你决定要进行GC优化，那么你需要选择一个GC类型并且为它设置内存大小。此时如果你有多个服务器，请如上文提到的那样，在每台机器上设置不同的GC参数并分析它们的区别。

### 4.分析结果


在设置完GC参数后就可以开始收集数据，请在收集至少24小时后再进行结果分析。如果你足够幸运，你可能会找到系统的最佳GC参数。如若不然，你还需要分析输出日志并检查分配的内存，然后需要通过不断调整GC类型/内存大小来找到系统的最佳参数。

### 5.如果结果令人满意，将参数应用到所有服务器上并结束GC优化

如果GC优化的结果令人满意，就可以将参数应用到所有服务器上，并停止GC优化。

在下面的章节中，你将会看到上述每一步所做的具体工作。

## 监控GC状态并分析结果

在运行中的Web应用服务器（Web Application Server,WAS）上查看GC状态的最佳方式就是使用`jstat`命令。笔者在[《如何监控Java GC》](http://www.cubrid.org/blog/how-to-monitor-java-garbage-collection)中已经介绍过了`jstat`命令，所以在本篇文章中我将着重关注数据部分。

下面的例子展示了某个还没有执行GC优化的JVM的状态（虽然它并不是运行服务器）。

```
$ jstat -gcutil 21719 1s
S0    S1    E    O    P    YGC    YGCT    FGC    FGCT GCT
48.66 0.00 48.10 49.70 77.45 3428 172.623 3 59.050 231.673
48.66 0.00 48.10 49.70 77.45 3428 172.623 3 59.050 231.673
```

我们先看一下YGC（从应用程序启动到采样时发生 Young GC 的次数）和YGCT（从应用程序启动到采样时 Young GC 所用的时间(秒)），计算YGCT/YGC会得出，平均每次新生代的GC耗时50ms，这是一个很小的数字，通过这个结果可以看出，我们大可不必关注新生代GC对GC性能的影响。

现在来看一下FGC（	从应用程序启动到采样时发生 Full GC 的次数）和FGCT（从应用程序启动到采样时 Full GC 所用的时间(秒)），计算FGCT/FGC会得出，平均每次老年代的GC耗时19.68s。有可能是执行了三次Full GC，每次耗时19.68s，也有可能是有两次只花了1s,另一次花了58s。不管是哪一种情况，GC优化都是很有必要的。

使用`jstat`命令可以很容易地查看GC状态，但是分析GC的最佳方式是加上`-verbosegc`参数来生成日志。在之前的文章中笔者已经解释了如何分析这些日志。**HPJMeter**是笔者最喜欢的用于分析`-verbosegc`生成的日志的工具，它简单易用，使用HPJmeter可以很容易地查看GC执行时间以及GC发生频率。

此外，如果GC执行时间满足下列所有条件，就没有必要进行GC优化了：
+ Minor GC执行非常迅速（50ms以内）
+ Minor GC没有频繁执行（大约10s执行一次）
+ Full GC执行非常迅速（1s以内）
+ Full GC没有频繁执行（大约10min执行一次）

括号中的数字并不是绝对的，它们也随着服务的状态而变化。有些服务可能要求一次Full GC在0.9s以内，而有些则会放得更宽一些。因此，对于不同的服务，需要按照不同的标准考虑是否需要执行GC优化。

当检查GC状态时，不能只查看Minor GC和Full GC的时间，还必须要**关注GC执行的次数**。如果新生代空间太小，Minor GC将会非常频繁地执行（有时每秒会执行一次，甚至更多）。此外，传入老年代的对象数目会上升，从而导致Full GC的频率升高。因此，在执行`jstat`命令时，请使用`-gccapacity`参数来查看具体占用了多少空间。

## 设置GC类型/内存大小

### 设置GC类型

Oracle JVM有5种垃圾收集器，但是在JDK 7以前的版本中，你只能在Parallel GC, Parallel Compacting GC 和CMS GC之中选择，至于具体选择哪个，则没有具体的原则和规则。

既然这样的话，**我们如何来选择GC呢？**最好的方法是把三种都用上，但是有一点必须明确——CMS GC通常比其他并行（Parallel）GC都要快（这是因为CMS GC是并发的GC），如果确实如此，那只选择CMS GC就可以了，不过CMS GC也不总是更快，当出现**concurrent mode failure**时，CMS GC就会比并行GC更慢了。

<big>**Concurrent mode failure**</big>

现在让我们来深入地了解一下**concurrent mode failure**。

并行GC和CMS GC的最大区别是并行GC采用“标记-整理”(Mark-Compact)算法而CMS GC采用“标记-清除”(Mark-Sweep)算法（具体内容可参照译者的文章[《GC算法与内存分配策略》](https://crowhawk.github.io/2017/08/10/jvm_2/)）,compact步骤就是通过移动内存来消除内存碎片，从而消除分配的内存之间的空白区域。

对于并行GC来说，无论何时执行Full GC，都会进行compact工作，这消耗了太多的时间。不过在执行完Full GC后，下次内存分配将会变得更快（因为直接顺序分配相邻的内存）。

相反，CMS GC没有compact的过程，因此CMS GC运行的速度更快。但是也是由于没有整理内存，在进行磁盘清理之前，内存中会有很多零碎的空白区域，这也导致没有足够的空间分配给大对象。例如，在老年代还有300MB可用空间，但是连一个10MB的对象都没有办法被顺序存储在老年代中，在这种情况下，会报出**“concurrent mode failure”**的warning，然后系统执行compact操作。但是CMS GC在这种情况下执行的compact操作耗时要比并行GC高很多，并且这还会导致另一个问题，关于**“concurrent mode failure”**的详细说明，可用参考Oracle工程师撰写的[《Understanding CMS GC Logs》](https://blogs.oracle.com/poonam/understanding-cms-gc-logs)。

综上所述，你需要根据你的系统情况为其选择一个最适合的GC类型。

每个系统都有最适合它的GC类型等着你去寻找，如果你有6台服务器，我建议你每两个服务器设置相同的参数，然后加上`-verbosegc`参数再分析结果。

### 设置内存大小

下面展示了内存大小、GC运行次数和GC运行时间之间的关系：

**大内存空间**
+ 减少了GC的次数
+ 提高了GC的运行时间

**小内存空间**
+ 增多了GC的次数
+ 降低了GC的运行时间

关于如何设置内存的大小，没有一个标准答案，如果服务器资源充足并且Full GC能在1s内完成，把内存设为10GB也是可以的，但是大部分服务器并不处在这种状态中，当内存设为10GB时，Full GC会耗时10-30s,具体的时间自然与对象的大小有关。

既然如此，**我们该如何设置内存大小呢？**通常我推荐设为500MB，这不是说你要通过`-Xms500m`和`-Xmx500m`参数来设置WAS内存。根据GC优化之前的状态，如果Full GC后还剩余300MB的空间，那么把内存设为1GB是一个不错的选择（300MB（默认程序占用）+ 500MB（老年代最小空间）+200MB（空闲内存））。这意味着你需要为老年代设置至少500MB空间，因此如果你有三个运行服务器，可以把它们的内存分别设置为1GB，1.5GB，2GB，然后检查结果。

理论上来说，GC执行速度应该遵循1GB> 1.5GB> 2GB，1GB内存时GC执行速度最快。然而，理论上的1GB内存Full GC消耗1s、2GB内存Full GC消耗2 s在现实里是无法保证的，实际的运行时间还依赖于服务器的性能和对象大小。因此，最好的方法是创建尽可能多的测量数据并监控它们。

在设置内存空间大小时，你还需要设置一个参数：`NewRatio`。`NewRatio`的值是新生代和老年代空间大小的比例。如果`XX:NewRatio=1`，则新生代空间:老年代空间=1:1，如果堆内存为1GB，则新生代:老年代=500MB:500MB。如果`NewRatio`等于2，则新生代:老年代=1:2，因此，`NewRatio`的值设置得越大，则老年代空间越大，新生代空间越小。

你可能会认为把`NewRatio`设为1会是最好的选择，然而事实并非如此，根据笔者的经验，当`NewRatio`设为2或3时，整个GC的状态表现得更好。

**完成GC优化最快地方法是什么？**答案是比较性能测试的结果。为了给每台服务器设置不同的参数并监控它们，最好查看的是一或两天后的数据。当通过性能测试来进行GC优化时，你需要在不同的测试时保证它们有相同的负载和运行环境。然而，即使是专业的性能测试人员，想精确地控制负载也很困难，并且需要大量的时间准备。因此，更加方便容易的方式是直接设置参数来运行，然后等待运行的结果（即使这需要消耗更多的时间）。

## 分析GC优化的结果

在设置了GC参数和`-verbosegc`参数后，可以使用tail命令确保日志被正确地生成。如果参数设置得不正确或日志未生成，那你的时间就被白白浪费了。如果日志收集没有问题的话，在收集一或两天数据后再检查结果。最简单的方法是把日志从服务器移到你的本地PC上，然后用**HPJMeter**分析数据。

在分析结果时，请关注下列几点（这个优先级是笔者根据自己的经验拟定的，我认为选取GC参数时应考虑的最重要的因素是Full GC的运行时间。）：
+ 单次Full GC运行时间
+ 单次Minor GC运行时间
+ Full GC运行间隔
+ Minor GC运行间隔
+ 整个Full GC的时间
+ 整个Minor GC的运行时间
+ 整个GC的运行时间
+ Full GC的执行次数
+ Minor GC的执行次数

找到最佳的GC参数是件非常幸运的，然而在大多数时候，我们并不会如此幸运，在进行GC优化时一定要小心谨慎，因为当你试图一次完成所有的优化工作时，可能会出现`OutOfMemoryError`错误。

## 优化案例

到目前为止，我们一直在从理论上介绍GC优化，现在是时候将这些理论付诸实践了，我们将通过几个例子来更深入地理解GC优化。

### 示例1

下面这个例子是针对**Service S**的优化，对于最近刚开发出来的Service S，执行Full GC需要消耗过多的时间。

现在看一下执行`jstat -gcutil`的结果

```
S0 S1 E O P YGC YGCT FGC FGCT GCT
12.16 0.00 5.18 63.78 20.32 54 2.047 5 6.946 8.993
```

左边的Perm区的值对于最初的GC优化并不重要，而YGC参数的值更加对于这次优化更为重要。

平均执行一次Minor GC和Full GC消耗的时间如下表所示：

<center><strong>表3：Service S的Minor GC 和Full GC的平均执行时间</strong></center>

|**GC类型**|**GC执行次数**|GC执行时间|平均值|
|:---|:---|:---|:---|
|Minor GC|54|2.047s|37ms|
|Full GC|5|6.946s|1.389s|

**37ms**对于Minor GC来说还不赖，但1.389s对于Full GC来说意味着当GC发生在数据库Timeout设置为1s的系统中时，可能会频繁出现超时现象。

首先，你需要检查开始GC优化前内存的使用情况。使用`jstat -gccapacity`命令可以检查内存用量情况。在笔者的服务器上查看到的结果如下：

```
NGCMN NGCMX NGC S0C S1C EC OGCMN OGCMX OGC OC PGCMN PGCMX PGC PC YGC FGC
212992.0 212992.0 212992.0 21248.0 21248.0 170496.0 1884160.0 1884160.0 1884160.0 1884160.0 262144.0 262144.0 262144.0 262144.0 54 5
```

其中的关键值如下：
+ 新生代内存用量：212,992 KB
+ 老年代内存用量：1,884,160 KB

因此，除了永久代以外，被分配的内存空间加起来有2GB，并且新生代：老年代=1：9，为了得到比使用`jstat`更细致的结果，还需加上`-verbosegc`参数获取日志，并把三台服务器按照如下方式设置（除此以外没有使用任何其他参数）：
+ NewRatio=2
+ NewRatio=3
+ NewRatio=4

一天后我得到了系统的GC log，幸运的是，在设置完NewRatio后系统没有发生任何Full GC。

**这是为什么呢？**这是因为大部分对象在创建后很快就被回收了，所有这些对象没有被传入老年代，而是在新生代就被销毁回收了。

在这样的情况下，就没有必要去改变其他的参数值了，只要选择一个最合适的`NewRatio`值即可。那么，**如何确定最佳的NewRatio值呢？**为此，我们分析一下每种`NewRatio`值下Minor GC的平均响应时间。

在每种参数下Minor GC的平均响应时间如下：
+ NewRatio=2：45ms
+ NewRatio=3：34ms
+ NewRatio=4：30ms

我们可以根据GC时间的长短得出NewRatio=4是最佳的参数值（尽管NewRatio=4时新生代空间是最小的）。在设置完GC参数后，服务器没有发生Full GC。

为了说明这个问题，下面是服务执行一段时间后执行`jstat –gcutil`的结果:

```
S0 S1 E O P YGC YGCT FGC FGCT GCT
8.61 0.00 30.67 24.62 22.38 2424 30.219 0 0.000 30.219
```

你可能会认为是服务器接收的请求少才使得GC发生的频率较低，实际上，虽然Full GC没有执行过，但Minor GC被执行了2424次。

### 示例2

这是一个Service A的例子。我们通过公司内部的应用性能管理系统（APM）发现JVM暂停了相当长的时间（超过8秒），因此我们进行了GC优化。我们努力寻找JVM暂停的原因，后来发现是因为Full GC执行时间过长，因此我们决定进行GC优化。

在GC优化的开始阶段，我们加上了`-verbosegc`参数，结果如下图所示：

<center><img src="https://pic.yupoo.com/crowhawk/ebb4b181/a24f4e9b.png"></center>

<center><strong>图1：进行GC优化之前STW的时间</strong></center>

上图是由HPJMeter生成的图片之一。横坐标表示JVM执行的时间，纵坐标表示每次GC的时间。CMS为绿点，表示Full GC的结果，而Parallel Scavenge为蓝点，表示Minor GC的结果。

之前我说过CMS GC是最快的GC，但是上面的结果显示在一些时候CMS耗时达到了15s。**是什么导致了这一结果？**请记住我之前说的：CMS在执行compact（整理）操作时会显著变慢。此外，服务的内存通过`-Xms1g`和`=Xmx4g`设置了，而分配的内存只有4GB。

因此笔者将GC类型从CMS GC改为了Parallel GC，把内存大小设为2GB，并把`NewRatio`设为3。在执行`jstat -gcutil`几小时后的结果如下：

```
S0 S1 E O P YGC YGCT FGC FGCT GCT
0.00 30.48 3.31 26.54 37.01 226 11.131 4 11.758 22.890
```

Full GC的时间缩短了，变成了每次3s，跟15s比有了显著提升。但是3s依然不够快，为此笔者创建了以下6种情况：
+ Case 1: `-XX:+UseParallelGC -Xms1536m -Xmx1536m -XX:NewRatio=2`
+ Case 2: `-XX:+UseParallelGC -Xms1536m -Xmx1536m -XX:NewRatio=3`
+ Case 3: `-XX:+UseParallelGC -Xms1g -Xmx1g -XX:NewRatio=3`
+ Case 4: `-XX:+UseParallelOldGC -Xms1536m -Xmx1536m -XX:NewRatio=2`
+ Case 5: `-XX:+UseParallelOldGC -Xms1536m -Xmx1536m -XX:NewRatio=3`
+ Case 6: `-XX:+UseParallelOldGC -Xms1g -Xmx1g -XX:NewRatio=3`

**上面哪一种情况最快？**结果显示，内存空间越小，运行结果最少。下图展示了性能最好的Case 6的结果图，它的最慢响应时间只有1.7s，并且响应时间的平均值已经被控制到了1s以内。

<center><img src="https://pic.yupoo.com/crowhawk/026cb5ec/dd3bdbb9.png"></center>

<center><strong>图2：Case 6的持续时间图</strong></center>

基于上图的结果，按照Case 6调整了GC参数，但这却导致每晚都会发生`OutOfMemoryError`。很难解释发生异常的具体原因，简单地说，应该是批处理程序导致了内存泄漏，我们正在解决相关的问题。

如果只对GC日志做一些短时间的分析就将相关参数部署到所有服务器上来执行GC优化，这将是非常危险的。切记，只有当你同时仔细分析服务的执行情况和GC日志后，才能保证GC优化没有错误地执行。

在上文中，我们通过两个GC优化的例子来说明了GC优化是怎样执行的。正如上文中提到的，例子中设置的GC参数可以设置在相同的服务器之上，但前提是他们具有相同的CPU、操作系统、JDK版本并且运行着相同的服务。此外，不要把我使用的参数照搬到你的应用上，它们可能在你的机器上并不能起到同样良好的效果。

## 总结

笔者没有执行heap dump并分析内存的详细内容，而是通过自己的经验进行GC优化。精确地分析内存可以得到更好的优化效果，不过这种分析一般只适用于内存使用量相对固定的场景。如果服务严重过载并占有了大量的内存，则建议你根据之前的经验进行GC优化。

笔者已经在一些服务上设置了G1 GC参数并进行了性能测试，但还没有应用于正式的生产环境。G1 GC的速度快于任何其他的GC类型，但是你必须要升级到JDK 7。此外，暂时还无法保证它的稳定性，没有人知道运行时是否会出现致命的错误，因此G1 
GC暂时还不适合投入应用。

等未来JDK 7真正稳定了（这并不是说它现在不稳定），并且WAS针对JDK 7进行优化后，G1 GC最终能按照预期的那样来工作，等到那一天我们可能就不再需要GC优化了。

想了解关于GC优化的更多细节，请前往[Slideshare.com](https://www.slideshare.net/) 查看相关资料。强烈推荐[Everything I Ever Learned About JVM Performance Tuning @Twitter](https://www.slideshare.net/aszegedi/everything-i-ever-learned-about-jvm-performance-tuning-twitter),作者是Attila Szegedi, 一名Twitter工程师，请花些时间好好阅读它。
