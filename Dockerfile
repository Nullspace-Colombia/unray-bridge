FROM devnullspace/unray-base
ENV DEBIAN_FRONTEND noninteractive

COPY . ./unray
RUN cd unray && ./install
RUN mkdir ./unray-config && cd unray-config && mkdir envs && mkdir config && cd envs
COPY ./unray-config ./unray-config

ENV DASHBOARD_DIR "/unray/unray-dashboard"
ENV UNRAY_CONFIG_DIR "/unray-config"

EXPOSE 8000




