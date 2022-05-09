FROM debian:latest

WORKDIR /test/

ADD ../test_requirements.txt /test/requirements.txt

RUN apt-get update && apt-get install python3-pip -y && pip3 install -r requirements.txt

ADD classifier_bulk_test.py /test/classifier_bulk_test.py

EXPOSE 9003

CMD python3 -m pytest classifier_bulk_test.py