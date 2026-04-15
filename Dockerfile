# syntax=docker/dockerfile:1

FROM python:3.10.20-alpine

RUN apk update && apk add git

WORKDIR /licheaters

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]