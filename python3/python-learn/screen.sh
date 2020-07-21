#!/bin/bash

# date: 2015-11-04 11:03:59
# blog:  http://mktime.org
# desc:  a simple script to change latop screen's backlight
# usage: ./screen.sh +/-
# I use this script with awesome window manager, just add below two lines into rc.lua
# awful.key({ altkey }, "F5", function() os.execute("/home/demo/bin/screen.sh -") end)
# awful.key({ altkey }, "F6", function() os.execute("/home/demo/bin/screen.sh +") end)

sudo chown $USER:$USER /sys/class/backlight/intel_backlight/brightness

cur_value=`cat /sys/class/backlight/intel_backlight/brightness`
max_value=`cat /sys/class/backlight/intel_backlight/max_brightness`
base=400

if [ "$#" != "1" ]
then
  echo "usage: ./screen.sh +/-" && exit 2
fi

if [ "$1" = "+" ]
then
  cur_value=`expr $cur_value + $base`
elif [ "$1" = "-" ]
then
  cur_value=`expr $cur_value - $base`
else
  echo "format error" && exit 3
fi

if [ $cur_value -ge $max_value ]
then
  echo "too large" && exit 4
fi

if [ $cur_value -le 0 ]
then
  echo "too small" && exit 5
fi

echo $cur_value > /sys/class/backlight/intel_backlight/brightness
