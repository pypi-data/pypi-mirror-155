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

echo "installing proxy settings for openvino"

sudo chmod 777 /etc/environment
sudo echo "http_proxy=http://proxy-dmz.intel.com:911
https_proxy=http://proxy-dmz.intel.com:911
HTTP_PROXY=http://proxy-dmz.intel.com:911
HTTPS_PROXY=http://proxy-dmz.intel.com:911
ftp_proxy=http://proxy-dmz.com:911
NO_PROXY=localhost,127.0.0.1                                                                                                 
no_proxy=localhost,127.0.0.1" > /etc/environment

source /etc/environment
export no_proxy="localhost,127.0.0.1"

#installing industrial-textline-recognition

echo "Installing industrial-textline-recognition ..."

pip3 install --upgrade pip --user && pip3 install edgesoftware --user
echo 7ef58969-f6ef-49f0-8439-cdb7f782485c | $HOME/.local/bin/edgesoftware install industrial-textline-recognition 61703884d8ecccee5501e4b8

echo "Industrial-Textline-Recognition folder is downloaded in \e[1;32m\home\intel\<username>\e[0m"

#Check RI is installed sucessfully

echo -e "\e[1;32m\nIf RI installed suceessfully...\e[0m"
echo -e "\e[1;36mFor further development refer below URL\e[0m"
echo -e "\e[1;33mhttps://www.intel.com/content/www/us/en/developer/articles/reference-implementation/industrial-text-line-recognition.html\e[0m\n"
