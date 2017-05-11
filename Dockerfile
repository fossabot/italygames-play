FROM python:2.7

RUN mkdir /web
WORKDIR /web

COPY requirements.txt /web
RUN pip install --no-cache-dir -r /web/requirements.txt
COPY . /web

ENV FLASK_CONFIG=development
ENV FLASK_APP=run.py

CMD ["flask", "run", "--host=0.0.0.0"]
