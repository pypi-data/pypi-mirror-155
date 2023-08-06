#!/bin/bash
# Copyright (C) 2018-2021 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

#Installing Cluster-Telemetry
echo "Installing Cluster-Telemetry"

echo $
if [ "$(echo "intel123" | sudo docker ps -q -f name=^prometheus$)" ]; then
    echo "Cluster-Telemetry already running"
    echo -e "To stop run command: '\e[1;3;4;33mdc app-services cluster-telemetry stop $1\e[0m'"
else
    echo "Installing Cluster-Telemetry service"
    export HOST_IP=$(hostname -I | cut -d' ' -f1)
    python_path=$(python3 -m site --user-site)
    if [ $1=="all-services" ]; then      
         sudo -E docker-compose -f $python_path/src/scripts/app-services/cluster-telemetry/docker-compose-app-service.yaml  up -d --build grafana prometheus node-exporter    
    fi
fi

echo "\nIf cluster-telemetry is working fine.Then check metrics by using Grafana"

echo -e "\e[1;32m\n********* Grafana URL **************\e[0m"
echo -e "\e[1;36mGrafana Dashboard is available in the below URL\e[0m"
echo -e "\e[1;33mhttp://$HOST_IP:3000 \e[0m\n"
