#!/bin/bash
INTEL_OPENVINO_DIR=/opt/intel/openvino_2021
INPUT_VIDEO=https://github.com/intel-iot-devkit/sample-videos/raw/master/face-demographics-walking.mp4
SINK_ELEMENT=fps
DEVICE=CPU
USER=/home/intel
DIR=$USER/dlstreamer

if [ -d "$DIR" ]; then
    echo "Success"
    export MODELS_PATH=$USER
    source $INTEL_OPENVINO_DIR/bin/setupvars.sh
    cd $DIR/samples/gst_launch/human_pose_estimation/
    ./human_pose_estimation.sh $INPUT_VIDEO $DEVICE $SINK_ELEMENT 
else
    echo " Error: ${DIR} not found. Please run installation script."
fi
