FROM python:latest
ARG DEBIAN_FRONTEND=noninteractive
RUN pip3 install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY flask-project /usr/local/bin/flask-project
CMD python3 /usr/local/bin/flask-project/app.py
