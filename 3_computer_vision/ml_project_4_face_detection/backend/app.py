from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from base64 import b64encode, b64decode
from service_layer import detect_faces
from google.cloud import vision
from loguru import logger
import io

app = FastAPI()
client = vision.ImageAnnotatorClient()

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
    output_image_bytes = await detect_faces(contents, client)
    return { "image": b64encode(output_image_bytes).decode() }


