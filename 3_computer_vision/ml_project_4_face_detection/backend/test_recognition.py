# from recognition import zero_shot, generate_image_to_id_mapping
from recognition import detect_celebrity
import pathlib
from botocore.session import Session
from loguru import logger

# def test_local_recognition_works():
#     assert len(zero_shot(id_to_images[0][5])) > 0

# def test_id_to_images():
#     id_to_images = generate_image_to_id_mapping("Celebrity Faces Dataset")
#     print(id_to_images)

def test_detect_celebrity():
    PATH_TO_TEST_IMAGE = pathlib.Path("Celebrity Faces Dataset/Brad Pitt/001_c04300ef.jpg")
    # PATH_TO_TEST_IMAGE = pathlib.Path(".test_assets/test_image.jpg")
    assert PATH_TO_TEST_IMAGE.exists(), f"Could not find {PATH_TO_TEST_IMAGE}"

    rekognition_session = Session(profile="rekognition")
    rekognition_client = rekognition_session.create_client(
        service_name="rekognition",
        region_name="us-east-1"
    )

    with open(PATH_TO_TEST_IMAGE, "rb") as image_file:
        content = image_file.read()
    
    response = detect_celebrity(content, rekognition_client)

    logger.info(f"Detected celebrities:\n{response}")