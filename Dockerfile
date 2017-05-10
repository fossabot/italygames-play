FROM python:2.7

COPY . /web
WORKDIR /web

RUN pip install -r requirements.txt

ENV FLASK_CONFIG=development
ENV FLASK_APP=run.py

CMD ["flask", "run", "--host=0.0.0.0"]
