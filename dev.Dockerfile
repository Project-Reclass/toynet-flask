FROM python:3.8-slim-buster

WORKDIR /app

copy requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 5000

ENTRYPOINT /app/test-entrypoint.sh
