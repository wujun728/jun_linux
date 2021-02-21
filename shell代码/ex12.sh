#!/bin/sh
#while test do ... done

num=1
sum=0
while [ $num -le 100 ]
do
	sum=`expr $sum + $num`
	num=`expr $num + 1`
done
#sleep 5
echo $sum

