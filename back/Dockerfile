# Use an official Python runtime as the base image
FROM python:3.7-alpine
MAINTAINER choheejin

ENV PYTHONUNBUFFERED 1

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .

# 원하는 포트를 열어준다. runserver가 8000번을 default로 쓰기때문에 8000번을 열어줌
EXPOSE 8000

# manage.py가 있는 directory로 이동한 후에 runesrver 실행
# manage.py가 dockerfile과 같은 dir에 있으면 따로 WORKDIR를 지정할 필요는 없다.
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]