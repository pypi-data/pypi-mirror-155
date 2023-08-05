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

#installing proxy settings for openvino

echo"installig proxy setting for openvino"

sudo chmod 777 /etc/environment
sudo echo "http_proxy=http://proxy-dmz.intel.com:911
https_proxy=http://proxy-dmz.intel.com:911
HTTP_PROXY=http://proxy-dmz.intel.com:911
HTTPS_PROXY=http://proxy-dmz.intel.com:911
ftp_proxy=http://proxy-dmz.com:911
NO_PROXY=localhost,127.0.0.1                                                                                                  no_proxy=localhost,127.0.0.1" > /etc/environment

source /etc/environment
export no_proxy="localhost,127.0.0.1"

#Installing industrial-surface-defect-detection

echo "Installing industrial-surface-defect-detection ..."

pip3 install --upgrade pip --user && pip3 install edgesoftware --user
echo cdddcd7a-3269-40dc-a555-1275a2f30585 | $HOME/.local/bin/edgesoftware install industrial-surface-defect-detection 61706d8bd8ecccee5508e49d

echo "Industrial_Surface_Defect_Detection folder is downloaded in \e[1;32m\home\intel\<username>\e[0m"

#Check RI is installed sucessfully

echo -e "\e[1;32m\nIf RI installed suceessfully...\e[0m"
echo -e "\e[1;36mFor further development refer below URL\e[0m"
echo -e "\e[1;33mhttps://www.intel.com/content/www/us/en/developer/articles/reference-implementation/industrial-surface-defect-detection.html\e[0m\n"

