#!/bin/bash

# Executa migrações do Django
python manage.py makemigrations
python manage.py migrate

# Cria um superusuário
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'adminpass')" | python manage.py shell

# Inicia o servidor Gunicorn
gunicorn --preload --bind 0.0.0.0:8000 projeto.wsgi:application