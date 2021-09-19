# syntax=docker/dockerfile:1
FROM python:3-slim
RUN apt-get update
RUN pip install --upgrade pip
RUN mkdir bot
WORKDIR /bot
COPY . /bot
RUN pip install -r requirements.txt
CMD python main.py