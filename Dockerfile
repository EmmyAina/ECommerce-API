FROM python:3.8

ENV PYTHONUNBUFFERED 1

WORKDIR /ecommerce-api
COPY requirements.txt /ecommerce-api/requirements.txt
RUN pip install -r requirements.txt
COPY . /ecommerce-api

EXPOSE  8000
