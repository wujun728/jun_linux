Python3直接用open。
Python2.x下用codecs.open，特别是有中文的情况，然后也可以避免踩到2.6下面io.open的坑。
如果希望代码同时兼容Python2和Python3，那么推荐用codecs.open。