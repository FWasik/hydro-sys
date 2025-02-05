FROM python:3.13.0-alpine

WORKDIR /app/hydro-sys

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /app/hydro-sys

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt