#!/bin/bash

BASE_PATH="$(realpath --relative-to="$(pwd)" "$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )")"

sudo apt update
# sudo apt-get install texlive-full -y
sudo apt install python3 python3-dev python3-venv -y
sudo apt-get install wget
wget https://bootstrap.pypa.io/get-pip.py
sudo python3 get-pip.py
pip install --no-cache-dir -r $BASE_PATH/requirements.txt

wget -qO- "https://yihui.org/tinytex/install-bin-unix.sh" | sh \
    && /root/.TinyTeX/bin/*/tlmgr path add
tlmgr install koma-script fancyhdr wrapfig tcolorbox adjustbox changepage caption pgf ocgx2 pdfrender stackengine environ fourier background everypage grfext
mkdir -p /root/.TinyTeX/texmf-local/tex/latex/local \
    && wget -O /root/.TinyTeX/texmf-local/tex/latex/local/pdfbase.sty "https://mirrors.ctan.org/macros/latex/contrib/media9/pdfbase.sty" \
    && mktexlsr

chmod +x $BASE_PATH/make_report.sh