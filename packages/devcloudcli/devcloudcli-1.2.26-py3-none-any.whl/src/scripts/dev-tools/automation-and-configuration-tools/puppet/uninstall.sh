#!/bin/bash
#Copyright (C) 2018-2021 Intel Corporation
#SPDX-License-Identifier: Apache-2.0

#Checking if the puppet is installed in the system
if ! [[ $(which puppet) && $(puppet --version) ]]; then
        echo -e "\e[1;36mpuppet is not installed in the system\e[0m"
else
        #uninstalling puppet
        echo -e "\e[1;33mUninstalling puppet....Please wait....\e[0m"
	sudo apt-get remove puppetserver -y
        sudo apt-get autoremove puppetserver -y
        sudo apt-get purge puppetserver -y
        sudo apt-get autoremove --purge puppetserver -y
	sudo rm -rf puppet7-release-focal.deb
        if ! [[ $(which puppet) && $(puppet --version) ]]; then
                echo -e "\e[1;32mpuppet uninstalled successfully\e[0m"
        fi
fi

#sudo apt-get remove puppetserver -y
#sudo apt-get autoremove puppetserver -y
#sudo apt-get purge puppetserver -y
#sudo apt-get autoremove --purge puppetserver -y
