# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 20:40:21 2022

@author: Audrey & Jaouad
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from passlib.context import CryptContext
from pydantic import BaseModel
from typing import Optional, List
from fastapi.encoders import jsonable_encoder
import pandas as pd
import numpy as np
import json
import joblib



class profile(BaseModel):
    age: int
    job: Optional[str] = 'management'
    marital: str
    education: Optional[str] = 'secondary'
    default: str
    balance: int
    housing: str
    loan: str
    duration: int
    campaign: int
    pdays: int
    previous: int
    poutcome: Optional[str] = 'failure'
  

class ProbaClassification(BaseModel):
    non_adhesion_class_0 : float
    adhesion_class_1 : float

class Response(BaseModel):
    predicted_class: int
    proba : ProbaClassification
    


api = FastAPI(title = "Bank project",
    
    description = "Classification of the adhesion to a new bank product",          
    
    openapi_tags=[
    {
        'name': 'default',
        'description': 'default functions'
    },
    {
        'name': 'categorical variables',
        'description': 'description of categorical variables'
    },
    {
        'name': 'classification',
        'description': 'simple and bulk classification'
    }
    ]
)


security = HTTPBasic()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


users = {
    
    "admin":{
        "username": "admin",
        "hashed_password": pwd_context.hash("IamTheAdmin!")
        },
    "audrey":{
        "username": "audrey",
        "hashed_password": pwd_context.hash("SunShine123")
        },
    "jaouad":{
        "username": "jaouad",
        "hashed_password": pwd_context.hash("InFine987")
        }
    
    }


# initial features used for pre-processing
with open('initial_features.json','r') as f:
    features = json.load(f)
    

# scaling
rb_scaler = joblib.load("scaling.joblib")


# one hot encoding
encoder = joblib.load("ohe.joblib")


# binary encoding
binary_encoder = joblib.load("binary_encode.joblib")


# features for the classification model
with open('features_model.json','r') as f:
    features_model = json.load(f)
    

# model classifier
classifier = joblib.load("classifier.joblib")



def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    if not(users.get(username)) or not (pwd_context.verify(credentials.password, users[username]['hashed_password'])):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            header={"WWW-Authenticate": "Basic"}
            )
    return credentials.username



@api.get('/status', tags=['default'], name="api status")
def get_api():
    """
    Status of the api
    
    Returns
    -------
    int
        1 if the api is up.

    """
    return 1



@api.get('/user', tags=['default'])
def get_user(username: str = Depends(get_current_user)):
    return "Hello {}".format(username)



@api.get('/authorized_values', tags=['categorical variables'])
def get_values(username: str = Depends(get_current_user)):
    
    categorical_value = {
        "job": ['admin.', 'technician', 'services', 'management', 'retired',
                'blue-collar', 'unemployed', 'entrepreneur', 'housemaid',
                'unknown', 'self-employed', 'student'],
        "marital": ['married', 'single', 'divorced'],
        "education" : ['secondary', 'tertiary', 'primary', 'unknown'],
        "default": ['no', 'yes'],
        "housing": ['no', 'yes'],
        "loan": ['no', 'yes'],
        "poutcome": ['unknown', 'other', 'failure', 'success']
        }
    
    json_compatible_data = jsonable_encoder(categorical_value)
    
    #return categorical_value
    return JSONResponse(content = json_compatible_data)



@api.post('/classifier', response_model = Response, tags=['classification'])
def make_classification(newprofile:profile, username: str = Depends(get_current_user)):
    df = pd.DataFrame([newprofile.dict()])
    
    # na handling
    df.loc[(df['poutcome']=='unknown') & (df['pdays']>-1),'poutcome'] = 'other'
    df['poutcome'] = df['poutcome'].replace("unknown", "new")
    df['poutcome'] = df['poutcome'].replace("other", "failure")
    
    df['job'] = df['job'].replace("unknown", "management")
    df['education'] = df['education'].replace("unknown", "secondary")
    
    # scaling
    df['age'],df['balance'],df['duration'],df['campaign'],df['pdays'],df['previous'] = rb_scaler.transform(df[['age','balance','duration','campaign','pdays','previous']]).T
    
    try :
        # one hot encoding
        columnsToEncode = ['job', 'education', 'poutcome', 'marital']
        column_names = pd.Series(encoder.get_feature_names()).apply(lambda x: x[3:])
        X_ohe = pd.DataFrame(encoder.transform(df[columnsToEncode]).toarray(), columns= column_names)
    
        df.drop(columnsToEncode, axis=1, inplace=True)
        df = pd.concat([df, X_ohe], axis=1)
        
        # binary encoding
        df['default'], df['loan'], df['housing'] = binary_encoder.transform(df[['default', 'loan', 'housing']]).T
    
        # classification
        df = df[features_model]
        classification = classifier.predict(df)
        predicted_proba = classifier.predict_proba(df)[0]

        
        return_dict = {"predicted_class": int(classification[0]),
                       "proba": { "non_adhesion_class_0": np.round(predicted_proba[0],2),
                                 "adhesion_class_1": np.round(predicted_proba[1],2)
                                 }
                       }
    
        return return_dict
    
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Check the value of the categorical variables. Authorized values are listed at the endpoint 'authorized_values'."
            )



@api.post('/classifier/bulk', response_model = List[Response], tags=['classification'])
def make_bulk_classification(newprofile:List[profile], username: str = Depends(get_current_user)):
    
    if username == "admin":
        df = pd.DataFrame([element.dict() for element in newprofile])
        
        
        # na handling
        df.loc[(df['poutcome']=='unknown') & (df['pdays']>-1),'poutcome'] = 'other'
        df['poutcome'] = df['poutcome'].replace("unknown", "new")
        df['poutcome'] = df['poutcome'].replace("other", "failure")
        df['job'] = df['job'].replace("unknown", "management")
        df['education'] = df['education'].replace("unknown", "secondary")
        
        # scaling
        df['age'],df['balance'],df['duration'],df['campaign'],df['pdays'],df['previous'] = rb_scaler.transform(df[['age','balance','duration','campaign','pdays','previous']]).T
        
        try :
            # one hot encoding
            columnsToEncode = ['job', 'education', 'poutcome', 'marital']
            column_names = pd.Series(encoder.get_feature_names()).apply(lambda x: x[3:])
            X_ohe = pd.DataFrame(encoder.transform(df[columnsToEncode]).toarray(), columns= column_names)
        
            df.drop(columnsToEncode, axis=1, inplace=True)
            df = pd.concat([df, X_ohe], axis=1)
            
            # binary encoding
            df['default'], df['loan'], df['housing'] = binary_encoder.transform(df[['default', 'loan', 'housing']]).T
        
            # classification
            df = df[features_model]
            classification = classifier.predict(df)
            predicted_proba = classifier.predict_proba(df)
            
            classification = classification.tolist()
            predicted_proba = predicted_proba.tolist()
            
            return_response = []
            
            for i in range(len(df)):
                probas = predicted_proba[i]
                return_dict = {"predicted_class": classification[i],
                               "proba": { "non_adhesion_class_0": np.round(probas[0],2),
                                          "adhesion_class_1": np.round(probas[1],2)
                                   }
                               }
                return_response.append(return_dict)
            
            
            return return_response
        
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Check the value of the categorical variables. Authorized values are listed at the endpoint 'authorized_values'."
                )
    else:

        return JSONResponse(
            status_code = 403,
            content = {'message': '{}, only the admin user has the rigt to do bulk classification.'.format(username)}
            )


# if __name__ == '__main__':
#     uvicorn.run(api, port=8000, host='127.0.0.1')