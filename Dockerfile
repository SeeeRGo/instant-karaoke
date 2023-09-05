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
ARG BASE=python:3.10-slim

FROM ${BASE}

ARG SPLEETER_VERSION=2.4.0
ENV MODEL_PATH /model

RUN mkdir -p /model
RUN apt-get update && apt-get install -y ffmpeg libsndfile1 build-essential libcairo2-dev libpango1.0-dev
RUN pip install musdb museval manim spleeter==2.4.0 click==7.1.2 openai-whisper jellyfish python-dotenv flask_cors supabase flask==2.0.1 --no-cache-dir
COPY . /project
RUN rm -rf /root/.cache
WORKDIR /project
RUN mkdir output
CMD ["flask", "run", "--host=0.0.0.0"]
# SHELL ["/bin/bash", "-c"]
