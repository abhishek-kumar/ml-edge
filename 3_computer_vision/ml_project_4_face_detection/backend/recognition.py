import base64
import io
import json
import pathlib
from typing import Dict, List, Optional, Tuple

import cv2
import numpy as np
import PIL
import tensorflow as tf
from google.cloud import aiplatform
from keras.applications.resnet50 import ResNet50, preprocess_input
from loguru import logger
from pydantic import BaseModel, validator
from tensorflow.keras.preprocessing.image import (
    DirectoryIterator,
    img_to_array,
    load_img,
)

DEFAULT_IMAGE_LEN = 112

DEFAULT_IMAGE_SIZE = (DEFAULT_IMAGE_LEN, DEFAULT_IMAGE_LEN)
PATH_TO_CELEBRITY_MAPPING = (
    pathlib.Path(__file__).resolve().parent / "idx_to_celebrity_name.json"
)
assert PATH_TO_CELEBRITY_MAPPING.exists(), f"Could not find {PATH_TO_CELEBRITY_MAPPING}"

with open(PATH_TO_CELEBRITY_MAPPING, "r") as f:
    loaded_idx_to_celebrity_name = json.load(f)


def detect_celebrity(image: bytes, rekognition_client) -> Optional[str]:
    response = rekognition_client.recognize_celebrities(Image={"Bytes": image})
    logger.info(f"Response:\n{response}")

    celebrities = response.get("CelebrityFaces")

    return response["CelebrityFaces"][0]["Name"] if len(celebrities) > 0 else None


def load_image_from_file(
    image_path: pathlib.Path, target_image_size: Tuple[int, int] = DEFAULT_IMAGE_SIZE
) -> PIL.Image:
    return load_img(image_path, target_size=target_image_size)


def load_local_model(model_path: pathlib.Path) -> Tuple[tf.keras.Model, Dict[int, str]]:
    """
    Returns a model saved locally in the SavedModel format, with a label
    mapping dictionary that has been saved as an asset
    """
    saved_model = tf.keras.models.load_model(model_path)
    with open(saved_model.asset.asset_path.numpy(), "r") as f:
        loaded_idx_to_celebrity_name = json.load(f)

    return saved_model, loaded_idx_to_celebrity_name


def get_predicted_celebrity_name_from_idx(
    data_streamer: DirectoryIterator, predicted_idx: int
) -> str:
    """
    The mapping from celebrity name to index in the data streamer needs to be
    inverted so that we can get the name of the predicted celebrity, given the
    index
    """
    idx_to_celebrity_name = {v: k for k, v in data_streamer.class_indices.items()}
    return str(idx_to_celebrity_name.get(predicted_idx))


def make_prediction(
    image: PIL.Image, model: tf.keras.Model, idx_to_celebrity_name: Dict[int, str]
) -> Optional[str]:
    logger.info(f"Input image: {image}")
    example_image_array: np.ndarray = img_to_array(image)
    logger.info(f"Image array shape: {example_image_array.shape}")
    example_image_array = np.expand_dims(example_image_array, axis=0)
    logger.info(f"After expanding dimensions: {example_image_array.shape}")
    example_image_array = preprocess_input(example_image_array)
    logger.info(f"After preprocessing: {example_image_array.shape}")

    prediction_probabilities = model.predict(example_image_array)

    predicted_celebrity_index: int = int(np.argmax(prediction_probabilities))
    logger.info(f"Predicted celebrity index: {predicted_celebrity_index}")

    logger.info(f"Using idx_to_celebrity_name mapping: {idx_to_celebrity_name}")

    celebrity_name_prediction: Optional[str] = idx_to_celebrity_name.get(
        str(predicted_celebrity_index)
    )

    logger.info(f"Predicted celebrity name: {celebrity_name_prediction}")

    return celebrity_name_prediction


class Instance(BaseModel):
    values: np.ndarray

    @validator("values")
    def check_shape(cls, values):
        if values.shape != (*DEFAULT_IMAGE_SIZE, 3):
            raise ValueError(f"Expected shape (224, 224, 3), got {values.shape}")
        return values

    class Config:
        arbitrary_types_allowed = True


class RequestModel(BaseModel):
    instances: List[Instance]


def vertex_ai_endpoint_predict_sample(
    project: str, location: str, instances, endpoint_id: str = "2627296228710285312"
) -> int:
    """
    Taken from https://cloud.google.com/vertex-ai/docs/predictions/get-online-predictions#predict-request

    Live endpoints are used like this:
    endpoint.predict(instances=[[6.7, 3.1, 4.7, 1.5], [4.6, 3.1, 1.5, 0.2]])
    """
    aiplatform.init(project=project, location=location)

    # endpoint = aiplatform.Endpoint(endpoint_name=endpoint_id)
    endpoint = aiplatform.Endpoint(
        endpoint_name="projects/820240006900/locations/us-east4/endpoints/5089357849998393344"
    )

    logger.info(f"Input instances: {instances}")
    prediction_probabilities = endpoint.predict(instances=instances).predictions
    logger.info(f"Prediction response: {prediction_probabilities}")
    predicted_celebrity_index: int = int(np.argmax(prediction_probabilities))
    logger.info(f"Predicted celebrity index: {predicted_celebrity_index}")
    return predicted_celebrity_index


def detect_celebrity_from_fine_tuned_resnet50(image: bytes) -> Optional[str]:
    # Convert bytes to image
    image = PIL.Image.open(io.BytesIO(image))

    # Preprocess the image
    image = image.resize(
        DEFAULT_IMAGE_SIZE
    )  # replace with your model's expected dimensions
    np_image = np.array(image)
    np_image = np.expand_dims(np_image, axis=0)  # add a batch dimension

    np_image = preprocess_input(np_image)

    # Send it to the model
    instances = np_image.tolist()  # convert the array to a list before sending

    prediction = vertex_ai_endpoint_predict_sample(
        project="aiedge-masterclass", location="us-east4", instances=instances
    )

    logger.info(f"Prediction response: {prediction}")

    predicted_celebrity: Optional[str] = loaded_idx_to_celebrity_name.get(
        str(prediction)
    )
    return predicted_celebrity
