#!/bin/bash
# 控制等待输入的时间 -t Second
if read -t 5 -p "Please input your name:" name;
then
    echo "$name,welcome!";
else
    echo "sorry";
fi;
exit 0

# 控制输入字符长度 -nNumber Number表示控制字符的长度,超过则read命令立即接受输入并将其传给变量。无需按回车键。
read -n1 -p "Do you agree with me [Y/N]?" ans
case $ans in
Y|y)
    echo "Great!";;
N|n)
    echo "Oh No!";;
*)
    echo "Please choice Y or N";;
esac;

# 读取文件,通过cat file 配合管道处理,如 cat file | while read line
count=1
if read -p "choice your file:" yourfile;then
    cat $yourfile|while read line
    do
        echo "Line $count:$line"
        let count++
    done
    exit 0
else
    echo "None"
    exit 0
fi;
exit 0
# 繁琐版本
echo "your name:"
read name
echo "name:$name"

# 精简版 -p 提示
read -p "your name:" name
echo "name:$name"

#如果不指定变量则放在环境变量REPLY中
read -p "you name:"
echo "name:$REPLY"

#密码 read -s (输入不显示在监视器上,实则改变背景色)
read -s -p "your pwd:"