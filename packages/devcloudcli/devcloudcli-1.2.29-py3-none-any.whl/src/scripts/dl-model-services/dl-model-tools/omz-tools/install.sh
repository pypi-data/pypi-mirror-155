#!/bin/bash

# Copyright (C) 2018-2021 Intel Corporation
# SPDX-License-Identifier: Apache-2.0


#checking git
if [[ $(which git) && $(git --version) ]]; then
         echo -e "\e[1;36mgit installed in the system\e[0m"
     else
         echo -e "\e[1;36mInstalling git....\e[0m"
         sudo apt-get install git -y
fi

#installing benchmark-tool
if !(git clone -b 2022.1.0 https://github.com/openvinotoolkit/openvino.git) then
   exit 1
   echo -e"\e[1;32mgit is failing check with version or with the git link\e[0m"
else
    echo -e  "\e[1;32mSuccess\e[0m"
    cd openvino/tools/
    python3 -m pip install benchmark_tool/
    echo -e "\e[1;32mbenchmark-tool installed\e[0m"
    
fi

