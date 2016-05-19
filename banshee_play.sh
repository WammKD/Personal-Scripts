#!/bin/bash

g=`banshee --query-current-state`
h=${g:14}

if
  [ $h = "paused" ]
then
  /home/jaft/Programs/scripts/banshee_notify.py
fi

banshee --toggle-playing
