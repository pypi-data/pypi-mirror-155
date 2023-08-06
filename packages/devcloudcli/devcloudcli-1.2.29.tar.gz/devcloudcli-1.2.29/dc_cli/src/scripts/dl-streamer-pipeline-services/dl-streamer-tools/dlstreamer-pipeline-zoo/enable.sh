#!/bin/bash
USER=/home/intel

cd $USER
DIR=$PWD/pipeline-zoo

if [[ $(which docker) && $(docker --version) ]]; then
      echo "Docker is present in the system"
else
        echo "Please install Docker, DockerCE, and Docker compose"
        exit 0
fi


if [ -d "$DIR" ]; then
    echo "Success"
    sudo ./pipeline-zoo/tools/docker/run.sh
    echo "You have successfully lauched Pipeline zoo"
    echo "-- To list pipelines, run: pipebench list"
    echo "-- To download pipeline, run: pipebench download od-h264-ssd-mobilenet-v1-coco"
    echo "-- Measure Single Stream Throughput, run: pipebench run od-h264-ssd-mobilenet-v1-coco"
    echo "-- Measure Stream Density, run: pipebench run --measure density od-h264-ssd-mobilenet-v1-coco"
else
    echo " Error: ${DIR} not found. Please run installation script."
fi
