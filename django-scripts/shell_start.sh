#!/bin/bash
if grep -q microsoft /proc/version; 
then sudo service postgresql start;
else sudo systemctl start postgresql;
fi
source ./venv/bin/activate

export DJANGO_SECRET_KEY='test'
export DB_PASSWORD='test'
export AUTH_LDAP_BIND_PASSWORD='test'

pip install -r req.txt
python ./manage.py makemigrations
python ./manage.py migrate
python ./manage.py shell