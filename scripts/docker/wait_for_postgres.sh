#!/bin/sh
echo "[ wait_for_postgres.sh ] - HOST=${POSTGRES_HOST} PORT=${POSTGRES_PORT}"
while ! nc -z ${POSTGRES_HOST} ${POSTGRES_PORT};
do
  echo "[ wait_for_postgres.sh ] - wait for postgres...";
  sleep 1;
done;
echo "[ wait_for_postgres.sh ] - CONNECTED";