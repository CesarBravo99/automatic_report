#!/bin/bash

ID=$1
DATA_INPUT_DIR=$2
PDF_CONFIG=$3
# PDF_EXPORT_DIR=$4

BASE_PATH="$(realpath --relative-to="$(pwd)" "$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )")"
MAIN_PY_PATH="$BASE_PATH/__main__.py"
HASH_GENERATOR_PATH="$BASE_PATH/src/utils/hash_generator.py"
HASH=$(python3 "$HASH_GENERATOR_PATH" "--id=$ID")
DATA_IMPORT_DIR="$BASE_PATH/content/import/$HASH/"
PDF_EXPORT_DIR="$BASE_PATH/content/export/$HASH/"

mkdir $DATA_IMPORT_DIR
mkdir $PDF_EXPORT_DIR

if [ -d "$DATA_INPUT_DIR" ]; then
    cp -R $DATA_INPUT_DIR/* $DATA_IMPORT_DIR
    echo "The input folder has been copied successfully."
    echo "Running the script with the following arguments:"
    echo "user_id: $ID"
    echo "Form Hash: $HASH"
    echo "data_input_dir: $DATA_INPUT_DIR"
    echo "report_output_path: $PDF_EXPORT_DIR"
    python3 "$MAIN_PY_PATH" "--root=$BASE_PATH" "--imported_data_dir=$DATA_IMPORT_DIR" "--exported_data_dir=$PDF_EXPORT_DIR" "--pdf_config=$PDF_CONFIG" "--hash=$HASH"

    # echo "Moving the generated file to results folder"
    # mv "$data_output_dir/report.pdf" "./auto_report/data/results"

    # echo "Removing the temporary directory $data_output_dir"
    # rm -rf $data_output_dir

    echo "PDF Generated!"
    echo "You can find the PDF at $PDF_EXPORT_DIR"

else
    echo "The source folder does not exist."
fi
