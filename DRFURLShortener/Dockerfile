# syntax=docker/dockerfile:1

FROM python:3.10-slim-buster

ENV PYTHONUNBUFFERED=True

WORKDIR /code_urlshortener

COPY requirements.txt /code_urlshortener/

RUN pip install -r requirements.txt

RUN apt-get -y upgrade


COPY . /code_urlshortener/
