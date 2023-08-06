#!/bin/bash

if [[ $(which docker) && $(docker --version) ]]; then
      echo "Docker is present in the system"
else
        echo "Please install Docker, DockerCE, and Docker compose"
        exit 0
fi

result=$( sudo docker images -q dlstreamer-pipeline-server-gstreamer )

if [[ -n "$result" ]]; then
	echo "dlstreamer-pipeline-server-gstreamer docker image is present"
else
	echo "dlstreamer-pipeline-server-gstreamer docker image is not present. Please run installation script"
	exit 0
fi


USER=/home/intel
DIR=$USER/pipeline-server

if [ -d "$DIR" ]; then
	cd $DIR
	./docker/run.sh -v /tmp:/tmp	
else
        echo "Folder doesnot exist. Please install the package first."
fi

