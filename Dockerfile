FROM python:2.7.17-slim-stretch

RUN pip install -r requirements.txt

RUN python manage.py migrate && python manage.py runserver
