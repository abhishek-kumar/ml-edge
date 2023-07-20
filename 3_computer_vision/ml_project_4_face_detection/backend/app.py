from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from base64 import b64encode, b64decode
from service_layer import detect_faces
from google.cloud import vision

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
    contents = await file.read()
    img_base64 = b64encode(contents)
    output_image_bytes = await detect_faces(img_base64, client)
    return b64decode(output_image_bytes.getvalue()).decode("utf-8")


