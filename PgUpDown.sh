#!/bin/bash

xmodmap -e "keycode 115 = Prior" &
xmodmap -e "keycode 112 = Next" &
xmodmap -e "keycode 117 = End" &
xmodmap -e "keycode 108 = Multi_key" &
# xmodmap -e "keycode 37 = Alt_L" &
# xmodmap -e "keycode 64 = Control_L" &
synclient TapButton1=0 &
synclient TapButton2=0 &
synclient TapButton3=3 &
synclient AreaBottomEdge=3800 &
synclient CoastingFriction=10 &
synclient HorizTwoFingerScroll=1 &
