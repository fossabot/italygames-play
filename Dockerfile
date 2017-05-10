FROM debian:jessie

RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential libmysqlclient-dev

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

ENV FLASK_CONFIG=development
ENV FLASK_APP=run.py

ENTRYPOINT ["flask", "run", "--host=0.0.0.0"]
