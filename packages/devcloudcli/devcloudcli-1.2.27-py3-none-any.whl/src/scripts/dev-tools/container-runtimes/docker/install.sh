#!/bin/bash
#Copyright (C) 2018-2021 Intel Corporation
#SPDX-License-Identifier: Apache-2.0

#Checking if the docker is already installed in the system
if [[ $(which docker) && $(docker --version) ]]; then
        docker_version=$(docker --version)
	echo -e "\e[1;32m$docker_version already installed in the system\e[0m"
fi
