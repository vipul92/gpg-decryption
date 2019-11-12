FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.7
RUN apk --update add bash vim gnupg

RUN mkdir -p /var/www/gpghome
RUN ln -sfn ./* /var/www/test_task

WORKDIR /var/www/test_task

RUN pip install virtualenv
RUN virtualenv /var/www/test_task/venv
RUN source /var/www/test_task/venv/bin/activate

COPY requirements.txt /var/wwwtest_task/
COPY .  /var/www/test_task/
RUN pip install -r /var/www/test_task/requirements.txt

EXPOSE 80
RUN gunicorn --bind 0.0.0.0:80 flask_app:application
