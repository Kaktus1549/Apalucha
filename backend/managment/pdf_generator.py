from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
import io
from PyPDF2 import PdfReader, PdfWriter
from sys import path
from os import getenv
apalucha = getenv("apalucha")
if apalucha is None:
    apalucha = "."
path.append(apalucha)
from managment.qr_codes import generate_qr_code
import hashlib

def generate_pdf(url, template_filename, new_filename):
    # Generate the QR code
    qr_code = generate_qr_code(url)
    url_hash = hashlib.sha256(url.encode('utf-8')).hexdigest()

    try:
        # Save the QR code to a bytes buffer
        qr_buffer = io.BytesIO()
        qr_code.save(qr_buffer, format='PNG')
        qr_buffer.seek(0)

        # Load the template PDF
        template_reader = PdfReader(template_filename)
        writer = PdfWriter()

        # Process the first page to add QR code
        if len(template_reader.pages) > 0:
            # Create a canvas for QR code
            qr_packet = io.BytesIO()
            qr_canvas = canvas.Canvas(qr_packet, pagesize=letter)
            qr_x = letter[0] - 100 - 80  # Right bottom corner
            qr_y = 20
            qr_canvas.drawImage(ImageReader(qr_buffer), qr_x, qr_y, width=80, height=80)
            qr_canvas.save()

            # Merge QR code with the first page of the template
            qr_packet.seek(0)
            qr_pdf = PdfReader(qr_packet)
            first_page = template_reader.pages[0]
            first_page.merge_page(qr_pdf.pages[0])
            writer.add_page(first_page)

        # Process the second page to add URL hash
        if len(template_reader.pages) > 1:
            hash_packet = io.BytesIO()
            hash_canvas = canvas.Canvas(hash_packet, pagesize=letter)
            hash_x = 20  # Left bottom corner
            hash_y = 20
            font_size = 8
            hash_canvas.setFont("Helvetica", font_size)
            hash_canvas.drawString(hash_x, hash_y, f"URL hash: {url_hash}")
            hash_canvas.save()

            # Merge hash page
            hash_packet.seek(0)
            hash_pdf = PdfReader(hash_packet)
            second_page = template_reader.pages[1]
            second_page.merge_page(hash_pdf.pages[0])
            writer.add_page(second_page)

        # Add any remaining pages (if any)
        for i in range(2, len(template_reader.pages)):
            writer.add_page(template_reader.pages[i])

        # Save the updated PDF as a new file
        with open(new_filename, "wb") as output_pdf_file:
            writer.write(output_pdf_file)
        
        return True
    except Exception as e:
        print(f"Got exception while generating PDF: {e}")
        return False