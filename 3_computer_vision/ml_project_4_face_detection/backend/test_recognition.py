# from recognition import zero_shot, generate_image_to_id_mapping
from recognition import detect_celebrity
import pathlib
from botocore.session import Session
from loguru import logger
import pytest

# @pytest.fixture
# def test_image():
#     # PATH_TO_TEST_IMAGE = pathlib.Path("Celebrity Faces Dataset/Brad Pitt/001_c04300ef.jpg")
#     PATH_TO_TEST_IMAGE = pathlib.Path(".test_assets/test_image.jpg")
#     assert PATH_TO_TEST_IMAGE.exists(), f"Could not find {PATH_TO_TEST_IMAGE}"
    
#     with open(PATH_TO_TEST_IMAGE, "rb") as image_file:
#         content = image_file.read()

#     return content


@pytest.mark.parametrize(
        "test_image_path,expected_output", 
        [
            (pathlib.Path("Celebrity Faces Dataset/Brad Pitt/001_c04300ef.jpg"), "Brad Pitt"), 
            (pathlib.Path(".test_assets/test_image.jpg"), None)
        ]
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
        service_name="rekognition",
        region_name="us-east-1"
    )
    response = detect_celebrity(content, rekognition_client)
    logger.info(f"Detected celebrities:\n{response}")

    assert response == expected_output

def test_vertexai_fine_tuned_resnet_can_detect_brad_pitt():
    pass
