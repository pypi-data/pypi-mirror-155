#!/bin/bash

USER=/home/intel

cd $USER
DIR=$PWD/gst-shark
OPTIONS="--prefix /usr/ --libdir /usr/lib/x86_64-linux-gnu/"
if [ -d "$DIR" ]; then
        echo "Success"
else
    git clone https://github.com/RidgeRun/gst-shark/
fi
if [ "$(gst-launch-1.0 --version)" -lt 1.7.1 ]; then
    echo "gst-lauch-1.0 version should be greater than 1.7.1"
    exit 1
else
    echo "Sucess. gst-launch-1.0 version matches."
    sudo apt install libgstreamer1.0-dev 
    sudo apt install graphviz libgraphviz-dev
    sudo apt install octave epstool babeltrace
    sudo apt-get install gtk-doc-tools
    cd $DIR
    ./autogen.sh $OPTIONS
    make
    sudo make install
    echo "Successfully installed Gst-Shark."
fi
