FROM tiangolo/uwsgi-nginx-flask:python3.8-alpine

RUN pip install requests

COPY telegramify/* /app/

EXPOSE 80:80