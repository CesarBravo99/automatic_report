#!/bin/bash

ID=$1
DATA_INPUT_DIR=$2
PDF_CONFIG=$3
# PDF_EXPORT_DIR=$4




# parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
# cd "$parent_path"
# cd "$(dirname "$0")"

echo "$(pwd)"
pwd1="$(pwd)"
cd "$(dirname "$0")"
pwd2="$(pwd)"
echo "$(realpath --relative-to="${pwd1}" "$pwd2")"
echo "-------------------"
BASE_PATH="$(realpath --relative-to="${pwd1}" "$pwd2")"
BASE_PATH="$(dirname BASE_PATH)"

HASH_GENERATOR_PATH="$BASE_PATH/src/utils/hash_generator.py"
MAIN_PY_PATH="$BASE_PATH/__main__.py"

# Check if hash_generator.py exists
# if [ ! -f "$HASH_GENERATOR_PATH" ]; then
#     echo "Error: hash_generator.py not found at $HASH_GENERATOR_PATH"
#     exit 1
# fi

# Generate hash
HASH=$(python3 "$HASH_GENERATOR_PATH" "--id=$ID")

DATA_IMPORT_DIR="$BASE_PATH/content/import/$HASH/"
PDF_EXPORT_DIR="$BASE_PATH/content/export/$HASH/"

echo "The hash is: $HASH"

# Check if __main__.py exists
if [ ! -f "$MAIN_PY_PATH" ]; then
    echo "Error: __main__.py not found at $MAIN_PY_PATH"
    exit 1
fi

if [[ -z $DATA_INPUT_DIR ]]; then
    echo "No arguments have been provided."
else

    echo "Creating the temporary directory $DATA_IMPORT_DIR" and $PDF_EXPORT_DIR
    mkdir $DATA_IMPORT_DIR
    mkdir $PDF_EXPORT_DIR

    if [ -d "$DATA_INPUT_DIR" ]; then
        cp -R $DATA_INPUT_DIR/* $DATA_IMPORT_DIR
        echo "The input folder has been copied successfully."
        echo "--------------------"
        echo "Generating PDF..."
        echo "--------------------"
        echo "Running the script with the following arguments:"
        echo "user_id: $ID"
        echo "Form Hash: $HASH"
        echo "data_input_dir: $DATA_INPUT_DIR"
        echo "report_output_path: $PDF_EXPORT_DIR"
        echo "--------------------"
        echo "Initializing Python script"
        python3 "$MAIN_PY_PATH" "--root=$BASE_PATH" "--imported_data_dir=$DATA_IMPORT_DIR" "--exported_data_dir=$PDF_EXPORT_DIR" "--pdf_config=$PDF_CONFIG" "--hash=$HASH"

        # echo "Moving the generated file to results folder"
        # mv "$data_output_dir/report.pdf" "./auto_report/data/results"

        # echo "Removing the temporary directory $data_output_dir"
        # rm -rf $data_output_dir


        echo "--------------------"
        echo "PDF Generated!"
        echo "You can find the PDF at $PDF_EXPORT_DIR"
        echo "--------------------"

    else
        echo "The source folder does not exist."
    fi

fi