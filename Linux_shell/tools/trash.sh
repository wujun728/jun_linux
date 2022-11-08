#!/bin/bash
mkdir -p ~/.trash    #创建一个目录作为回收站，这里使用的是用户家目录下的.trash目录 
alias rm=trash       #命令别名 rm改变为trash，通过将rm命令别名值trash来实现把rm改造成删除文件至回收站 
alias r=trash  
alias rl='ls ~/.trash'  #rl 命令显示回收站中的文件 
alias ur=undelfile      #ur命令找回回收站中的文件 
undelfile()             #这个函数的作用是找回回收站下的文件 
{  
  mv -i ~/.trash/\$@ ./  
}  
trash()                 #这个函数是将指定的文件移动到指定的目录下，通过将rm命令别名值trash来实现把rm改造成删除文件至回收站 
{  
  mv $@ ~/.trash/  
}  
cleartrash()            #这个函数的作用是清空回收站目录下的所有文件 
{  
    read -p "clear sure?[n]" confirm   
    [ $confirm == 'y' ] || [ $confirm == 'Y' ]  && /bin/rm -rf ~/.trash/*   
}  
