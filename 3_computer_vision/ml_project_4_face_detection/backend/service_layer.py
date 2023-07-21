from PIL import Image
from image_utils import (
    draw_boxes, 
    get_gcp_bounding_boxes,
    print_face_diagnostics
)
import io

async def detect_faces(contents: io.BytesIO, client) -> io.BytesIO:
    contents = Image.open(contents)
    if contents.mode != 'RGB':
        contents = contents.convert('RGB')

    byte_arr = io.BytesIO()
    contents.save(byte_arr, format='PNG')
    byte_data = byte_arr.getvalue()
    detected_faces = get_gcp_bounding_boxes(byte_data, client)

    print_face_diagnostics(detected_faces)

    output_image = draw_boxes(byte_arr, detected_faces)
    output_image_stream = io.BytesIO()
    output_image.save(output_image_stream, format="PNG")
    return output_image_stream.getvalue()