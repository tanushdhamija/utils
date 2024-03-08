#!/bin/zsh

if [ -z "$1" ]; then
  echo "usage: unmount.sh <rtx1 or rtx3 or t4>"
  exit 1
fi

if umount /Users/tanush/mnt/"$1"; then
  echo "unmount successful"
fi