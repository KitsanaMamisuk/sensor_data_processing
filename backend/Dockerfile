FROM python:3.13

ENV PYTHONUNBUFFERED 1
ENV TZ=Asia/Bangkok
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update
RUN apt-get install -y \
    telnet \
    gettext \
    build-essential \
    python3-dev \
    python3-pip \
    python3-setuptools \
    python3-wheel \
    python3-cffi \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    shared-mime-info \
    ghostscript \
    python3-distutils \
    libjpeg-dev \
    zlib1g-dev \
    libfreetype6-dev 

ENV PROJECT_ROOT /opt/app
RUN mkdir -p $PROJECT_ROOT
WORKDIR $PROJECT_ROOT

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./apps /opt/app/apps
COPY ./configs /opt/app/configs
COPY ./manage.py /opt/app
