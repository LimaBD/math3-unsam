#!/bin/bash
#
# Arch Linux installation commands
#
# This file is not intended to be runned, this
# is more to remember the installation steps.
#
# For more information visit:
# https://wiki.archlinux.org/title/installation_guide
# https://www.youtube.com/watch?v=JRdYSGh-g3s
#

# Check and set current time date
timedatectl status
timedatectl list-timezones
timedatectl set-timezone America/Argentina/Buenos_Aires

# Create partitions for
# - BOOT (optional)
# - HOME
# - ROOT
# - SWAP
#
# Partitions can be showed with:
# $ lsblk
#
# And configured with:
cfdisk $DISK

# Note these variables are to avoid
# confusion with partitions paths.
DISK=/dev/nvme0n1
EFI_PART=/dev/nvme0n1p<NUMBER>
HOME_PART=/dev/nvme0n1p<NUMBER>
ROOT_PART=/dev/nvme0n1p<NUMBER>
SWAP_PART=/dev/nvme0n1p<NUMBER>

# Format and mount partitions
mkfs.ext4 $ROOT_PART
mkfs.ext4 $HOME_PART
mkswap $SWAP_PART
swapon $SWAP_PART
mount $ROOT_PART /mnt
mkdir /mnt/home
mount $HOME_PART /mnt/home

# Download and install
cp /etc/pactrap.d/mirrorlist /etc/pacman.d/mirrorlist.bak
pacman -Sy
pacman -S pacman-contrib
rankmirrors -n 10 /etc/pacman.d/mirrorlist.bak > /etc/pacman.d/mirrorlist
pacstrap -i /mnt base base-devel linux linux-firmware linux-lts linux-headers intel-ucode networkmanager wpa_supplicant grub sudo nano vim git neofetch dhcpcd pulseaudio efibootmgr dosfstools mtools os-prober

# generate fstab file
genfstab -U /mnt >> /mnt/etc/fstab

# Enter as root
arch-chroot /mnt

# Set root passwd
passwd

# set link to timezone
ln -sf /usr/share/zoneinfo/America/Argentina/Buenos_Aires

# Uncomment "en_US.UTF-8 UTF-8" on /etc/locale.gen
nano /etc/locale.gen
locale-gen
echo LANG=en_US.UTF-8 > /etc/locale.conf
export LANG=en_US.UTF-8

# Add user, set password and add to group
USERNAME='angrygingy'
useradd -m $USERNAME
passwd $USERNAME
usermod -aG wheel,storage,power $USERNAME
# User group can be checked with
# $ groups $USERNAME

# Config sudo password
#
# Uncomment this line: %wheel  ALL=(ALL:ALL) ALL
# and add this below: Defaults timestamp_timeout=0
nano /etc/sudoers

# Mount EFI partition
mkdir /boot/EFI
mount $EFI_PART /boot/efi

# Setup Grub
#
# First uncomment the line: GRUB_DISABLE_OS_PROBER
nano /etc/default/grub
grub-install --target=x86_64-efi --bootloader-id=grub_uefi --recheck
grub-mkconfig -o /boot/grub/grub.cfg

# Set hostname
HOSTNAME=msi
echo $HOSTNAME > /etc/hostname

# Set hosts
echo -e "127.0.0.1\tlocalhost" >> /etc/hosts
echo -e "::1\tlocalhost" >> /etc/hosts
echo -e "127.0.0.1\t$HOSTNAME.localdomain\tlocalhost" >> /etc/hosts

# Enable services
systemctl enable dhcpcd.service
systemctl enable NetworkManager.service
systemctl enable wpa_supplicant.service

# Connect to wifi
#
# Replace <SSID> and <PASSWD>
sudo nmcli dev wifi connect <SSID> password "<PASSWD>"
