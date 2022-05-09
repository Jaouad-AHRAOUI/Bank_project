FROM debian:latest

WORKDIR /test/

ADD ../test_requirements.txt /test/requirements.txt

RUN apt-get update && apt-get install python3-pip -y && pip3 install -r requirements.txt

ADD authentification_test.py /test/authentification_test.py

EXPOSE 9000

CMD python3 -m pytest authentification_test.py