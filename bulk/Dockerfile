FROM debian:latest

RUN apt-get update && apt-get install python3-pip -y

WORKDIR /app

COPY . /app

EXPOSE 5003

CMD ["python3","bulk_classifier_test.py"] 