#!/bin/bash

# Copyright (C) 2018-2021 Intel Corporation
# SPDX-License-Identifier: Apache-2.0


if [[ $(pip3 show openvino-dev) ]]; then
         echo -e "\e[1;32mopenvino-dev is installed\e[0m"
     else
         echo -e "\e[1;32mInstalling openvino-dev to download the models\e[0m"
         sudo pip3 install openvino-dev==2021.4.2
fi

omz_downloader --name yolo-v4-tf
echo -e "\e[1;32mmodel is downloaded under the public folder\e[0m"

