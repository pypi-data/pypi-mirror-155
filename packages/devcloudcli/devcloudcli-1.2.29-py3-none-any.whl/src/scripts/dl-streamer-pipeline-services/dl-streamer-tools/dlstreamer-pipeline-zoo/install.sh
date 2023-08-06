#!/bin/bash

USER=/home/intel

cd $USER
DIR=$PWD/pipeline-zoo
MODEL_PATH=$PWD

if [[ $(which docker) && $(docker --version) ]]; then
      echo "Docker is present in the system"
else
        echo "Please install Docker, DockerCE, and Docker compose"
        exit 0
fi

if [ -d "$DIR" ]; then
	echo "Success"
else
    git clone https://github.com/dlstreamer/pipeline-zoo.git pipeline-zoo
fi
cd pipeline-zoo/tools/docker/
sudo ./build.sh 



