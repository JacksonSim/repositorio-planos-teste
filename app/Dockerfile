FROM python:3.12

ENV DockerHOME=/home/app/webapp

RUN mkdir -p ${DockerHOME}

WORKDIR ${DockerHOME}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

# Collect static files
RUN python manage.py collectstatic --noinput
COPY . ${DockerHOME}

COPY init.sh /usr/src/app/init.sh
RUN chmod +x /usr/src/app/init.sh

# RUN pip install -r requeriments.txt

EXPOSE 8000

# Use volumes to map the local code to the container
# VOLUME ${DockerHOME}

# CMD ["/usr/src/app/init.sh"]
# CMD [ "gunicorn", "--bind", "0.0.0.0:8000", "projeto.wsgi:application"]