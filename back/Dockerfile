# Use an official Python runtime as the base image
FROM python:3.7-alpine
MAINTAINER choheejin

ENV PYTHONUNBUFFERED 1

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

WORKDIR /usr/src/app
COPY back .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]