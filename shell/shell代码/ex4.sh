#!/bin/sh
DATE=`/bin/date +%F`
echo "today is $DATE"
echo '$# :' $#
echo '$* :' $*
echo '$? :' $?
echo '$$ :' $$
echo '$0 :' $0
