FROM debian:latest

WORKDIR /api/

ADD ./requirements.txt /api/requirements.txt

RUN apt-get update && apt-get install python3-pip -y && pip3 install -r requirements.txt

ADD binary_encode.joblib /api/binary_encode.joblib
ADD classifier.joblib /api/classifier.joblib
ADD ohe.joblib /api/ohe.joblib
ADD scaling.joblib /api/scaling.joblib
ADD features_model.json /api/features_model.json
ADD initial_features.json /api/initial_features.json

ADD api.py /api/api.py

EXPOSE 8000

CMD uvicorn api:api --reload