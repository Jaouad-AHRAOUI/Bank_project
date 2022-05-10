FROM debian:latest

RUN apt-get update && apt-get install python3-pip -y

WORKDIR /app

COPY . /app

EXPOSE 5004

CMD ["python3","classifier_test.py"] 