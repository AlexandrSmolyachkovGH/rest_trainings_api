#!/bin/sh
echo "Starting Report Worker"
python /trainings_app/trainings_app/reports/run_worker.py &
echo "Starting Membership_Checker Worker"
python /trainings_app/trainings_app/check_membership/run_worker.py &
echo "Workers are launched"