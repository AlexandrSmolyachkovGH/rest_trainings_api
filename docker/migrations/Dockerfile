FROM python:3.10

WORKDIR /trainings_app

ENV PYTHONPATH="/trainings_app"
ENV YOYO_LOGLEVEL=DEBUG

RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client libpq-dev build-essential curl netcat-openbsd && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

RUN poetry config virtualenvs.create false
COPY ./pyproject.toml ./poetry.lock ./
RUN poetry install --no-root --no-interaction --no-ansi

COPY . .

RUN chmod +x /trainings_app/scripts/docker/migrate.sh
RUN chmod +x /trainings_app/scripts/docker/wait_for_postgres.sh

RUN echo MIGRATIONS BUILD SUCCESS
ENTRYPOINT ["sh", "/trainings_app/scripts/docker/migrate.sh"]