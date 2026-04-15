#!/bin/bash

PROJ_DIR=$(pwd)
DATA_DIR="$PROJ_DIR/data"
ASSET_DIR="$PROJ_DIR/assets"

rm -rf $ASSET_DIR

cd tools/asset-extraction

find $DATA_DIR -type f -printf "%P\n" | while read -r line;do
    if [[ "$line" == *.bin || "$line" == *.srl || "$line" == *.char || "$line" == *.sdat || "$line" == *.plt ]]; then
        echo "Skipping $line ..."
        continue
    fi
    echo "Processing $line ..."
    mkdir -p $ASSET_DIR/$line
    python3 narc_extract.py $DATA_DIR/$line $ASSET_DIR/$line > $ASSET_DIR/$line/narc_info.txt   
done

cd ../../