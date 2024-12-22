FROM python:3.10

WORKDIR /trainings_app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./pyproject.toml ./poetry.lock ./

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev build-essential curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-dev

COPY . .

