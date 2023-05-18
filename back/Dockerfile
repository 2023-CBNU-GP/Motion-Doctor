# Use an official Python runtime as the base image
FROM python:3.7
MAINTAINER choheejin

ENV PYTHONUNBUFFERED 1

COPY requirements.txt /requirements.txt

RUN pip install --upgrade pip
RUN pip install -r /requirements.txt

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install -r requirements.txt
RUN mkdir /usr/src/app/media
COPY . .

EXPOSE 8000


CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "back.asgi:application"]