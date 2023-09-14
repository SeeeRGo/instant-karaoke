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
ARG BASE=seeergo/karaoke-maker:0.4-base

FROM ${BASE}

# # RUN apt-get install -y wget
# # RUN wget https://openaipublic.azureedge.net/main/whisper/models/81f7c96c852ee8fc832187b0132e569d6c3065a3252ed18e56effd0b6a73e524/large-v2.pt -P /root/.cache/whisper
COPY . /project
WORKDIR /project
ARG PORT=5000
RUN pip install supabase==1.0.4 gunicorn
# RUN apt install -y openssl
RUN mkdir output
CMD flask run --host=0.0.0.0
# # SHELL ["/bin/bash", "-c"]
###########
# BUILDER #
###########

# # pull base image
# ARG BASE=seeergo/karaoke-maker:0.4-base

# FROM ${BASE} as builder

# # set work directory
# WORKDIR /usr/src/app

# # set environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# # install system dependencies

# # lint
# RUN pip install --upgrade pip
# RUN pip install flake8==6.0.0 supabase>=1.0.0
# COPY . /usr/src/app/
# RUN mkdir output
# # RUN flake8 --ignore=E501,F401 .

# # install python dependencies
# # COPY ./requirements.txt .
# RUN pip freeze > requirements.txt
# RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt


# #########
# # FINAL #
# #########

# # pull official base image
# FROM ${BASE}
# # create directory for the app user
# RUN mkdir -p /home/app

# # create the app user
# RUN addgroup --system app && adduser --system --group app

# # create the appropriate directories
# ENV HOME=/home/app
# ENV APP_HOME=/home/app/web
# RUN mkdir $APP_HOME
# WORKDIR $APP_HOME

# # install dependencies
# RUN apt-get update && apt-get install -y netcat-openbsd gunicorn
# COPY --from=builder /usr/src/app/wheels /wheels
# # COPY --from=builder /usr/src/app/requirements.txt .
# RUN pip install --upgrade pip
# RUN pip install --no-cache /wheels/*

# # copy entrypoint-prod.sh
# COPY ./entrypoint.prod.sh $APP_HOME

# # copy project
# COPY . $APP_HOME

# # chown all the files to the app user
# RUN chown -R app:app $APP_HOME

# # change to the app user
# USER app

# # run entrypoint.prod.sh
# ENTRYPOINT ["/bin/bash"]