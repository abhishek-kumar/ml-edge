import numpy as np
from typing import Optional
from loguru import logger

def detect_celebrity(image: bytes, rekognition_client) -> Optional[str]:
    response = rekognition_client.recognize_celebrities(
        Image={"Bytes": image}
    )
    logger.info(f"Response:\n{response}")

    celebrities = response.get("CelebrityFaces")

    return response["CelebrityFaces"][0]["Name"] if len(celebrities) > 0 else None

def detect_celebrity_from_fine_tuned_resnet50(image: bytes, vertexai_client) -> Optional[str]:

    pass