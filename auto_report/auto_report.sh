#!/bin/bash

CONTAINER=$1
DATA_INPUT_DIR=$2
DATA_OUTPUT_DIR=$3
PDF_CONFIG=$4

mkdir "$DATA_OUTPUT_DIR"
docker exec $CONTAINER sh -c "rm -r docker/import/*"
docker cp "$DATA_INPUT_DIR" $CONTAINER:docker/import/. 
docker exec $CONTAINER ./make_report.sh $PDF_CONFIG
docker cp $CONTAINER:docker/export/. "$DATA_OUTPUT_DIR"
docker exec $CONTAINER sh -c "rm -rf docker/export/*"

echo "PDF Generated!"
echo "You can find the PDF at $DATA_OUTPUT_DIR"
