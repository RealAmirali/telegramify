FROM tiangolo/uwsgi-nginx-flask

RUN pip install requests

COPY telegramify/* /app/

EXPOSE 80:80