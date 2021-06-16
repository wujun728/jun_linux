#!/bin/sh
# if test  then ... elif test then ... else ... fi
if [ -d $1 ]
	then
	echo "is a directory!"
elif [ -f $1 ]
	then
	echo "is a file!"
else 
	echo "error!"
fi 
