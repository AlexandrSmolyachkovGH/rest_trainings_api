#!/bin/sh
sh scripts/docker/wait_for_postgres.sh;
cd /trainings_app;
python migrations/apply_migrations.py;
