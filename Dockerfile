# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.9-buster

# The environment variable ensures that the python output is set straight
# to the terminal with out buffering it first
# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y apt-utils && apt-get -y install sudo
RUN apt-get install -y python3-dev  \
    && apt-get install -y gcc  \
    && apt-get install -y virtualenv

SHELL ["/bin/bash", "-c"]

ENV HOME_DIR "/app"
ENV PROJECT_DIR "$HOME_DIR/app"
ENV VENV_DIR "$HOME_DIR/venv"
RUN export PATH="$HOME_DIR/.local/bin:$PATH"

WORKDIR $PROJECT_DIR

# Copy in your requirements file
ADD requirements.txt /tmp/requirements.txt

RUN virtualenv $VENV_DIR

RUN $VENV_DIR/bin/pip install --upgrade pip

COPY ./requirements.txt /tmp/
RUN $VENV_DIR/bin/pip install -r /tmp/requirements.txt

COPY . .

ENTRYPOINT cd $PROJECT_DIR/project && PYTHONPATH=$PROJECT_DIR:$PYTHONPATH $VENV_DIR/bin/app -A 'app:python_app'  --port=80
