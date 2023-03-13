FROM python:3.11-alpine
MAINTAINER Pedram P

ENV PYTHONUNBUFFERED 1
copy ./requirments.txt /requirments.txt
run pip install -r /requirments.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser -D user
USER user