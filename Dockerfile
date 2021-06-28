FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

ENV FLASK_ENV=production
ENV FLASK_APP=flasksrc

EXPOSE 5000

RUN flask init-db

CMD [ "flask", "run", "--host", "0.0.0.0"]