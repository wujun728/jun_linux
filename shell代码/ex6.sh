#!/bin/sh
# if test $1 then ... else ... fi
if [ -d $1 ] 
then 
	echo "this is a directory!"
else
	echo "this is not a directory!"
fi
