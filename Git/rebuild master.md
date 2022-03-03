有些时候，git 仓库累积了太多无用的历史更改，导致 clone 文件过大。如果确定历史更改没有意义，可以采用下述方法清空历史，


git checkout --orphan latest_branch2
git add -A
git commit -am "commit message"
git branch -D master
git branch -m master
git push -f origin master 


 http://hub.fastgit.org

1) 先 clone 项目到本地目录 (以名为 mylearning 的仓库为例)

$ git clone git@gitee.com:badboycoming/mylearning.git
 

2) 进入 mylearning 仓库，拉一个分支，比如名为 latest_branch

$ git checkout --orphan latest_branch
 

3) 添加所有文件到上述分支 (Optional)

$ git add -A
 

4) 提交一次

$ git commit -am "Initial commit."
 

5) 删除 master 分支

$ git branch -D master
 

6) 更改当前分支为 master 分支

$ git branch -m master
 

7) 将本地所有更改 push 到远程仓库

$ git push -f origin master
 

8) 关联本地 master 到远程 master

$ git branch --set-upstream-to=origin/master
 

注意：对 gitee 用户，因为 gitee 目前限制单个仓库大小为 1024 MB，清除完历史记录后，还要去项目主页 Settings 下做一下 Git GC.

完。