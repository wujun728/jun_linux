---
layout:     post
title:      技术人如何搭建自己的技术博客
no-post-nav: true
category: other
tags: [other]
excerpt: 每个程序员都想拥有一个博客
---

上次有人留言说，技术博客是程序员的标配，但据我所知绝大部分技术同学到现在仍然没有自己的技术博客。原因有很多，有的是懒的写，有的是怕写不好，还有的是一直想憋个大招，幻想做到完美再发出来，结果一直胎死腹中。但其实更多程序员是不知道如何去搭建一个博客，其实如今搭建一个个人技术博客非常简单，其中最简单搭建方式莫属使用 GitHub Pages + Jekyll 了，我的博客就是使用这种技术。

## GitHub Pages

Github Pages 是面向用户、组织和项目开放的公共静态页面搭建托管服务，站点可以被免费托管在 Github 上，你可以选择使用 Github Pages 默认提供的域名 github.io 或者自定义域名来发布站点。Github Pages 支持 自动利用 Jekyll 生成站点，也同样支持纯 HTML 文档，将你的 Jekyll 站点托管在 Github Pages 上是一个不错的选择。

使用 Github Pages 搭建博客有以下几个优点：

- 完全免费，其中服务器、流量、域名什么的都管，完全零费用搭建一个技术博客
- 写博客就是提交代码，让写作和编程的体验保持一致
- 支持绑定自己的域名
- 提供流行的网页主题模板

缺点也是有的：

- 不支持动态内容，博客必须都是静态网页，一般会使用 Jekyll 来构建内容。
- 博客不能被百度索引，因 Github 和百度有过节，所以 Github 就把百度给屏蔽了。
- 仓库空间不大于1G
- 每个月的流量不超过100G
- 每小时更新不超过 10 次


Github Pages 使用 Jekyll 来构建内容，那么 Jekyll 是什么呢？

**Jekyll 介绍**

Jekyll 是一个简单的博客形态的静态站点生产机器。它有一个模版目录，其中包含原始文本格式的文档，通过一个转换器（如 Markdown）和我们的 Liquid 渲染器转化成一个完整的可发布的静态网站，你可以发布在任何你喜爱的服务器上。Jekyll 也可以运行在 GitHub Page 上，也就是说，你可以使用 GitHub 的服务来搭建你的项目页面、博客或者网站，而且是完全免费的。

但如果我们只是在 GitHub 上面使用的话，到不需要知道 Jekyll 的语法，一般 Github 会自动将我们写的 Markdown  文件转换成静态页面。使用 Jekyll 需要使用 Markdown 语法来写你的文章，不过 Markdown 语法非常简单，做为程序员来讲基本上两三天就掌握了，大家也可以参考这篇文章：[markdown 使用总结](http://www.ityouknow.com/other/2015/10/18/markdown-summary.html)。

给大家分享一些 Jekyll 主题，这个网站下有很多 [http://jekyllthemes.org/](http://jekyllthemes.org/) 主题，大家可以根据自己的爱好去选择博客主题。

## 我的个人博客

我的博客经过了三个阶段，第一个阶段，完全依托于使用 GitHub Pages 来构建；第二个阶段，将博客托管于国外的一个服务商；第三个阶段，服务器迁移回到国内、域名备案。之前也写过几篇关于技术博客的文章，如下：

- [千里追踪博客之殇](http://www.ityouknow.com/other/2017/09/10/blog-stop-a-month.html)
- [历时25天，我的博客（www.ityouknow.com）终于又活了过来](http://www.ityouknow.com/life/2018/06/10/my-blog-back.html)
- [技术博客那些事儿](http://www.ityouknow.com/other/2017/07/16/operating-technology-blog.html)

使用 Github Pages + Jekyll 构建一个技术博客很简单，基本上步骤就是网上找一个自己喜欢的主题，直接 Fork 到自己的 Github ，然后在删掉原博客中的内容，在上传自己的文章即可，以我自己的博客为例。

我的博客最初使用的是[Yummy-Jekyll](https://github.com/DONGChuan/Yummy-Jekyll)，但这个主题已经尽两年多都没有更新了。因此后期我在这个主题的基础上做了一些改动，其中有依赖组件的更新，结合个人情况对个别页面进行了改版，就成为了现在的样子：

![](http://www.itmind.net/assets/images/2018/it/blog1.png)

使用这个主题的原因是，我比较喜欢简洁大气的风格，并且此博客主题对代码展示支持良好。

## 快速构建一个博客

以我的博客为例，介绍如何最快搭建一个博客。这也是我博客经历的第一个阶段。

1、首先打开地址[https://github.com/ityouknow/ityouknow.github.io](https://github.com/ityouknow/ityouknow.github.io)，点击 Fork 按钮将代码复制一份到自己的仓库。

![](http://www.itmind.net/assets/images/2018/it/blog8.png)

过上一分钟，你的 github 仓库发现一个 ityouknow.github.io 项目。

2、删除 CNAME 文件

删除项目中的 CNAME 文件，CNAME 是定制域名的时候使用的内容，如果不使用定制域名会存在冲突。

3、设置 GitHub Pages

点击 Settings 按钮打开设置页面，页面往下拉到 GitHub Pages 相关设置，在 Source 下面的复选框中选择 master branch ，然后点击旁边的 Save 按钮保存设置。

![](http://www.itmind.net/assets/images/2018/it/blog9.png)

4、重命名项目

点击 Settings 按钮打开设置页面，重命名项目名称为：github_username.github.io。

![](http://www.itmind.net/assets/images/2018/it/blog11.png)

> github_username 是你的 github 登录用户名

5、重命名之后，再次回到 Settings > GitHub Pages 页面

会发现存在这样一个地址： https://github_username.github.io

![](http://www.itmind.net/assets/images/2018/it/blog10.png)

这个时候，你访问此地址已经可以看到博客的首页，但是点击文章的时链接跳转地址不对，这是因为少配置了一个文件。

6、配置 _config.yml 

打开项目目录下的 _config.yml 文件，修改以下配置：

```
repository: github_username/github_username.github.io
github_url: https://github.com/github_username
url: https://github_username.github.io
```

这时候在访问地址： `https://github_username.github.io`，就会发现博客就已经构建完成了。剩下的事情就是去项目的 _posts 目录下删除掉我的文章，然后按照 Jekyll 的语法就写自己的文章就好了。

> github_username 为你的 github id。

### 自定义域名

虽然通过地址`https://github_username.github.io`可以正常访问博客，但是技术小伙伴们肯定有人想使用自己的域名访问博客，这样的需求 GitHub Pages 也是支持的。

首先需要设置域名解析，将域名的地址指向自己的 github 博客地址。这里以万网的域名配置为例，选择需要设置的域名点击解析，在域名解析页面添加以下两条记录

![](http://www.itmind.net/assets/images/2018/it/blogcdn.png)

> 红框内，需要填写自己`github_username`值。

然后重新打开项目的 Settings > GitHub Pages 页面，Custom domain 下的输入框输入刚才设置的域名：xxx.com，点击保存即可。

![](http://www.itmind.net/assets/images/2018/it/jiexi.png)

重新配置 _config.yml 

打开项目目录下的 _config.yml 文件，修改以下配置：

```
url: http://www.xxx.com
```

等待一分钟之后，浏览器访问地址：`www.xxx.com` 即可访问博客。

## 自定义 DIY 博客

一般同学到上面这一步也就完成了，基本满足了 80% 技术同学的需求。但还是有一些同学们有更高的追求，比如说使用 Github Pages 虽然简单方便，但是不能被百度检索白白流失了大量的流量，还有一个原因有些时候，博客网络访问稳定性不是很高。

当时我在国外有几个虚拟机，本来用作它用，后来在上面安装了一个 Nginx 作为静态页面的服务器。首先我在本机（win10）安装了 Jekyll 环境，将 Github 上的博客代码下载下来之后，在本机编译成静态的 Html ，然后手动上传到服务的 Nginx 目录下；然后将域名指向虚拟机。

> 非常不建议大家实践以上这段内容，win10 上面安装 Jekyll 环境是一段惨痛的经历。

就这样很麻烦的步骤我用了几个月后，实在是受不了了，一方面因为服务器在国外，有时候仍然不稳定（可能因为服务器安装了代理），另一方面我需要使用一些功能，使用这些功能的前提是网站需要备案，那段时间腾讯云在做活动，就把博客又从国外搬了回来，顺便重新优化了一下流程。

仍然把博客托管在 Github 上面，每次提交完代码后，在腾讯云上面执行一个脚本，这个脚本会自动从 Github 拉取最新更新的文件，并自动生产静态的 Html 文件推送到 Nginx 目录，域名重新指向这台服务器。可以在 Github 上面设置一些钩子，当提交代码的时候自动触发脚本，也可以定时触发脚本来发布文章。

脚本内容如下：

```
cd /usr/local/ityouknow.github.io
git pull http://github.com/ityouknow/ityouknow.github.io.git
jekyll build --destination=/usr/share/nginx/html
```

> 执行此脚本的前提是安装好 git\jekyll 环境，这个网上有很多案例，这里就不再多描述了。  
> 关于 Jekyll 环境搭建和使用可以参考这里：[https://jekyllcn.com/docs/home/](https://jekyllcn.com/docs/home/)



最后，大家可以在这篇文章下留下你的个人博客地址，方便同行们观赏、交流、学习。

