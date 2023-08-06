#!/bin/bash

# Copyright (C) 2018-2021 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

echo $1
if [ "$(echo "intel123" | sudo docker ps -q -f name=^influxdb$)" ]; then
    echo "Stoping and Deleting System-Telemetry service"
    export HOST_IP=$(hostname -I | cut -d' ' -f1)
    if [ $1=="all-services" ]; then
        python_path=$(python3 -m site --user-site)	    
        sudo -E docker-compose -f $python_path/src/scripts/app-services/system-telemetry/docker-compose-app-service.yaml stop influxdb grafana collectd
	sudo docker rm -f $(sudo docker ps -aq)
    else
	python_path=$(python3 -m site --user-site)
        sudo -E docker-compose -f $python_path/src/scripts/app-services/system-telemetry/docker-compose-app-service.yaml stop $1
    fi
else
    echo "System-Telemetry is not running"
    echo -e "To start run command: '\e[1;3;4;33mdc app-services system-telemetry start $1\e[0m'"
fi
