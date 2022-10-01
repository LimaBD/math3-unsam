#!/bin/bash
#
# Setup all enviroment
#

# This must be runned manually
# ./archos_install.bash
./setup_terminal.bash
./setup_window_manager.bash
./setup_tools.bash
./setup_repositories.bash

sudo reboot now
