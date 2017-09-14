FROM phusion/baseimage

RUN mkdir -p /app
WORKDIR /app
RUN apt-get update && apt-get install -qy python python-dev python-pip libffi-dev libxml2-dev libxslt-dev lib32z1-dev libssl-dev
ADD ./requirements.txt /app
RUN pip install -r requirements.txt