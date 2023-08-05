#!/bin/bash
INTEL_OPENVINO_DIR=/opt/intel/openvino_2021
INPUT_VIDEO=https://github.com/intel-iot-devkit/sample-videos/raw/master/head-pose-face-detection-female-and-male.mp4

USER=/home/intel
DIR=$USER/dlstreamer

if [ -d "$DIR" ]; then
	cd $USER
	wget $INPUT_VIDEO
	cd $DIR
        source $INTEL_OPENVINO_DIR/bin/setupvars.sh
        gst-launch-1.0 filesrc location=$USER/head-pose-face-detection-female-and-male.mp4 ! decodebin ! videoconvert ! gvadetect model=$USER/intel/face-detection-adas-0001/FP16/face-detection-adas-0001.xml ! gvaclassify model=$USER/intel/emotions-recognition-retail-0003/FP16/emotions-recognition-retail-0003.xml model-proc=$DIR/samples/gst_launch/metapublish/model_proc/emotions-recognition-retail-0003.json ! gvawatermark ! autovideosink sync=false
else
         echo "Folder does not exist. Please install the package first."
         
fi

