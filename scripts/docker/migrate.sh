#!/bin/sh
echo 1111;
sh scripts/docker/wait_for_postgres.sh;
echo 2222;
cd /trainings_app;
echo 3333;
python migrations/apply_migrations.py;
echo 4444;
