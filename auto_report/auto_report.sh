#!/bin/bash

CONTAINER=$1
DATA_INPUT_DIR=$2
DATA_OUTPUT_DIR=$3
PDF_CONFIG=$4

mkdir $DATA_EXPORT_DIR
docker exec auto_report ./make_report.sh $DATA_INPUT_DIR $PDF_CONFIG
docker cp $CONTAINER:temp/export/. $DATA_OUTPUT_DIR

echo "PDF Generated!"
echo "You can find the PDF at $DATA_OUTPUT_DIR"

# ./auto_report.sh auto_report test/input test/output a