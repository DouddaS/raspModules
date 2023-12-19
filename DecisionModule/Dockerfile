#!/bin/bash
FROM arm32v7/python:3.7-slim-buster
# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

ARG ARCH=arm32v7

COPY requirements.txt /requirements.txt
RUN pip install -r requirements.txt
EXPOSE 1092
COPY . /.
CMD ["python","-u","app.py"]
