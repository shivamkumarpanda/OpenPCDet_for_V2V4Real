#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <cfg_file> <data_path> <ckpt>"
    exit 1
fi

CFG_FILE=$1
DATA_PATH=$2
CKPT=$3

# Start Xvfb
Xvfb :1 -screen 0 800x600x24 &

# Set the DISPLAY environment variable
export DISPLAY=:1

# Run the Python script with the provided arguments
python tools/demo.py --cfg_file $CFG_FILE --data_path $DATA_PATH --ckpt $CKPT

# Kill Xvfb after the script is done
kill %1
