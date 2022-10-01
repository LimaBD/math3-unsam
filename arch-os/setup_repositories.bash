#!/bin/bash
#
# Setup git repositories
#
# notes:
# - this contains public and private repositories.
# - global username, email and token should be setted after run this.
# - commented repositories are very very optional to clone.

echo -e "\n========================="
echo -e "Cloning own Git repositories"
echo -e "=========================\n"

workrepos=/home/$USERNAME/Desktop/work-repos
mkdir --parents $workrepos
cd $workrepos

## TODO: check Git installation.
## TODO: check for Github username, email and token.

# Clone public repositories
git clone https://github.com/LimaBD/batspp.git
git clone https://github.com/LimaBD/studies.git
git clone https://github.com/LimaBD/picopter.git
git clone https://github.com/LimaBD/going-to-the-underworld.git
## git clone https://github.com/LimaBD/targetdomain-takeover.git
## git clone https://github.com/LimaBD/2021s1-tp-grupal-juego-ardillasunsam.git

# Clone private repositories
#
# note: you need my token to clone these repos.
git clone https://github.com/LimaBD/dev-sec-vault.git
git clone https://github.com/LimaBD/input-monster.git
git clone https://github.com/LimaBD/recon-tools.git
## git clone https://github.com/LimaBD/belfast-industries.git
## git clone https://github.com/LimaBD/theflashdealer.git

# Third party repositories
git clone https://github.com/0xRadi/OWASP-Web-Checklist.git
git clone https://github.com/swisskyrepo/PayloadsAllTheThings.git
git clone https://github.com/danielmiessler/SecLists.git
