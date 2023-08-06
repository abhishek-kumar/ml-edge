# Python Standard Library Imports
import io
from base64 import b64encode

# Third Party Imports
from botocore.session import Session
from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from google.cloud import vision
from loguru import logger
from service_layer import detect_faces

app = FastAPI()
client = vision.ImageAnnotatorClient()
rekognition_session = Session(profile="rekognition")
rekognition_client = rekognition_session.create_client(
    service_name="rekognition", region_name="us-east-1"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.get("/")
async def hello_world():
    return {"message": "Hello World"}


@app.post("/detect_faces")
async def post_detect_faces(file: UploadFile):
    """
    An endpoint to send uploaded images to GCP to detect faces on an image
    """
    contents = io.BytesIO(await file.read())
    output_image_bytes = await detect_faces(contents, client, rekognition_client)
    return {"image": b64encode(output_image_bytes).decode()}
