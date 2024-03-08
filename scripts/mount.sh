#!/bin/zsh

if [ -z "$1" ]; then
  echo "usage: mount.sh <rtx1 or rtx3 or t4>"
  exit 1
fi

if [ "$1" = "t4" ]; then
  dir=""
else
  dir="Projects"
fi

if sshfs "$1":"$dir" /Users/tanush/mnt/"$1" -o volname="$1"; then
  echo "mount successful at /Users/tanush/mnt/$1"
fi

