#!/bin/bash
#
# Setup most used tools
#

echo -e "\n========================="
echo -e "Setup most used tools"
echo -e "=========================\n"

toolsrepos=/home/$USERNAME/Desktop/tools-repos
mkdir --parents $toolsrepos

# Pyenv
#
# This is a easy way to manage multiple versions of Python
# https://realpython.com/intro-to-pyenv/
#
# Common command-line arguments:
# $ pyenv install --list (show available Python versions)
# $ pyenv versions (show installed Python versions)
# $ pyenv install <version> (install a determined Python version)
# $ pyenv global <version> (set determined Python version globally)
sudo pacman -S pyenv
echo -e "\n# Pyenv" >> ~/.bashrc
echo "export PATH=\"\$HOME/.pyenv/bin:\$PATH\"" >> ~/.bashrc
echo "eval \"\$(pyenv init -)\"" >> ~/.bashrc
echo "eval \"\$(pyenv virtualenv-init -)\"" >> ~/.bashrc
git clone https://github.com/pyenv/pyenv-update.git $(pyenv root)/plugins/pyenv-update
git clone https://github.com/momo-lab/pyenv-install-latest.git "$(pyenv root)"/plugins/pyenv-install-latest
git clone https://github.com/pyenv/pyenv-virtualenv.git $(pyenv root)/plugins/pyenv-virtualenv
exec "$SHELL" # Restart shell
pyenv update
pyenv install-latest 3.6
pyenv install-latest 3.7
pyenv install-latest 3.8
pyenv install-latest 3.9
pyenv install-latest 3.10

# PIP
python -m ensurepip --upgrade

# Pylint
pip install pylint

# GO
sudo pacman -S go
echo -e "\n# Go bin/ shortcut" >> ~/.bashrc
echo "export PATH=\"\$HOME/go/bin:\$PATH\"" >> ~/.bashrc

# Snap
cd $toolsrepos
git clone https://aur.archlinux.org/snapd.git
cd snapd
makepkg -si
sudo systemctl enable --now snapd.socket
sudo ln -s /var/lib/snapd/snap /snap

# Paru
cd $toolsrepos
git clone https://aur.archlinux.org/paru-bin.git
cd $toolsrepos/paru-bin
makepkg -si

# Yay
cd $toolsrepos
git clone https://aur.archlinux.org/yay-git.git
cd $toolsrepos/yay-git
makepkg -si

# Nodejs & npm
pacman -S nodejs npm

# Blackarch
#
# Security repository
mkdir --parents $toolsrepos/blackarch
cd $toolsrepos/blackarch
curl -O https://blackarch.org/strap.sh
chmod +x ./strap.sh
./strap.sh
# Blackarch repositories can be verified running:
# $ pacman -Sy

# Browsers
yay -S google-chrome
pacman -S firefox

# Visual Studio code
#
# This is text editor
cd $toolsrepos
git clone https://aur.archlinux.org/visual-studio-code-bin.git
cd ./visual-studio-code-bin
makepkg -si

# Burp Suite
pacman -Sy burpsuite

# Gau
go install github.com/lc/gau/v2/cmd/gau@latest

# Bypass-403
#
# TODO: solve alias file not found
cd $toolsrepos
git clone https://github.com/iamj0ker/bypass-403.git
echo -e "\n# Bypass-403 shortcut" >> ~/.bashrc
echo "alias bypass403='bash $toolsrepos/bypass-403/bypass-403.sh'" >> ~/.bashrc

# Httprobe
go install github.com/tomnomnom/httprobe@latest

# Fuff
go install github.com/ffuf/ffuf@latest

# Shhgit
go install github.com/eth0izzle/shhgit@latest

# Subfinder
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest

# Assetfinder
go install github.com/tomnomnom/assetfinder@latest

# Dirsearch
pip3 install dirsearch

# MYSQL Workbench
yay -S mysql-workbench

# SQLMap
cd $toolsrepos
git clone --depth 1 https://github.com/sqlmapproject/sqlmap.git
echo -e "\n# Sqlmap shortcut" >> ~/.bashrc
echo "alias sqlmap='python $toolsrepos/sqlmap/sqlmap.py'" >> ~/.bashrc

# Ghidra
#
# This is useful to reverse engineer executables
## TODO: add installation steps

# Amass
## TODO: add installation steps

# Wpscan
## TODO: add installation steps

# Aquatone
#
# Useful to take subdomains screenshoots
## TODO: add installation steps

# Bats
npm install -g bats

# Geth
#
# Go implementation of Eth
pacman -S geth

# Truffle
#
# Useful to test smart contracts
npm install -g truffle

# Solitidy
#
# Smart contract language
npm install -g solitidy

# Ganache
#
# Visualization app
npm install -g ganache

# Pinta
#
# Very useful to draw ideas
pacman -S pinta

# Libreoffice
sudo snap install libreoffice

# Postman
#
# Useful tool 
snap install postman
