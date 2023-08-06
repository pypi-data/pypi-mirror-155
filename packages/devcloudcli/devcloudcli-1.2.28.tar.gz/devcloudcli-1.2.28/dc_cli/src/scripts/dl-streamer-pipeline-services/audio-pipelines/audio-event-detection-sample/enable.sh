#!/bin/bash
INTEL_OPENVINO_DIR=/opt/intel/openvino_2021
USER=/home/intel
DIR=$USER/dlstreamer

if [ -d "$DIR" ]; then
    echo "Success"
    source $INTEL_OPENVINO_DIR/bin/setupvars.sh
    export MODELS_PATH=$USER
    cd $DIR/samples/gst_launch/audio_detect
    INPUT_PATH=$PWD/how_are_you_doing.wav
    ./audio_event_detection.sh $INPUT_PATH
else
    echo " Error: ${DIR} not found. Please run installation script."
fi
