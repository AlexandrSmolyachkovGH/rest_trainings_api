#!/bin/sh
echo "[ wait_for_rabbitmq.sh ] - HOST=${RABBITMQ_HOST} PORT=${RABBITMQ_PORT}"
while ! nc -z ${RABBITMQ_HOST} ${RABBITMQ_PORT}; do
  echo "[ wait_for_rabbitmq.sh ] - wait for rabbitmq...";
  sleep 1;
done
echo "[ wait_for_rabbitmq.sh ] - CONNECTED"