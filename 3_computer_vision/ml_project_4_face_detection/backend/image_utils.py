from google.cloud import vision
from PIL import Image, ImageDraw
import io
from typing import List, Dict

def draw_boxes(content: io.BytesIO, detected_faces) -> io.BytesIO:
    """
    The `Image.open` function from the Pillow library expects a file path or a
    file-like object as the argument; not the content of the file itself.

    You can use `io.BytesIO` to create a binary stream from the image 
    content and open the image.
    
    Draw bounding boxes around the faces detected in the image,
    and return a version of the image with the bounding boxes
    """
    image = Image.open(content)
    draw = ImageDraw.Draw(image)

    for detected_face in detected_faces:
        vertices = [(vertex.x, vertex.y) for vertex in detected_face.bounding_poly.vertices]
        draw.line(vertices + [vertices[0]], width=5, fill='red')

    return image

def get_gcp_bounding_boxes(base64_image, gcp_vision_client):
    # Create an image object from the base64 string
    image = vision.Image(content=base64_image)
    
    # Perform face detection on the image
    response = gcp_vision_client.face_detection(image=image)
    face_annotations = response.face_annotations

    return face_annotations

def extract_vertices(detected_faces: List[Dict[str, Dict[str, List[Dict[str, int]]]]]):
    for detected_face in detected_faces:
        vertices  = [
            (vertex['x'], vertex['y']) for vertex in detected_face.get("bounding_poly").get("vertices")
        ]

    return vertices

def print_face_diagnostics(detected_faces):
    """
    This function prints out likelihoods of different faces, 
    and prints vertices for detected faces
    """
    likelihood_name = (
        "UNKNOWN",
        "VERY_UNLIKELY",
        "UNLIKELY",
        "POSSIBLE",
        "LIKELY",
        "VERY_LIKELY",
    )
    print("Faces:")

    for face in detected_faces:
        print(f"anger: {likelihood_name[face.anger_likelihood]}")
        print(f"joy: {likelihood_name[face.joy_likelihood]}")
        print(f"surprise: {likelihood_name[face.surprise_likelihood]}")

        vertices = [
            f"({vertex.x},{vertex.y})" for vertex in face.bounding_poly.vertices
        ]

        print(f"face bounds: {','.join(vertices)}")