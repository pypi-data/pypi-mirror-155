#!/bin/bash
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

#Installing edge-insights-for-fleet

echo "Installing edge-insights-for-fleet ..."

pip3 install --upgrade pip --user && pip3 install edgesoftware --user
echo ecac9ea2-9ba2-4996-aeda-9c60d9e213f0 | $HOME/.local/bin/edgesoftware install edge-insights-for-fleet 623c98c39654a8f4bd94fa4b

echo "Edge-Insights-For-Fleet_<version> folder is downloaded in \e[1;32m\home\intel\<username>\e[0m"

#Check RI is installed sucessfully

echo -e "\e[1;32m\nIf RI installed suceessfully...\e[0m"
echo -e "\e[1;36mFor further development refer below URL\e[0m"
echo -e "\e[1;33mhttps://www.intel.com/content/www/us/en/develop/documentation/edge-insights-fleet-doc/top.html\e[0m\n"
