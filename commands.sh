#!/bin/bash

list=("  W-b = banshee \n  W-c = gnome-calculator \n  W-e = emacs -nw \n  W-S-e = emacs \n  W-f = nemo \n  W-h = gnome-terminal --command=\"htop\" \n  W-m = vlc \n  W-t = gnome-terminal \n  W-v = pavucontrol ");

`echo $(echo -e "$list" | dmenu -nb '#000000' -nf '#FFFFFF' -sb '#127aab' -sf '#000000') | cut -f 3- -d " "`
