FROM python:3.8

RUN apt-get -y update
RUN apt-get -y install vim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /wanted_lab
ADD . /wanted_lab
WORKDIR /wanted_lab

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install gunicorn
RUN pip install psycopg2

RUN python3 manage.py migrate --settings=config.settings.deploy
RUN python3 manage.py collectstatic --settings=config.settings.deploy
RUN python3 companies/utils/db_uploader.py

EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi.deploy:application"]