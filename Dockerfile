FROM python:3.7-slim-buster

RUN apt-get update
RUN apt-get install build-essential -y

COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY app/ /app

WORKDIR /app

ENTRYPOINT ["sh","gunicorn.sh"]