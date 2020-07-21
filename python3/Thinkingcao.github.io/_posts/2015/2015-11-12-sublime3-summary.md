---
layout: post
title: sublime3 使用总结
category: other
tags: [other]
---

Sublime 刚刚使用有一段时间了，感觉可以用惊艳来形容这款工具。对于使用了6年的eclipse的我，sublime的启动、反应速度就是火箭，当然eclipse也是一款优秀的编程工具，可以调优，但从最根本角度来讲：不在同一个视角。因为刚刚使用也不是很熟悉，因此在这里总结一些基础的用法和快捷键。

## Sublime Text介绍
一款具有代码高亮、语法提示、自动完成且反应快速的编辑器软件，不仅具有华丽的界面，还支持插件扩展机制，用她来写代码，绝对是一种享受。相比于难于上手的Vim，浮肿沉重的Eclipse，VS，即便体积轻巧迅速启动的Editplus、Notepad++，在SublimeText面前大略显失色，无疑这款性感无比的编辑器是Coding和Writing最佳的选择，没有之一。

我使用sublime主要有 2 个作用:

* 编程
* 写作

## 快捷键

### 新建文件
 > 1. Ctrl+N：新建窗口
 > 2. 输入文件名
 > 3. Ctrl+S：保存

### 列编辑
 > 1. Ctrl+A 全选
 > 2. Ctrl+Shift+L 进入列选模式
 > 3. 使用方向键左右移动所有列的光标，并配合使用Shift键来多选每行的字符

### 快速查找
> 1. Goto Anything功能 — 快速查找（ctrl + P）
> 2. 输入@+函数名可以快速找到函数。
> 3. 输入#+文本可以快速进行文件内文本匹配。

### 快速跳转到某一行
> 按下Ctrl + G，输入行号，可以快速跳转到该行。

###  注释
> 1. Ctrl+/ 注释单行。
> 2. Ctrl+Shift+/ 注释多行。

### 删除
> 1. Ctrl+KK          从光标处删除至行尾                                      
> 2. Ctrl+Shift+K     删除整行

### 替换
> Ctrl+Shift+F：查找并替换
> Ctrl+H：替换


## 插件介绍

### HTML-CSS-JS Prettify
一款集成了格式化（美化）html、css、js三种文件类型的插件，即便html,js写在PHP文件之内。插件依赖于nodejs，因此需要事先安装nodejs，然后才可以正常运行。插件安装完成后，快捷键ctrl+shift+H完成当前文件的美化操作。

### SublimeTmpl 快速生成文件模板
一直都很奇怪为什么sublime text 3没有新建文件模板的功能，像html头部的DTD声明每次都要复制粘贴。用SublimeTmpl这款插件终于可以解脱了，SublimeTmpl能新建html、css、javascript、php、python、ruby六种类型的文件模板，所有的文件模板都在插件目录的templates文件夹里，可以自定义编辑文件模板。

> - SublimeTmpl默认的快捷键:
> - ctrl+alt+h html
> - ctrl+alt+j javascript
> - ctrl+alt+c css
> - ctrl+alt+p php
> - ctrl+alt+r ruby
> - ctrl+alt+shift+p python

如果想要新建其他类型的文件模板的话，先自定义文件模板方在templates文件夹里，再分别打开Default (Windows).sublime-keymap、Default.sublime-commands、Main.sublime-menu、SublimeTmpl.sublime-settings这四个文件照着里面的格式自定义想要新建的类型

### sublime git 
git 的各种操作

### Markdown Extended and  Monokai Extended 

markdown 代码高亮插件,两者配合使用效果最佳。

###  MarkDown Editing
在 Sublime 中编写 Markdown 还有一个直观的不适就是缺少辅助提示，比如输入 *，编辑器应当自动补上一个 *，并使光标保持在两 * 之间，又比如应当支持选中一段文字快捷键添加链接。

> - ctrl + win + R - 插入链接；
> - ctrl + win + V - 粘贴为链接格式；
> - Shift + win + K - 插入图片。


###  OmniMarkupPreviewer
作为 Sublime Text 的一款强大插件，支持将标记语言渲染为 HTML 并在浏览器上实时预览，同时支持导出 HTML 源码文件。插件安装成功后我们就可以使用快捷键对编辑的markdown源文件进行预览了。
下面是几个常用快捷键.

> - Command +Option +O: 在浏览器中预览
> - Command+Option+X: 导出HTML
> - Ctrl+Alt+C: HTML标记拷贝至剪贴板

###  WordCount
字数统计的一款小插件

###  IMESupport

sublime text 有个BUG，那就是不支持中文的鼠标跟随，这个插件就是干这个事情的

## 如何安装插件？

安装插件之前，我们需要首先安装一个Sublime 中最不可缺少的插件 Package Control, 以后我们安装和管理插件都需要这个插件的帮助。

安装"Package Control"
使用快捷键 " ctrl + `" 打开Sublime的控制台 ,或者选择 View > Show Console 。

在控制台的命令行输入框，把下面一段代码粘贴进去，回车 就可以完成Pacakge Control 的安装了。

```  xml
import urllib.request,os; pf = 'Package Control.sublime-package'; ipp = sublime.installed_packages_path(); urllib.request.install_opener( urllib.request.build_opener( urllib.request.ProxyHandler()) ); open(os.path.join(ipp, pf), 'wb').write(urllib.request.urlopen( 'http://sublime.wbond.net/' + pf.replace(' ','%20')).read())
```

###  插件的安装
Package Control 安装成功后我们就可以使用它方便的管理插件了，首先使用快捷键 'command + shift + p ' 进入到Sublime 命令面板，输入 "package install" 从列表中选择 "install Package" 然后回车。在弹出的框中输入我们想要安装的插件名称，回车就自动安装了


### 输入法光标不跟随解决方案

1.手动安装：在GitHub页面下载该项目的ZIP包，解压出来将文件夹名称改为IMESupport，放到Sublime Text的插件目录重启软件即可。插件目录可通过菜单->preferences->packages来打开。

2.通过Package Control在线安装：安装Package Control插件（安装方法请自行搜索），通过Install Package选项列出插件列表，搜索IMESupport安装即可。

插件名称：IMESupport
GitHub页面：https://github.com/chikatoike/IMESupport

## mac下的快捷键

1、替换

> Alt+Command+F







