# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED=True

WORKDIR /code_pcentra

COPY requirements.txt /code_pcentra/

RUN pip install -r requirements.txt

RUN apt-get -y upgrade


COPY . /code_pcentra/
