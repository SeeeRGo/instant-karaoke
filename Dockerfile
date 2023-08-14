# ARG BASE=python:3.7
# FROM ${BASE}

# RUN apt-get update --fix-missing \
#     && apt-get install -y wget bzip2 ca-certificates curl git \
#     && apt-get clean \
#     && rm -rf /var/lib/apt/lists/* \
#     && wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-4.6.14-Linux-x86_64.sh -O ~/miniconda.sh \
#     && /bin/bash ~/miniconda.sh -b -p /opt/conda \
#     && rm ~/miniconda.sh \
#     && /opt/conda/bin/conda clean -tipsy \
#     && ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh \
#     && echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc \
#     && echo "conda activate base" >> ~/.bashrc \
#     && ln -s /opt/conda/bin/conda /usr/bin/conda
# SHELL ["/bin/bash", "-c"]
ARG BASE=python:3.9

FROM ${BASE}

ARG SPLEETER_VERSION=2.4.0
ENV MODEL_PATH /model

RUN mkdir -p /model
RUN apt-get update && apt-get install -y ffmpeg libsndfile1
RUN pip install musdb museval
RUN pip install spleeter==${SPLEETER_VERSION}
RUN apt install -y build-essential python3-dev libcairo2-dev libpango1.0-dev
RUN pip install manim
RUN pip install -U openai-whisper
RUN pip uninstall -y click
RUN pip install click==7.1.2
SHELL ["/bin/bash", "-c"]