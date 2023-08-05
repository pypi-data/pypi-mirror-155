#!/bin/bash
# Copyright (C) 2018-2021 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

echo $
if [ "$(echo "intel123" | sudo docker ps -q -f name=^cadvisor$)" ]; then
    echo "Docker-Telemetry already running"
    echo -e "To stop run command: '\e[1;3;4;33mdc app-services docker-telemetry stop  $1\e[0m'"
else
    echo "Installing Docker-Telemetry service"
    export HOST_IP=$(hostname -I | cut -d' ' -f1)
    python_path=$(python3 -m site --user-site)
    if [ $1=="all-services" ]; then      
        sudo -E docker-compose -f $python_path/src/scripts/app-services/docker-telemetry/docker-compose-app-service.yaml  up -d --build influxdb grafana cadvisor prometheus    
    fi
fi


echo "If docker-telemetry is working fine.Then check metircs by using Grafana"

echo -e "\e[1;32m\n********* Grafana URL **************\e[0m"
echo -e "\e[1;36mGrafana Dashboard is available in the below URL\e[0m"
echo -e "\e[1;33mhttp://$HOST_IP:3000 \e[0m\n"
