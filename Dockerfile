FROM debian:buster-slim
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get -y update && apt-get -y install python3 python3-pip curl procps
RUN pip3 install --upgrade pip && pip3 install flask
COPY app.py /usr/local/bin/app.py
CMD app.py