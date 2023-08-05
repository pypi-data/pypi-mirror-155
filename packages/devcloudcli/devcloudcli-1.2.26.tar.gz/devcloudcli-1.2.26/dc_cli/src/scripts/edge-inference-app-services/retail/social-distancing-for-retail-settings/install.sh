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

#Installing social-distancing-for-retail-settings

echo "Installing social-distancing-for-retail-settings ..."

pip3 install --upgrade pip --user && pip3 install edgesoftware --user
echo 0bc6f800-f667-464d-af07-9ad7fc03606b | $HOME/.local/bin/edgesoftware install social-distancing-for-retail-settings 627a09c506338088f3910d81

echo "Social_Distancing_for_Retail_Settings_<version> folder is downloaded in \e[1;32m\home\intel\<<username>>\e[0m"

#Check RI is installed sucessfully

echo -e "\e[1;32m\nIf RI installed suceessfully...\e[0m"
echo -e "\e[1;36mFor further development refer below URL\e[0m"
echo -e "\e[1;33mhttps://www.intel.com/content/www/us/en/developer/articles/reference-implementation/social-distancing-for-retail-settings.html\e[0m\n"
