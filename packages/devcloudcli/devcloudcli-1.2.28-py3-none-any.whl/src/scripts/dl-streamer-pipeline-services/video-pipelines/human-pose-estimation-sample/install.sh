#!/bin/bash
INTEL_OPENVINO_DIR=/opt/intel/openvino_2021

sudo chmod 777 /etc/environment
sudo echo "http_proxy=http://proxy-dmz.intel.com:911
https_proxy=http://proxy-dmz.intel.com:911
HTTP_PROXY=http://proxy-dmz.intel.com:911
HTTPS_PROXY=http://proxy-dmz.intel.com:911
ftp_proxy=http://proxy-dmz.com:911
NO_PROXY=localhost,127.0.0.1                                                                                            no_proxy=localhost,127.0.0.1" > /etc/environment                                                                        

source /etc/environment
export no_proxy="localhost,127.0.0.1"

if [ -d "$INTEL_OPENVINO_DIR" ]; then
        echo "OpenVINO toolkit is already installed"
else
        wget https://registrationcenter-download.intel.com/akdlm/irc_nas/18319/l_openvino_toolkit_p_2021.4.752.tgz
        sudo apt-get update
        sudo apt-get install cpio
        tar -xvzf l_openvino_toolkit_p_2021.4.752.tgz
        cd l_openvino_toolkit_p_2021.4.752
        sed -i 's/decline/accept/g' silent.cfg
        sudo ./install.sh -s silent.cfg
        cd /opt/intel/openvino_2021/install_dependencies
        sudo -E ./install_openvino_dependencies.sh
	echo "Successfully installed OpenVINO toolkit"
fi

USER=/home/intel
cd $USER
MODEL_PATH=$PWD/
DIR=$PWD/dlstreamer
if [ -d "$DIR" ]; then
        echo "Success"
else
    git clone https://github.com/dlstreamer/dlstreamer.git
fi
export INTEL_OPENVINO_DIR=$INTEL_OPENVINO_DIR
export MODELS_PATH=$MODEL_PATH
pip3 install numpy networkx onnx
pip3 install -r $INTEL_OPENVINO_DIR/deployment_tools/open_model_zoo/tools/downloader/requirements.in
cd $DIR/samples
sh ./download_models.sh

