FROM debian:latest

RUN apt-get update && apt-get install python3-pip -y

WORKDIR /app

COPY . /app

EXPOSE 5002

CMD ["python3","authentification_test.py"] 