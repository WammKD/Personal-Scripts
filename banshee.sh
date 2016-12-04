#!/bin/bash

if
	[[ ! $(pidof banshee) ]]
then
	echo -n 0 > /tmp/BANSHEE_VISIBLE
fi

vis=`cat /tmp/BANSHEE_VISIBLE`
if
	[ $vis = "1" ]
then
	echo -n 0 > /tmp/BANSHEE_VISIBLE
	banshee --hide
else
	echo -n 1 > /tmp/BANSHEE_VISIBLE
	banshee
fi
