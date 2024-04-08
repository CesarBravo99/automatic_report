#!/bin/bash

BASE_PATH="$(realpath --relative-to="$(pwd)" "$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )")"

sudo apt update
sudo apt-get install texlive-lang-english -y
sudo apt-get install texmaker -y
sudo apt-get install texlive-fonts-extra -y

sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys D6BC243565B2087BC3F897C9277A7293F59E4889
echo "deb http://miktex.org/download/ubuntu bionic universe" | sudo tee /etc/apt/sources.list.d/miktex.list
sudo apt-get update
sudo apt-get install miktex


sudo apt install python3 python3-dev python3-venv -y
sudo apt-get install wget
wget https://bootstrap.pypa.io/get-pip.py
sudo python3 get-pip.py
pip install --no-cache-dir -r $BASE_PATH/requirements.txt

chmod +x $BASE_PATH/make_report.sh