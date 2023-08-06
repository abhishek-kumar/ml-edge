# Python Standard Library Imports
import os
import pathlib

# Third Party Imports
from google.cloud import vision
from loguru import logger
from PIL import Image, ImageDraw

PATH_TO_TEST_IMAGE = pathlib.Path(".test_assets/test_image.jpg")
assert PATH_TO_TEST_IMAGE.exists(), f"Could not find {PATH_TO_TEST_IMAGE}"
PATH_TO_OUTPUT_IMAGE = pathlib.Path(".test_assets/output_image.jpg")

PATH_TO_SERVICE_USER_CREDENTIALS = pathlib.Path("cloud-vision-credentials.json")
assert (
    PATH_TO_SERVICE_USER_CREDENTIALS.exists()
), f"Could not find {PATH_TO_SERVICE_USER_CREDENTIALS}"

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(PATH_TO_SERVICE_USER_CREDENTIALS)


def test_cloud_vision_works():
    client = vision.ImageAnnotatorClient()

    with open(PATH_TO_TEST_IMAGE, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.face_detection(image=image)
    faces = response.face_annotations
    logger.info(f"Face annotations:\n{faces}")

    pil_image = Image.open(PATH_TO_TEST_IMAGE)
    draw = ImageDraw.Draw(pil_image)

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = (
        "UNKNOWN",
        "VERY_UNLIKELY",
        "UNLIKELY",
        "POSSIBLE",
        "LIKELY",
        "VERY_LIKELY",
    )
    logger.info("Faces:")

    for face in faces:
        logger.info(f"anger: {likelihood_name[face.anger_likelihood]}")
        logger.info(f"joy: {likelihood_name[face.joy_likelihood]}")
        logger.info(f"surprise: {likelihood_name[face.surprise_likelihood]}")

        vertices_str = [
            f"({vertex.x},{vertex.y})" for vertex in face.bounding_poly.vertices
        ]
        vertices = [(vertex.x, vertex.y) for vertex in face.bounding_poly.vertices]
        draw.line(vertices + [vertices[0]], width=5, fill="red")

        logger.info(f"face bounds: {','.join(vertices_str)}")

    if response.error.message:
        raise Exception(
            f"{response.error.message}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors"
        )

    pil_image.save(PATH_TO_OUTPUT_IMAGE)
