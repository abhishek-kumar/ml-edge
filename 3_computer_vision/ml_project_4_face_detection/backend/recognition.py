import numpy as np
from typing import Optional, Tuple
from loguru import logger
from google.cloud import aiplatform
import tensorflow as tf
from tensorflow.keras.preprocessing.image import (
    load_img,
    DirectoryIterator,
    img_to_array,
)
from keras.applications.resnet50 import ResNet50, preprocess_input
import pathlib
import PIL
from typing import Dict
import json

DEFAULT_IMAGE_SIZE = (224, 224)

def detect_celebrity(image: bytes, rekognition_client) -> Optional[str]:
    response = rekognition_client.recognize_celebrities(
        Image={"Bytes": image}
    )
    logger.info(f"Response:\n{response}")

    celebrities = response.get("CelebrityFaces")

    return response["CelebrityFaces"][0]["Name"] if len(celebrities) > 0 else None


def vertex_ai_endpoint_predict_sample(
    project: str, location: str, instances: list, endpoint_url: str
):
    """
    Taken from https://cloud.google.com/vertex-ai/docs/predictions/get-online-predictions#predict-request
    """
    aiplatform.init(project=project, location=location)

    endpoint = aiplatform.Endpoint(endpoint_url)

    prediction = endpoint.predict(instances=instances)
    logger.info(f"Input instances: {instances}")
    logger.info(f"Prediction response: {prediction}")
    return prediction

def load_image_from_file(
        image_path: pathlib.Path, 
        target_image_size: Tuple[int, int]=DEFAULT_IMAGE_SIZE
) -> PIL.Image:
    return load_img(image_path, target_size=target_image_size)

def load_local_model(model_path: pathlib.Path) -> Tuple[tf.keras.Model, Dict[int, str]]:
    """
    Returns a model saved locally in the SavedModel format, with a label
    mapping dictionary that has been saved as an asset
    """
    saved_model = tf.keras.models.load_model(model_path)
    with open(saved_model.asset.asset_path.numpy(), 'r') as f:
        loaded_idx_to_celebrity_name= json.load(f)

    return saved_model, loaded_idx_to_celebrity_name

def get_predicted_celebrity_name_from_idx(data_streamer: DirectoryIterator, predicted_idx: int) -> str:
    """
    The mapping from celebrity name to index in the data streamer needs to be
    inverted so that we can get the name of the predicted celebrity, given the
    index
    """
    idx_to_celebrity_name = {v: k for k, v in data_streamer.class_indices.items()}
    return str(idx_to_celebrity_name.get(predicted_idx))

def make_prediction(image: PIL.Image, model: tf.keras.Model, idx_to_celebrity_name: Dict[int, str]) -> Optional[str]:
    example_image_array: np.ndarray  = img_to_array(image)
    example_image_array = np.expand_dims(example_image_array, axis=0)
    example_image_array = preprocess_input(example_image_array)

    prediction_probabilities = model.predict(example_image_array)

    predicted_celebrity_index: int = int(np.argmax(prediction_probabilities))
    logger.info(f"Predicted celebrity index: {predicted_celebrity_index}")

    return idx_to_celebrity_name.get(predicted_celebrity_index)




def detect_celebrity_from_fine_tuned_resnet50(image: bytes, vertexai_client) -> Optional[str]:

    pass