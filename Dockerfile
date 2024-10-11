FROM python:3.12.7-slim-bullseye
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /tmp/requirements.txt

RUN python -m venv /opt/env && \
    pip install --upgrade pip &&\
    apt-get update && \
    apt-get install -y\
        gcc libpq-dev musl-dev && \ 
    pip install -r /tmp/requirements.txt &&\
    rm -rf /tmp && \
    rm -rf /var/lib/apt/lists/* && \
    adduser \
        --disabled-password \
        --no-create-home \
        server-user

COPY ./src /app
WORKDIR /app
