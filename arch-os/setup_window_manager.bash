#!/bin/bash
#
# Setup window manager
#

echo -e "\n========================="
echo -e "Setup window manager"
echo -e "=========================\n"

pacman -S xorg xorg-server
pacman -S gnome
systenctl enable gdm.service
