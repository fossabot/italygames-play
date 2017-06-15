FROM python:2.7

RUN mkdir /web
WORKDIR /web

COPY requirements.txt /web
RUN pip install --no-cache-dir -r /web/requirements.txt
COPY . /web

CMD ["python", "manage.py", "gunicorn", "-h", "0.0.0.0"]
