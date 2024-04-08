#!/bin/bash

id=$1
data_input_dir=$2
docker=$3

if [ "$docker" = "true" ]; then
    BASE_PATH="."
else
    BASE_PATH="./auto_report"
fi

HASH_GENERATOR_PATH="$BASE_PATH/src/utils/hash_generator.py"
MAIN_PY_PATH="$BASE_PATH/__main__.py"

# Check if hash_generator.py exists
if [ ! -f "$HASH_GENERATOR_PATH" ]; then
    echo "Error: hash_generator.py not found at $HASH_GENERATOR_PATH"
    exit 1
fi

# Generate hash
hash=$(python3 "$HASH_GENERATOR_PATH" "--id=$id")

# Set data_output_dir based on the generated hash
if [ "$docker" = "true" ]; then
    data_output_dir="./data/temp/$hash/"
    pdf_output_dir="./data/results/$hash/"
else
    data_output_dir="./auto_report/data/temp/$hash/"
    pdf_output_dir="./auto_report/data/results/$hash/"
fi

echo "$hash $data_output_dir $pdf_output_dir"

# Check if __main__.py exists
if [ ! -f "$MAIN_PY_PATH" ]; then
    echo "Error: __main__.py not found at $MAIN_PY_PATH"
    exit 1
fi

if [[ -z $data_input_dir ]]; then
    echo "No arguments have been provided."
else
    echo "The argument provided is: $hash and $data_input_dir"

    echo "Creating the temporary directory $data_output_dir"
    mkdir -p $data_output_dir
    mkdir -p $pdf_output_dir

    if [ -d "$data_input_dir" ]; then
        cp -R $data_input_dir/* $data_output_dir
        echo "The folder has been copied successfully."
    else
        echo "The source folder does not exist."
    fi

    echo "Initializing Python script with docker=$docker"
    python3 "$MAIN_PY_PATH" "--data_dir=$data_output_dir" "--hash=$hash" "--docker=$docker"

    # echo "Moving the generated file to results folder"
    # mv "$data_output_dir/report.pdf" "./auto_report/data/results"

    # echo "Removing the temporary directory $data_output_dir"
    # rm -rf $data_output_dir


fi