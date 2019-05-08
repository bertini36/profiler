FROM python:3.7

ARG REQUIREMENTS

WORKDIR /code/

RUN apt update

COPY requirements.txt ${REQUIREMENTS} /code/

RUN pip3 install --upgrade pip \
 && pip3 install -r ${REQUIREMENTS}

COPY . /code/
