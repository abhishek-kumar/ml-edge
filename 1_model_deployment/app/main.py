from fastapi import FastAPI, Request

import joblib
import json
import numpy as np
import pickle
import os

from google.cloud import storage
from sklearn.datasets import load_iris

from pydantic import BaseModel

app = FastAPI()
gcs_client = storage.Client()

with open("model.joblib", 'wb') as model_f:
    gcs_client.download_blob_to_file(
        f"{os.environ['AIP_STORAGE_URI']}/model.joblib", model_f
    )

_class_names = load_iris().target_names
_model = joblib.load("model.joblib")

@app.get("/")
def greet_user():
    return {"message": "Hello! Welcome to MLE MasterClass!"}

@app.get(os.environ["AIP_HEALTH_ROUTE"], status_code=200)
def health():
    return {"message": "Model API is healthy!"}

@app.post(os.environ["AIP_PREDICT_ROUTE"])
async def predict(request: Request):
    body = await request.json() 
    instances = body["instances"]
    inputs = np.asarray(instances)
    outputs = _model.predict(inputs)
    return {"predictions": [_class_names[class_num] for class_num in outputs]}