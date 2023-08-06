#!/bin/bash
USER=/home/intel

cd $USER
sudo docker rmi dlstreamer-pipeline-server-gstreamer
sudo rm -rf pipeline-server 
echo "Successfully uninstalled"
