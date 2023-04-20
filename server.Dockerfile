FROM python:3.8

RUN apt-get update

RUN pip install --upgrade pip

RUN mkdir /server

WORKDIR /server

COPY . /server

RUN pip install -r requirements.txt

RUN chmod +x entrypoint.sh

ENTRYPOINT ["bash", "/server/entrypoint.sh"]