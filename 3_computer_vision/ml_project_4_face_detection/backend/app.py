from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from google.cloud import vision
from base64 import b64encode
from typing import List
from loguru import logger

app = FastAPI()

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
async def detect_faces(file: UploadFile):
    """
    An endpoint to send uploaded images to GCP to detect faces on an image
    """
    # client = vision.ImageAnnotatorClient()

    # Read the image file
    contents = await file.read()
    
    # Encode the image file to base64
    img_base64 = b64encode(contents)

    decoded_image = img_base64.decode('utf-8')

    return {"image": decoded_image}
    
    # # Create an image object from the base64 string
    # image = vision.Image(content=img_base64)
    
    # # Perform face detection on the image
    # response = client.face_detection(image=image)
    # face_annotations = response.face_annotations

    # # Return the face annotations
    # return face_annotations
