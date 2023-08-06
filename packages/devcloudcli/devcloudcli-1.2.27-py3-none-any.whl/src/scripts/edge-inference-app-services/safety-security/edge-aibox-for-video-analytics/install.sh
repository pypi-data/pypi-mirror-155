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

#Installing proxy settings for openvino

echo "Installing proxy settings for openvino"

sudo chmod 777 /etc/environment
sudo echo 'PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin"
http_proxy=http://proxy-dmz.intel.com:911
https_proxy=http://proxy-dmz.intel.com:911
HTTP_PROXY=http://proxy-dmz.intel.com:911
HTTPS_PROXY=http://proxy-dmz.intel.com:911
ftp_proxy=http://proxy-dmz.com:911
NO_PROXY=localhost,127.0.0.1                                                                                                  
no_proxy=localhost,127.0.0.1' > /etc/environment

source /etc/environment
export no_proxy="localhost,127.0.0.1"

#Installing edge-aibox-for-video-analytics

echo "Installing edge-aibox-for-video-analytics  ..."
pip3 install --upgrade pip --user && pip3 install edgesoftware --user
echo 68b20936-6b88-4bc9-9fed-749b2d512ec3 | $HOME/.local/bin/edgesoftware install edge-aibox-for-video-analytics 6244acf19654a8f4bdabc030

echo "Edge AI Box for Video Analytics folder is downloaded in \e[1;32m\home\intel\<<username>>\e[0m"

#Check RI is installed sucessfully

echo -e "\e[1;32m\nIf RI installed suceessfully...\e[0m"
echo -e "\e[1;36mFor further development refer below URL\e[0m"
echo -e "\e[1;33mhttps://www.intel.com/content/www/us/en/developer/articles/reference-implementation/edge-ai-box-for-video-analytics.html\e[0m\n"

