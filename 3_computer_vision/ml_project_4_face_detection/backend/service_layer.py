from image_utils import (
    draw_boxes, 
    get_gcp_bounding_boxes,
    print_face_diagnostics
)
import io

async def detect_faces(img_base64, client) -> io.BytesIO:
    detected_faces = get_gcp_bounding_boxes(img_base64, client)

    print_face_diagnostics(detected_faces)

    image_bytes = draw_boxes(uri, face_annotations)

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )

    return image_bytes