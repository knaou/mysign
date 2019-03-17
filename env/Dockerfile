FROM python:3.7

RUN apt update
RUN apt install openssl make gcc

#RUN pip3 install --upgrade pip
#RUN pip3 install pyopenssl django djangorestframework django-filter uwsgi
COPY env/requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

