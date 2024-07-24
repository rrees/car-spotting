ARG PYTHON_VERSION=3.12.2

FROM python:${PYTHON_VERSION}-alpine AS builder

ENV PYTHONUNBUFFERED=1 \
    PIPENV_VENV_IN_PROJECT=1 \
    PIPENV_CUSTOM_VENV_NAME=.venv

RUN \
 apk update && \
 apk upgrade && \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev

WORKDIR /app
COPY . /app


RUN pip install pipenv
RUN pipenv install

RUN apk --purge del .build-deps


FROM python:${PYTHON_VERSION}-alpine

ENV PYTHONUNBUFFERED=1

RUN apk update && apk upgrade

WORKDIR /app
COPY --from=builder /app .

EXPOSE 8080

CMD [ "/app/.venv/bin/gunicorn", "--bind=0.0.0.0:8080", "--worker-tmp-dir", "/dev/shm", "spotting.app:app"]
