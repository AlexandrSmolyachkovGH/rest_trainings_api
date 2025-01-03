FROM python:3.10

WORKDIR /trainings_app

ENV PYTHONPATH="/trainings_app"

RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client libpq-dev build-essential curl netcat-openbsd && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

COPY ./pyproject.toml ./poetry.lock ./

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --only main

COPY . .

RUN chmod +x /trainings_app/scripts/docker/migrate.sh
RUN chmod +x /trainings_app/scripts/docker/wait_for_postgres.sh

RUN echo MIGRATIONS BUILD SUCCESS