# Third Party Imports
import joblib
import numpy as np
import pydantic
from fastapi import FastAPI
from sklearn.datasets import load_iris

app = FastAPI()

iris_class_names = load_iris().target_names
model = joblib.load("model.joblib")


class IrisSample(pydantic.BaseModel):
    sepal_length: float = pydantic.Field(default=5.1, title="Sepal Length")
    sepal_width: float = pydantic.Field(default=3.5, title="Sepal Width")
    petal_length: float = pydantic.Field(default=1.4, title="Petal Length")
    petal_width: float = pydantic.Field(default=0.2, title="Petal Width")


@app.get("/")
def hello_world():
    return {"message": "Hello World!"}


@app.post("/predict")
async def predict(sample: IrisSample):
    prediction = model.predict(
        np.asarray(
            [
                [
                    sample.sepal_length,
                    sample.sepal_width,
                    sample.petal_length,
                    sample.petal_width,
                ]
            ]
        )
    )
    return {"prediction": iris_class_names[prediction[0]]}
