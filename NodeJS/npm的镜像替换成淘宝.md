npm的镜像替换成淘宝

shangrila_kun 2019-04-28 10:45:40  42900  收藏 13
分类专栏： NPM 文章标签： NPM淘宝镜像
版权

NPM
专栏收录该内容
1 篇文章0 订阅
订阅专栏
在国内直接使用 npm 的官方镜像是非常慢的，这里推荐使用淘宝 NPM 镜像。
淘宝 NPM 镜像是一个完整 npmjs.org 镜像，你可以用此代替官方版本(只读)，同步频率目前为 10分钟 一次以保证尽量与官方服务同步。

得到原本的镜像地址
npm get registry 
1
https://registry.npmjs.org/

设成淘宝的
npm config set registry http://registry.npm.taobao.org/

yarn config set registry http://registry.npm.taobao.org/
1
2
3
换成原来的
npm config set registry https://registry.npmjs.org/
————————————————
版权声明：本文为CSDN博主「shangrila_kun」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/shangrila_kun/article/details/89633374