import io
from image_utils import (
    draw_boxes, 
    extract_vertices,
    get_gcp_bounding_boxes
)
import pathlib
import os
from google.cloud import vision
from loguru import logger
from base64 import b64encode, b64decode
import pytest

@pytest.fixture
def example_face_annotations():
    PATH_TO_TEST_IMAGE = pathlib.Path(".test_assets/test_image.jpg")
    assert PATH_TO_TEST_IMAGE.exists(), f"Could not find {PATH_TO_TEST_IMAGE}"

    PATH_TO_SERVICE_USER_CREDENTIALS = pathlib.Path("cloud-vision-credentials.json")
    assert PATH_TO_SERVICE_USER_CREDENTIALS.exists(), f"Could not find {PATH_TO_SERVICE_USER_CREDENTIALS}"

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(PATH_TO_SERVICE_USER_CREDENTIALS)
    client = vision.ImageAnnotatorClient()

    with open(PATH_TO_TEST_IMAGE, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.face_detection(image=image)
    return response.face_annotations

def test_draw_boxes(example_face_annotations):
    # Arrange
    PATH_TO_TEST_IMAGE = pathlib.Path(".test_assets/test_image.jpg")
    with open(PATH_TO_TEST_IMAGE, "rb") as image_file:
        content = image_file.read()

    # Act
    image_with_boxes = draw_boxes(io.BytesIO(content), example_face_annotations)

    image_with_boxes.save(".test_assets/output_image.jpg")


def test_extract_vertices():
    detected_faces = [
        {
            "bounding_poly": 
            {
                "vertices": [
                    {
                        "x": 10,
                        "y": 40
                    },
                    {
                        "x": 40,
                        "y": 10
                    }
                ]
            }
        },
    ]
    vertices = extract_vertices(detected_faces)

    assert vertices == [(10, 40), (40, 10)]


def test_get_gcp_bounding_boxes():
    PATH_TO_TEST_IMAGE = pathlib.Path(".test_assets/test_image.jpg")
    assert PATH_TO_TEST_IMAGE.exists(), f"Could not find {PATH_TO_TEST_IMAGE}"

    PATH_TO_SERVICE_USER_CREDENTIALS = pathlib.Path("cloud-vision-credentials.json")
    assert PATH_TO_SERVICE_USER_CREDENTIALS.exists(), f"Could not find {PATH_TO_SERVICE_USER_CREDENTIALS}"

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(PATH_TO_SERVICE_USER_CREDENTIALS)
    client = vision.ImageAnnotatorClient()

    with open(PATH_TO_TEST_IMAGE, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.face_detection(image=image)
    faces = response.face_annotations
    logger.info(f"Face annotations:\n{faces}")


