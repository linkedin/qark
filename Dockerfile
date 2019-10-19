FROM python:3.6-alpine
RUN apk add --no-cache \
    build-base \
    libffi-dev \
    openssl-dev \
    openjdk8-jre
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
RUN pip install .
