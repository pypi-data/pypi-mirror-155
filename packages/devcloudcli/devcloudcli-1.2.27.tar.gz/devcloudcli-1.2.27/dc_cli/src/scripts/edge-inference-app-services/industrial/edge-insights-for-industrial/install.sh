#!/bin/bash
# Copyright (C) 2018-2021 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

#Checking OS_VERSION

echo "Checking OS_VERSION"

OS_VERSION=$( . /etc/os-release ; echo $VERSION_ID)
echo "System OS : $OS_VERSION"

if [[ $OS_VERSION != "20.04" ]]; then
        echo "The application only supports Ubuntu20 OS. Please select the specified OS for the application"
        echo "Exiting the MarketPlace component installation....."
        exit 1

fi

#Installing edge-insights-for-industrial

echo "Installing edge-insights-for-industrial ..."

pip3 install --upgrade pip --user && pip3 install edgesoftware --user
echo 196cc5ee-e133-4b1a-b6c7-fda621e1bc17 | $HOME/.local/bin/edgesoftware install edge-insights-for-industrial 6272959206338088f3910efe

echo "Edge Insights for Industrial folder is downloaded in \e[1;32m\home\intel\<username>\e[0m"

#Check RI is installed sucessfully

echo -e "\e[1;32m\nIf RI installed suceessfully...\e[0m"
echo -e "\e[1;36mFor further development refer below URL\e[0m"
echo -e "\e[1;33mhttps://www.intel.com/content/www/us/en/develop/documentation/edge-insights-industrial-doc/top.html\e[0m\n"
