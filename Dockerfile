FROM python:3.8

WORKDIR /code/

RUN apt update

COPY requirements.txt .
COPY requirements/dev.txt requirements/dev.txt

RUN pip install --upgrade pip && pip install -r requirements.txt
