FROM python:3.8-alpine

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir --upgrade -r requirements.txt

RUN pip install geopy #need to be installed outide requirements.txt

EXPOSE 8000

CMD [ "python", "main.py" ]