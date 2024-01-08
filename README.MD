
# Docker Compose para um projeto Django com MySQL e Nginx

## docker-compose.yaml

```yaml
version: '3.3'

services:
  # Serviço para o banco de dados MySQL
  db:
    build:
      context: ./db
    restart: always
    env_file:
      - ./app/.env
    ports:
      - "3306:3306"
    volumes:
      - ./mysql_data:/var/lib/mysql
    networks:
      - app_net

  # Serviço para o aplicativo Django
  web:
    build:
      context: ./app
    restart: always
    expose:
      - "8000"
    volumes:
      - "D:\\jackson\\dev\\django\\planos-sim_internet\\app:/home/app/webapp"
    networks:
      - app_net
    command: >
      bash -c "pip install -r requeriments.txt && 
      /usr/src/app/init.sh"
    depends_on:
      - db

  # Serviço para o servidor Nginx
  nginx:
    build:
      context: ./nginx
    restart: always
    ports:
      - "80:80"
    depends_on:
      - web
    networks:
      - app_net
    volumes:
      - ./app/staticfiles:/home/app/webapp/staticfiles

networks:
  app_net:
    driver: bridge
```

## Dockerfile para o aplicativo Django

```Dockerfile
FROM python:3.12

ENV DockerHOME=/home/app/webapp

RUN mkdir -p ${DockerHOME}

WORKDIR ${DockerHOME}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

# Coleta arquivos estáticos
RUN python manage.py collectstatic --noinput
COPY . ${DockerHOME}

COPY init.sh /usr/src/app/init.sh
RUN chmod +x /usr/src/app/init.sh

EXPOSE 8000
```

## Script de inicialização para o aplicativo Django

```bash
#!/bin/bash

# Executa migrações do Django
python manage.py makemigrations
python manage.py migrate

# Cria um superusuário
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'adminpass')" | python manage.py shell

# Inicia o servidor Gunicorn
gunicorn --preload --bind 0.0.0.0:8000 projeto.wsgi:application
```

## Dockerfile para o banco de dados MySQL

```Dockerfile
FROM mysql:8.0

ENV MYSQL_ROOT_PASSWORD=root
ENV MYSQL_DATABASE=planos
ENV MYSQL_USER=jackson
ENV MYSQL_PASSWORD=jackson

# COPY init.sql /docker-entrypoint-initdb.d/
```

## Dockerfile para o servidor Nginx

```Dockerfile
FROM nginx:latest
COPY ./default.conf /etc/nginx/conf.d/default.conf
```

## Configuração do Nginx (default.conf)

```conf
server {
    listen 80;
    server_name localhost;

    location / {
        proxy_pass http://web:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /home/app/webapp/staticfiles/;
    }

    location /media/ {
        alias /home/app/webapp/media/;
    }

    error_page 500 502 503 504 /500.html;
    location = /500.html {
        root /home/app/webapp/templates/;
    }
}
```