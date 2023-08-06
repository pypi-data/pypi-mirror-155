#!/bin/bash
INTEL_OPENVINO_DIR=/opt/intel/openvino_2021
INPUT_VIDEO=https://github.com/intel-iot-devkit/sample-videos/raw/master/head-pose-face-detection-female-and-male.mp4
METHOD=mqtt
OUTPUT="localhost:1883"
TOPIC=dlstreamer
USER=/home/intel
DIR=$USER/dlstreamer

if [ -d "$DIR" ]; then
    echo "Success"
    export MODELS_PATH=$USER
    source $INTEL_OPENVINO_DIR/bin/setupvars.sh
    cd $DIR/samples/gst_launch/metapublish/
    #./metapublish.sh $INPUT_VIDEO $METHOD $OUTPUT $TOPIC 
    ./metapublish.sh $INPUT_VIDEO
else
    echo " Error: ${DIR} not found. Please run installation script."
fi
