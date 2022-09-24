# syntax=docker/dockerfile:1
FROM python:alpine AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ARG SECRET_KEY

WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt

FROM builder AS runner

COPY . /code/
EXPOSE 8000
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]