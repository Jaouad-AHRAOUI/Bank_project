FROM debian:latest

WORKDIR /test/

ADD ./test_requirements.txt /test/requirements.txt

RUN apt-get update && apt-get install python3-pip -y && pip3 install -r requirements.txt

ADD standardisation_test.py /test/standardisation_test.py

EXPOSE 9001

CMD python3 -m pytest standardisation_test.py