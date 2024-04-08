#!/bin/bash

BASE_PATH="$(realpath --relative-to="$(pwd)" "$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )")"

sudo apt update
sudo apt-get install texlive-lang-english -y
sudo apt-get install texmaker -y
sudo apt install python3 python3-dev python3-venv -y
sudo apt-get install wget
wget https://bootstrap.pypa.io/get-pip.py
sudo python3 get-pip.py
pip install --no-cache-dir -r $BASE_PATH/requirements.txt

chmod +x $BASE_PATH/make_report.sh