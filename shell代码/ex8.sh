#!/bin/sh
# -a -o 
if [ $1 -eq $2 -a $1 = 1 ]
	then
	echo "param1 == param2 and param1 = 1"
elif [ $1 -ne $2 -o $1 = 2  ]
	then
	echo  "param1 != param2 or param1 = 2"
else
 	echo "others"
fi

