---
layout: post
title: 千里追踪博客之殇
category: other
tags: [other]
---

发生了什么

细心的同学会发现虽然公众号每周还在更新，但是我的博客[www.ityouknow.com](http://www.ityouknow.com/)有一月多都没有更新了。这其中有两个原因，第一呢去了新公司996各种忙乱，没有太多的时间，但最主要的问题是博客更新不了，每次提交都会报错。

我的博客托管在Github上，每次写文章的节奏都是这样子的：在sublime text3上面使用markdown语法来写文章，写完文章之后，使用Github Desktop提交到Github，Github会自动进行构建，这样文章就发布到博客中，然后我再复制文章内容同步到公众号、博客园、CSDN。这次博客突然提交文章报错，导致我写文章的节奏完全被打乱了，为什么会这样呢，这个事还得从头说起。


## 起因

我最开始只是在博客园写文章，虽然博客园的阅读量和用户氛围都很不错，但还是有很多的限制，做为一个博客的爱好者，还是希望有自己的独立博客，考察了很多方案，最后还是觉得Github直接提交代码发布博客的方式最喜欢，并且还完全免费。使用github pages之后，很长的一段时间内都没有发现喜欢的博客主题。有一次查找资料的时候偶然发现了DONGChuan同学的这个博客主题[Yummy-Jekyll](https://github.com/DONGChuan/Yummy-Jekyll)，简洁大方非常符合我的审美观，果断入手。后来又根据自己的情况对博客主题做了一些定制，就成了现在的样子。

博客使用了一年多，期间一直都很稳定，中间做过一次升级，增加了移动端动态适配。一月前，答应给[丑胖侠](http://blog.csdn.net/wo541075754)同学加一个友情连接，按照往常的情况，修改link.md文件添加一条记录然后提交。过了一会发现博客link页面并没有更新过来，反而收到了github自动回复的一封邮件，如下：

``` text
主题：[ityouknow/ityouknow.github.io] Page build failure

内容：
The page build failed for the `master` branch with the following error: 

Page build failed. For more information, see https://help.github.com/articles/troubleshooting-github-pages-builds/.

For information on troubleshooting Jekyll see:

https://help.github.com/articles/troubleshooting-jekyll-builds 

If you have any questions you can contact us by replying to this email.
```

当时正在上班，没有时间细看，就先放了下来，等有空闲了再仔细瞧瞧。

## 设法解决

过了两天刚好得空的时候，就研究下到底是啥原因，想着应该是哪个文件的格式没写对导致报语法错误，于是回退了最近修改的link.md文件，提交上去之后又报同样的错误，于是索性把最近一周提交的文件全都进行回退，提交之后还是报同样的错误，于是我意识到应该不是因为我最近提交文件导致的此问题，仔细的查看了报错的邮件内容，按照邮件中提示的两个网址核对了相关信息，尝试着修改了一些配置，但还是没有解决。于是用我蹩脚的英语就给github官方发了一封邮件：

``` text
Hi:
     I don’t know why page build failure,I just modified a MD file, and now the page cannot be submitted again。

     Can you tell me the reason,Thank you for your reply.
```

第二天就收到了Github官方的回复邮件：

``` text
Hi ityouknow,
Here's the full error we're seeing:

[31m  Liquid Exception: no implicit conversion of Integer into String in /_layouts/default.html[0m
[31m             Fatal: TypeError[0m
[31m                    no implicit conversion of Integer into String[0m
You can also find this by building your site locally with Jekyll:

https://help.github.com/articles/setting-up-your-github-pages-site-locally-with-jekyll/

I notice in your Gemfile you're using some outdated dependancies that may be causing the Pages build process to fail. You may want to follow the instructions above, and make sure you're running the same versions of each dependancy listed on this page:

https://pages.github.com/versions/
Hope this helps!

Thanks,
Thomas
```

邮件内容一方面把具体的报错信息帮我贴了出来，一方面说我的Gemfile文件中有一些组件版本过低，可能会导致这方面的原因，Github Page使用打包的相关组件版本在这里：[https://pages.github.com/versions](https://pages.github.com/versions)。我试着按照这个网址的内容修改Gemfile.lock里面的相关组件版本后，再次进行了提交，结果仍然是报这个错误，再次陷入了死胡同中。

过了两天我突然想到，Yummy-Jekyll主题的作者会不会也遇到了这个问题，于是到作者的Github主页是fork了她的博客相关代码，在我的Github账户下面进行了测试，也报同样的错误，接着又试着将作者Gemfile的相关内容覆盖我的博客相对应的文件中，结果还是报错，于是我就在Yummy-Jekyll主题下创建了一个issues，将问题描述了一下，希望作者能给帮忙解决掉，同时根据作者在github留下的邮箱，同步发送了一封邮件。

``` text
Hi 您好：

首先非常感谢你开源这个主题，我使用了你的主题做了博客：www.ityouknow.com。最近提交的时候总是报错，我给Github官方发送了邮件，回复说有可能是组件依赖过低的问题，我自己对前端来说是小白，请求给予帮忙，谢谢。

可以有偿帮助，我的微信/QQ:xxxxx.
```

过了一周，可能作者没有注意到github提交的issues和我的邮件，然后我再次发送了邮件给作者，仍然没有收到回复。于是我想使用这个主题的博主应该也不只我一个，会不会他们也遇到了同样的问题，有的可能有能力解决了此问题。在Github上面查看了Yummy-Jekyll主题的所有fork记录，查看了很多的博主，大多都仅仅是停留在fork没动过，或者写了一两篇后就停止了，这个方向又陷入了死胡同。

又过了几天想着自己好好研究下前端和Gemfile兴许可以解决掉，于是我将博客代码在coding.net复制了一份[ityouknow](https://coding.net/u/ityouknow/p/ityouknow/git)，因为使用coding.net在打包的时候可以查看日志，如果报错可以看到具体的错误信息。于是我就一边试着修改相关代码和配置，一边不断的重新部署查看错误日志，再根据错误日志在谷歌上搜索相关的解决方案，这个过程持续了大概两个半天，终究还是没有解决，前端对我来说仍然像谜一样。

## 出现转机

求助主题作者和自力更生都无果之后，就想着找一些对jekyll和前端比较熟悉的大牛，帮我看看如何去解决。在QQ群中发了一些求助信息后，也没有找到合适的对象，于是就想到了[v2ex](https://www.v2ex.com/)，以前总听说v2ex是一个神奇的社区，但我完全不明白神奇在哪里，以前也使用过一两次，也么看出个所以然。当然我还是抱着死马当作活马医的态度在v2ex发了一个帖子：

<div align="center">
  <img src="http://www.ityouknow.com/assets/images/2017/v2ex.png">
</div>

不一会，就收到了一个网友的回复："上班中，现在没时间帮你验证， 你把 readme 删掉试试是否 ok"，虽然我明明知道这个建议是多么的不靠谱，但我还是试了，仍然报错。突然在v2ex上有一个叫做"lzhr"的小伙伴给我回复了这么一条信息：

``` text
这个错误好像持续一段时间了，/DONGChuan/Yummy-Jekyll/issues/40 。 

要不换个很近似的：/smartjinyu?tab=repositories
```

跟着里面的链接我找到了这个地址：[https://github.com/smartjinyu/smartjinyu.github.io](https://github.com/smartjinyu/smartjinyu.github.io)，这个哪是近似，就是和我使用了同一个模板主题。作者也是在原来的模板上进行了一些改造，赶紧瞄了一下Gemfile.lock的最新修改时间，是14天前貌似有戏，于是我迅速复制了一份代码在coding.net上面进行了测试，但仍然还是报错，感觉很奇怪给"lzhr"回复了还是不行，不一会"lzhr"又给我回复了信息："不是啊，我直接 fork，改改地址就行了 [https://github.com/RGXY/rgxy.github.io](https://github.com/RGXY/rgxy.github.io)"，于是我想是不是coding.net和github的打包环境不一致导致的，于是fork了smartjinyu作者的代码在github上面进行了测试，果然可以！

就在周五的晚上，终于看到了胜利的曙光。使用对比工具"Beyond Compare"将原来我的博客和smartjinyu的博客进行了一一对比。不断的改动、提交、查看报错，持续了一个多小时之后，发现这样效率太低了，于是转变了思路，直接在smartjinyu的博客上面进行修改定制，花费了两个多小时，终于将smartjinyu的博客修改成和我原先博客一模一样，然后再同步上博客内容，提交上去做了测试，都非常成功，完了一看时间已经凌晨3点了，但终究是搞定了一件事情。

在对照改造的过程中，我发现smartjinyu将依赖的组件包都相应的做了升级，以前很多的模板写法到现在的环境已经不通过编译。问题的本质应该是Github官方升级了相关的打包环境，导致博客中有一些写法和组件包不兼容。虽然最后修改的版本在Github上已经没有问题了，但我复制到了coding.net上面进行打包测试还是报错，有机会的话哪位对Jekyll熟悉的朋友可以一起看看，最后再次感谢v2ex的[lzhr](https://www.v2ex.com/member/lzhr)。

