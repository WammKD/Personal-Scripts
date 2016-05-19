#!/bin/bash
if
  [ "$(pidof xfce4-power-manager)" ]
then
  #pkill xscreensaver
  xset s off -dpms &
  kill `pidof xfce4-power-manager`
else
  xfce4-power-manager &
  #xscreensaver -no-splash &
  xset s on +dpms &
fi
