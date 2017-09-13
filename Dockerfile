FROM phusion/baseimage

RUN mkdir -p /app
WORKDIR /app
RUN apt-get update && apt-get install -qy python3 python3-dev python3-pip libffi-dev libxml2-dev libxslt-dev lib32z1-dev libssl-dev
ADD ./requirements.txt /app
RUN pip3 install -r requirements.txt