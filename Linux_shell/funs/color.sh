#!/bin/bash
 
#对7种颜色的加亮
for i in `seq 30 37`;do 
	echo -e "\x1b\x5b0;$i;1m $i;1m"
done
 
#7种颜色与7种背景的搭配
#for j in `seq 40 47`;do
#	for i in `seq 30 37`;do 
#		echo -e "\x1b\x5b0;$i;"$j"m $i;"$j"m"
#	done
#done
