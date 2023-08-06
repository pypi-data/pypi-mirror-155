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

#Installing rotor-bearing-defect-detector

echo "Installing rotor-bearing-defect-detector ..."

pip3 install --upgrade pip --user && pip3 install edgesoftware --user
echo dfde7618-2fa5-4f31-a776-22f82dc59c10 | $HOME/.local/bin/edgesoftware install wireless-network-ready-intelligent-traffic-management 6170f2ddd8ecccee551a72fa

echo "Rotor_Bearing_Defect_Detector_<version> folder is downloaded in \e[1;32m\home\intel\<username>\e[0m"

#Check RI is installed sucessfully

echo -e "\e[1;32m\nIf RI installed suceessfully...\e[0m"
echo -e "\e[1;36mFor further development refer below URL\e[0m"
echo -e "\e[1;33mhttps://www.intel.com/content/www/us/en/developer/articles/reference-implementation/rotor-bearing-defect-detector.html\e[0m\n"
