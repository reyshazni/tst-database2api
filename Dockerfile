FROM python:3.8-alpine

WORKDIR /app

ADD . /app

RUN pip install geopy

CMD [ "python", "distance.py" ]