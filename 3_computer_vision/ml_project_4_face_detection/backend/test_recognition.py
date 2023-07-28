# from recognition import zero_shot, generate_image_to_id_mapping
import json
import pathlib
from typing import Optional

import numpy as np
import PIL
import pytest
from botocore.session import Session
from google.cloud import aiplatform
from keras.applications.resnet50 import preprocess_input
from loguru import logger
from tensorflow.keras.preprocessing.image import img_to_array

from recognition import (
    DEFAULT_IMAGE_SIZE,
    detect_celebrity,
    detect_celebrity_from_fine_tuned_resnet50,
    load_image_from_file,
    load_local_model,
    make_prediction,
)

PATH_TO_CELEBRITY_MAPPING = pathlib.Path("idx_to_celebrity_name.json")
assert PATH_TO_CELEBRITY_MAPPING.exists(), f"Could not find {PATH_TO_CELEBRITY_MAPPING}"

with open(PATH_TO_CELEBRITY_MAPPING, "r") as f:
    idx_to_celebrity_name = json.load(f)


@pytest.fixture
def test_pil_image() -> PIL.Image:
    example_file_path = pathlib.Path(".test_assets/test_image.jpg")
    loaded_img_from_file: PIL.Image = load_image_from_file(
        image_path=example_file_path,
    )
    return loaded_img_from_file


@pytest.fixture
def brad_pitt_image() -> PIL.Image:
    brad_pitt_image_path = pathlib.Path(
        "Celebrity Faces Dataset/Brad Pitt/001_c04300ef.jpg"
    )
    return load_image_from_file(brad_pitt_image_path)


@pytest.mark.parametrize(
    "test_image_path,expected_output",
    [
        (
            pathlib.Path("Celebrity Faces Dataset/Brad Pitt/001_c04300ef.jpg"),
            "Brad Pitt",
        ),
        (pathlib.Path(".test_assets/test_image.jpg"), None),
    ],
)
def test_rekognition_can_detect_brad_pitt(test_image_path, expected_output):
    """
    Test that AWS Rekognition can detect Brad Pitt, but not the example image.
    """
    assert test_image_path.exists(), f"Could not find {test_image_path}"

    with open(test_image_path, "rb") as image_file:
        content = image_file.read()

    rekognition_session = Session(profile="rekognition")
    rekognition_client = rekognition_session.create_client(
        service_name="rekognition", region_name="us-east-1"
    )
    response = detect_celebrity(content, rekognition_client)
    logger.info(f"Detected celebrities:\n{response}")

    assert response == expected_output


def test_vertexai_fine_tuned_resnet_can_detect_brad_pitt():
    pass


def test_load_img_from_file(test_pil_image: PIL.Image):
    assert isinstance(test_pil_image, PIL.Image)


def test_can_convert_pil_image_to_np_array(test_pil_image: PIL.Image):
    test_image_np_array: np.ndarray = img_to_array(test_pil_image)
    assert isinstance(test_image_np_array, np.ndarray)
    assert test_image_np_array.shape == (*DEFAULT_IMAGE_SIZE, 3)


def test_can_make_local_prediction_on_fine_tuned_resnet(brad_pitt_image):
    # arrange
    path_to_model = pathlib.Path("../backend/model")
    model, idx_to_celebrity_name = load_local_model(path_to_model)

    # act
    prediction = make_prediction(brad_pitt_image, model, idx_to_celebrity_name)

    # assert
    assert prediction == "Brad Pitt"


def test_vertex_ai_request(brad_pitt_image):
    example_image_array: np.ndarray = img_to_array(brad_pitt_image)
    example_image_array = np.expand_dims(example_image_array, axis=0)
    example_image_array = preprocess_input(example_image_array)

    aiplatform.init(
        project="aiedge-masterclass",
        location="us-east4",
    )

    endpoint = aiplatform.Endpoint("2627296228710285312")

    logger.info(f"Example image array shape: {example_image_array.shape}")

    prediction_probabilities = endpoint.predict([{"values": example_image_array}])

    predicted_celebrity_index: int = int(np.argmax(prediction_probabilities))
    logger.info(f"Predicted celebrity index: {predicted_celebrity_index}")

    logger.info(f"Using idx_to_celebrity_name mapping: {idx_to_celebrity_name}")

    celebrity_name_prediction: Optional[str] = idx_to_celebrity_name.get(
        str(predicted_celebrity_index)
    )

    # act
    prediction = detect_celebrity_from_fine_tuned_resnet50(brad_pitt_image)

    # assert
    assert prediction == "Brad Pitt"
