FROM python:3.9-alpine

COPY . /app
WORKDIR app

RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev

RUN pip install pipenv
RUN pipenv install

RUN apk --purge del .build-deps

ENV PYTHONUNBUFFERED=1

EXPOSE 8080

ENTRYPOINT [ "pipenv", "run", "gunicorn", "--bind=0.0.0.0:8080", "--worker-tmp-dir", "/dev/shm", "spotting.app:app"]
