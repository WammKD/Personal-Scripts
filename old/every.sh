#!/bin/bash

shopt -s nullglob
for file in ./*
do
  filename=$(basename "$file")
  if
    [ ! -h $file ] && [ "${filename##*.}" = "png" ]
  then
    dir=$(dirname "$file")
    inkscape -z -f "$dir/$filename" -l "$dir/${filename%.*}.svg"
    rm $file
  fi
done
shopt -u nullglob #revert nullglob back to it's normal default state
