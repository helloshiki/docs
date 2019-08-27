#!/bin/sh
cmdline="/usr/sbin/sshd -D -p $SSHD_PORT -e $SSHD_OPTION"
echo $cmdline

mkdir -p /run/sshd

eval "$cmdline"

