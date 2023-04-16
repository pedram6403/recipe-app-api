FROM python:3.11-alpine
MAINTAINER Pedram P

ENV PYTHONUNBUFFERED 1
copy ./requirments.txt /requirments.txt
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps gcc libc-dev linux-headers postgresql-dev
RUN pip install -r /requirments.txt
RUN apk del .tmp-build-deps

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser -D user
USER user