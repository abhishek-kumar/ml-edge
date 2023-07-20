import io
from image_utils import draw_boxes, extract_vertices

def test_draw_boxes():

    # Arrange
    with open("test_image.jpg", "rb") as image_file:
        image_bytes = io.BytesIO(image_file.read())

    detected_faces = [
        {
            "bounding_poly": 
            {
                "vertices": [
                    {
                        "x": 10,
                        "y": 40
                    },
                    {
                        "x": 40,
                        "y": 10
                    }
                ]
            }
        },
    ]

    # Act
    output = draw_boxes(image_bytes, detected_faces)

    with open("output_image.jpg", "wb") as output_file:
        output_file.write(output.getvalue())


def test_extract_vertices():
    detected_faces = [
        {
            "bounding_poly": 
            {
                "vertices": [
                    {
                        "x": 10,
                        "y": 40
                    },
                    {
                        "x": 40,
                        "y": 10
                    }
                ]
            }
        },
    ]
    vertices = extract_vertices(detected_faces)

    assert vertices == [(10, 40), (40, 10)]


