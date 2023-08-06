#!/bin/bash

if [[ $(which docker) && $(docker --version) ]]; then
      echo "Docker is present in the system"
else
	echo "Please install Docker, DockerCE, and Docker compose"
	exit 0
fi

USER=/home/intel
cd $USER
DIR=$PWD/pipeline-server
MODEL_PATH=$PWD

if [ -d "$DIR" ]; then
	echo "Success"
else
    git clone https://github.com/dlstreamer/pipeline-server.git
fi

cd $DIR/
./docker/build.sh
echo "dlstreamer-pipeline-server-gstreamer docker image is been created"
docker images dlstreamer-pipeline-server-gstreamer:latest



