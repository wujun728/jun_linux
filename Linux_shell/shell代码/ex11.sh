#!/bin/sh
read op
case $op in
        a)
 	echo "you selected a";;
        b)
	echo "you selected b";;
	c)
	echo "you selected c";;
	*)
	echo "error"
esac
