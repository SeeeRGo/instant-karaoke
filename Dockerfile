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
ARG BASE=seeergo/karaoke-maker:0.1-base

FROM ${BASE}

RUN apt-get install -y wget
RUN wget https://openaipublic.azureedge.net/main/whisper/models/81f7c96c852ee8fc832187b0132e569d6c3065a3252ed18e56effd0b6a73e524/large-v2.pt -P /root/.cache/whisper
COPY . /project
WORKDIR /project
RUN mkdir output
CMD ["flask", "run", "--host=0.0.0.0"]
# SHELL ["/bin/bash", "-c"]
