import io
from pdf2image import convert_from_bytes
import pyzbar.pyzbar as pyzbar
from PIL import Image

def extract_qr_code(pdf_data):
    # Convert PDF to image
    images = convert_from_bytes(pdf_data)
    for image in images:
        # Read QR code from image
        image_stream = io.BytesIO()
        image.save(image_stream, format="PNG")
        image_stream.seek(0)
        image = Image.open(image_stream)
        decoded_objects = pyzbar.decode(image)
        for obj in decoded_objects:
            return obj.data.decode("utf-8")
    return None