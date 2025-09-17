import os
import uuid
import datetime
from dotenv import load_dotenv
import json

import io
from google.cloud import vision

def detect_text_from_local_file(file_path: str) -> str:
    """Detects text from a local image file.
    Args: file_path: The path to the local image file.
    Returns: The extracted text as a single string.
    """
    client = vision.ImageAnnotatorClient()
    with io.open(file_path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    if texts:
        full_text = texts[0].description
        return full_text
    else:
        return "No text detected."
    
# Test with this code
# text_over_image = detect_text_from_local_file('input/quote-image.jpg')
# print(text_over_image)
