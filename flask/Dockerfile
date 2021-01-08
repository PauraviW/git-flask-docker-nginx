FROM python:3.8-buster

WORKDIR /

ADD . /

RUN pip3 install uwsgi
RUN pip3 install -r requirements.txt

EXPOSE 5000

CMD ["uwsgi", "app.ini"]