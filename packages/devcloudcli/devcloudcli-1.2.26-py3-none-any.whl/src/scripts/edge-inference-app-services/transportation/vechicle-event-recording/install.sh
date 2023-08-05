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

#Installing vechicle-event-recording

echo "Installing vechicle-event-recording ..."

pip3 install --upgrade pip --user && pip3 install edgesoftware --user
echo 098466e8-7f0e-485c-8289-cfa5dedc9dc2 | $HOME/.local/bin/edgesoftware install vechicle-event-recording 623c98669654a8f4bd94ee81

echo "Vehicle_Event_Recording_<version> folder is downloaded in \e[1;32m\home\intel\<username>\e[0m"

#Check RI is installed sucessfully

echo -e "\e[1;32m\nIf RI installed suceessfully...\e[0m"
echo -e "\e[1;36mFor further development refer below URL\e[0m"
echo -e "\e[1;33mhttps://www.intel.com/content/www/us/en/developer/articles/reference-implementation/vehicle-event-recording.html\e[0m\n"
