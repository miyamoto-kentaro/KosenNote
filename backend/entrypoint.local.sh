#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

find . -name "000*.*" -exec rm {} \;
python manage.py flush --no-input
python manage.py makemigrations
python manage.py migrate users
python manage.py migrate
echo "from users.models import User; User.objects.create_superuser('admin', 'admin@gmail.com', 'admin')" | python manage.py shell
# echo "from blog.models import Article; User.objects.create_superuser('admin', 'admin@gmail.com', 'admin')" | python manage.py shell
exec "$@"