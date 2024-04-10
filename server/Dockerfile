# ---- Base python ----
FROM python:3.11-alpine AS base
RUN apt-get update
RUN mkdir /app
WORKDIR /app

# ---- Dependencies ----
FROM base AS dependencies
RUN apk add gcc python-dev postgresql-dev
RUN pip3 install -r requirements.txt


# ---- Release ----
FROM dependencies AS build
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
COPY service/ /app/service/
COPY main.py /app/main.py
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]
