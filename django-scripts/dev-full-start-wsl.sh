#!/bin/bash
if grep -q microsoft /proc/version; 
then sudo service postgresql start;
else sudo systemctl start postgresql;
fi
source ./venv/bin/activate

export DJANGO_SECRET_KEY='django-insecure-a1@u+((7+uk%e9^p69061#5lykrsleazjfewd2sp#6lk03p&wh'
export DB_PASSWORD="wLFaEwHIRCfWBTY9rU9gNsEIZ"
export AUTH_LDAP_BIND_PASSWORD="!Wsparcie5005"

python ./manage.py makemigrations
python ./manage.py migrate
python ./manage.py runserver 0.0.0.0:8000