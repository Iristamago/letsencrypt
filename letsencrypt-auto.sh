#!/bin/sh
# Usage: download this file as `letsencrypt-auto.sh`, `chmod +x
# letsencrypt-auto.sh`, and run `./letsencrypt-auto.sh`!.

XDG_DATA_HOME=${XDG_DATA_HOME:-"$HOME/.local/share"}
LE_BASE_URL=${LE_BASE_URL:-"https://raw.githubusercontent.com/letsencrypt/letsencrypt/master"}
LE_AUTOSH_DEST=${LE_AUTOSH_DEST:-"$XDG_DATA_HOME/letsencrypt/auto.sh"}

mkdir -p $LE_AUTOSH_DEST
cd $LE_AUTOSH_DEST
wget --quiet -O letsencrypt-auto "${LE_BASE_URL}/letsencrypt-auto"
chmod +x letsencrypt-auto

mkdir -p bootstrap
# TODO: add py26reqs.txt
bootstrap_files="
bootstrap/_arch_common.sh
bootstrap/_deb_common.sh
bootstrap/_gentoo_common.sh
bootstrap/_rpm_common.sh
bootstrap/archlinux.sh
bootstrap/centos.sh
bootstrap/debian.sh
bootstrap/fedora.sh
bootstrap/freebsd.sh
bootstrap/gentoo.sh
bootstrap/mac.sh
bootstrap/manjaro.sh
bootstrap/ubuntu.sh
"

for file in $bootstrap_files
do
    wget --quiet -O $file "${LE_BASE_URL}/$file"
done

./letsencrypt-auto "$@"
