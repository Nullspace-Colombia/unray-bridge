FROM ubuntu:20.04
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install -y python3.9 python3-pip

# RUN apt-get update && apt-get install --no-install-recommends -y python3.9 python3.9-dev python3.9-venv python3-pip python3-wheel build-essential && \
#    apt-get clean && rm -rf /var/lib/apt/lists/*
COPY requirements.txt ./
COPY . ./unray

RUN pip install --no-cache-dir -r requirements.txt
RUN cd unray && ./install
RUN mkdir ./unray-config && cd unray-config && mkdir envs && mkdir config && cd envs
COPY ./unray-config ./unray-config

ENV DASHBOARD_DIR "/unray/unray-dashboard"
ENV UNRAY_CONFIG_DIR "/unray-config"

EXPOSE 8000




