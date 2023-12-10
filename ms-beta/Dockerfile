FROM python:3.10-buster

RUN useradd --create-home --home-dir /home/flaskapp flaskapp

# seleccionar la carpeta del usuario
WORKDIR /home/flaskapp

# instalar las dependencias del sitema
RUN apt-get update
RUN apt-get install -y curl gcc g++ libffi-dev libssl-dev build-essential default-mysql-client python3-mysqldb libmariadb-dev
RUN apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false
RUN rm -rf /var/lib/apt/lists/*

USER flaskapp
RUN mkdir app

COPY ./test ./test
COPY ./main ./main
COPY ./app.py .

ADD requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gevent gunicorn==20.1.0

EXPOSE 7000

CMD ["python", "./app.py"]