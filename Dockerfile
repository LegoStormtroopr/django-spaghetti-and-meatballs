FROM python:3.8-buster

# Install python package management tools
RUN pip install --upgrade setuptools pip poetry

COPY ./* /usr/src/app/
WORKDIR /usr/src/app

ENV PYTHONPATH=/usr/src/app/django_spaghetti DJANGO_SETTINGS_MODULE=tests.settings
