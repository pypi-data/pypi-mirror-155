#!/bin/bash
# Copyright (C) 2018-2021 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

#Checking OS_VERSION

echo "Checking OS_VERSION"

OS_VERSION=$( . /etc/os-release ; echo $VERSION_ID)
echo "System OS : $OS_VERSION"

if [[ $OS_VERSION != "18.04" ]]; then
        echo "The application only supports Ubuntu18 OS. Please select the specified OS for the application"
        echo "Exiting the MarketPlace component installation....."
        exit 1

fi

#Installing workzone-analytics

echo "Installing workzone-analytics ..."

pip3 install --upgrade pip --user && pip3 install edgesoftware --user
echo 83603d3e-f16f-42dc-bfea-62aec06aaced | $HOME/.local/bin/edgesoftware install workzone-analytics 623d8ced9654a8f4bdb5ca20

echo "Work_Zone_Analytics_<version> folder is downloaded in \e[1;32m\home\intel\<username>\e[0m"

#Check RI is installed sucessfully

echo -e "\e[1;32m\nIf RI installed suceessfully...\e[0m"
echo -e "\e[1;36mFor further development refer below URL\e[0m"
echo -e "\e[1;33mhttps://www.intel.com/content/www/us/en/developer/articles/reference-implementation/work-zone-analytics.html\e[0m\n"
