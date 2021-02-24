FROM python:3.8

WORKDIR /srv
COPY requirements.txt /srv/
RUN pip install -r requirements.txt
COPY . /srv/
RUN apt-get update && apt-get install -y wkhtmltopdf xvfb
