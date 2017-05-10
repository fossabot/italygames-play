FROM python:2.7

#RUN apt-get update -y
#RUN apt-get install -y python-pip python-dev build-essential libmysqlclient-dev

COPY . /web
WORKDIR /web

RUN pip install -r requirements.txt

ENV FLASK_CONFIG=development
ENV FLASK_APP=run.py

#ENTRYPOINT ["flask", "run", "--host=0.0.0.0"]
CMD ["flask", "run", "--host=0.0.0.0"]
