#!/bin/bash
if grep -q microsoft /proc/version; 
then sudo service postgresql start;
else sudo systemctl start postgresql;
fi
source ./venv/bin/activate

#change values on production environment
export DJANGO_SECRET_KEY='placeholder'
export DB_PASSWORD="placeholder"
export AUTH_LDAP_BIND_PASSWORD="placeholder"

pip install -r req.txt
python ./manage.py makemigrations --settings=vigo_guests.settings.production
python ./manage.py migrate --settings=vigo_guests.settings.production
echo "yes" | python ./manage.py collectstatic --settings=vigo_guests.settings.production

daphne -b 0.0.0.0 -p 8000 --access-log daphne.log vigo_guests.asgi:application 