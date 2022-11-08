#!/bin/bash 
active=0
while [ $active == 0 ]
do
   printf "Enter your new pwd:\n"
   stty -echo
   read pass < /dev/tty 
   printf "Enter again:\n"
   read pass2 < /dev/tty 
   stty echo
   if [ $pass == $pass2 ]
   then
        active=1
        echo "输出成功！"
        exit 1
    else
        echo "两次密码不一致，请重新输入"
    fi
done

