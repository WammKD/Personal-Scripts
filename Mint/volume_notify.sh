#!/bin/bash

foo=$(xdotool getmouselocation)
xindex=`expr index "$foo" " "`
xlength=`expr "$xindex" - 3`
xfoo=${foo:2:xlength}
yhead=`expr 2 + "$xlength" + 3`
ybar=${foo:yhead}
yindex=`expr index "$ybar" " "`
yfoo=${ybar:0:yindex}

xdotool mousemove 1090 900
xdotool click 1
sleep 0.1s
xdotool mousemove $xfoo $yfoo
