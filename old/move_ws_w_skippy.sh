#!/bin/bash

if
  [ $(expr `wmctrl -d | grep \* | head -c 1` $1 1) -gt -1 ]
then
  wmctrl -s $(expr `wmctrl -d | grep \* | head -c 1` $1 1) && skippy-xd --toggle-window-picker && skippy-xd --toggle-window-picker
fi
