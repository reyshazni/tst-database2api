FROM python:3.8-alpine

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

RUN pip install geopy #need to be installed outide requirements.txt

EXPOSE 8000

CMD [ "uvicorn", "main:app" ]