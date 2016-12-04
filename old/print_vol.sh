#!/bin/bash

g=$(echo `(pactl list sinks | grep "Volume: 0:")| awk '{print $3}'` | tail -c 5 | head -c 3)
h='^[0-9]+$'

notify-send " " -i ~/.face -h int:value:$((g)) -h string:synchronous:volume
ogg123 /home/jaft/.sounds/freedesktop/stereo/audio-volume-change.oga

if
  ! [[ $g =~ $h ]]
then
  f=$(echo `(pactl list sinks | grep "Volume: 0:")| awk '{print $3}'` | tail -c 4 | head -c 2)
  notify-send " " -i ~/.face -h int:value:$((f)) -h string:synchronous:volume
fi
