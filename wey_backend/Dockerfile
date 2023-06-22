FROM python:3.11
RUN mkdir /code
WORKDIR /code
COPY . /code

COPY pip.conf /root/.pip/pip.conf

# uwsgi setup
# RUN apk add python3-dev build-base linux-headers pcre-dev
RUN pip install uwsgi
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["uwsgi", "--ini", "uwsgi.ini"]