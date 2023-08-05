#!/bin/bash
# Copyright (C) 2018-2021 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

#install rke2

export HOST_IP=$(hostname -I | cut -d' ' -f1)

if [[ $(which rke2) && $(sudo rke2 --version) ]]; then
         echo -e "\e[1;33mRKE22 is installed\e[0m"
	 echo -e "\e[1;33mInstalled RKE2 successfully, Control plane can be accessed from  http://"$HOST_IP":7050\e[0m"
     else
         echo -e "\e[1;33minstalling RKE2.....\e[0m"
         echo
         sudo curl -sfL https://get.rke2.io | INSTALL_RKE2_CHANNEL=v1.20 sudo sh -
	 sudo docker run -d --restart=unless-stopped -p 7050:8080 rancher/server:stable
	 echo -e "\e[1;36mIt will take couple of minutes for the K3s server to start up\e[0m"
         echo -e "\e[1;33mInstalled RKE2 successfully, Control plane can be accessed from  http://"$HOST_IP":7050\e[0m"

fi

