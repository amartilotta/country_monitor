FROM python:3.11-alpine3.16 as backend

ARG ENVIRONMENT

ENV TZ=America/Argentina/Buenos_Aires \
    PIP_DEFAULT_TIMEOUT=100 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYDEVD_DISABLE_FILE_VALIDATION=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

ADD poetry.lock poetry.lock
ADD pyproject.toml pyproject.toml
ADD deployment/docker/Aptfile Aptfile

RUN apk add --no-cache $(cat Aptfile)

RUN pip install poetry
RUN poetry config virtualenvs.create false

RUN echo PROJECT_NAME=$(sed -n 's/^ *name.*=.*"\([^"]*\)".*/\1/p' pyproject.toml) >> /etc/metadata && \
    echo PROJECT_VERSION=$(sed -n 's/^ *version.*=.*"\([^"]*\)".*/\1/p' pyproject.toml) >> /etc/metadata

RUN if [ "$ENVIRONMENT" == "prod" ]; then poetry install --only main; else poetry install; fi

COPY src ./
