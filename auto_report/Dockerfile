FROM python:3.10-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install TinyTeX
RUN wget -qO- "https://yihui.org/tinytex/install-bin-unix.sh" | sh \
    && /root/.TinyTeX/bin/*/tlmgr path add

# Add TinyTeX to the PATH
ENV PATH="/root/.TinyTeX/bin/x86_64-linux:${PATH}"

# Install required TeX Live packages
RUN tlmgr install koma-script fancyhdr wrapfig tcolorbox adjustbox changepage caption pgf ocgx2 pdfrender stackengine environ fourier background everypage grfext

RUN mkdir -p /root/.TinyTeX/texmf-local/tex/latex/local \
    && wget -O /root/.TinyTeX/texmf-local/tex/latex/local/pdfbase.sty "https://mirrors.ctan.org/macros/latex/contrib/media9/pdfbase.sty" \
    && mktexlsr

RUN apt-get update && apt-get install -y
RUN apt-get install unzip
COPY . /

RUN pip install --no-cache-dir -r requirements.txt
RUN chmod +x ./make_report.sh
