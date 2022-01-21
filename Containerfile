# Dockerfile

# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
# FROM registry.access.redhat.com/ubi8/python-38:1-68 <<< 3.10 required
# for use of the match/case syntax
#FROM python:3.10.1-alpine AS builder
FROM python:3.10.1-alpine

# User nobody has id 65534 and is used to address running as non-root
# within an OpenShift environment

WORKDIR /opt/app-root/src

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1
ENV CRYPTOGRAPHY_DONT_BUILD_RUST 1

#COPY requirements.txt .
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev libffi-dev \
    && apk add --no-cache mariadb-dev make
RUN pip install -U pip

# Allows docker to cache installed dependencies between builds
COPY requirements.txt /opt/app-root/src
RUN pip install -r requirements.txt

# Mounts the application code to the image
COPY . /opt/app-root/src
#RUN python manage.py migrate

RUN apk del build-deps

#FROM python:3.10.1-alpine

#COPY --from=builder . /opt/app-root/src

EXPOSE 8000

# runs the production server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
