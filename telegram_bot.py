import os
from barcode import Code128
from barcode.writer import ImageWriter
from reportlab.pdfgen import canvas
import traceback

def generate_pdf(barcode_number, part_name, rack_number):
    try:
        # Generate barcode image
        barcode_path = os.path.join(os.getcwd(), f"{barcode_number}.png")
        try:
            barcode = Code128(barcode_number, writer=ImageWriter())
            barcode.save(barcode_path)
        except Exception as e:
            print(f"Error generating barcode: {e}")
            raise

        # Ensure barcode image file was created
        if not os.path.exists(barcode_path):
            raise FileNotFoundError(f"Barcode image could not be created at: {barcode_path}")

        # Set up PDF dimensions (10cm x 15cm converted to points)
        pdf_width, pdf_height = 283.5, 425.25
        pdf_path = os.path.join(os.getcwd(), f"{barcode_number}.pdf")
        c = canvas.Canvas(pdf_path, pagesize=(pdf_width, pdf_height))

        # Add barcode image to the PDF
        if not os.path.exists(barcode_path):
            print(f"Barcode image not found at: {barcode_path}")
            raise FileNotFoundError("Barcode image is missing.")
        c.drawImage(barcode_path, x=70.875, y=283.5, width=141.75, height=56.7)

        # Add barcode number text
        c.setFont("Helvetica", 10)
        c.drawCentredString(pdf_width / 2, 269.325, barcode_number)

        # Add part name
        c.setFont("Helvetica", 12)
        c.drawCentredString(pdf_width / 2, 198.45, f"Part Name: {part_name}")

        # Add rack number
        c.setFont("Helvetica", 12)
        c.drawCentredString(pdf_width / 2, 141.75, f"Rack Number: {rack_number}")

        # Finalize the PDF
        c.save()

        # Remove the temporary barcode image
        if os.path.exists(barcode_path):
            try:
                os.remove(barcode_path)
            except Exception as e:
                print(f"Error removing barcode image: {e}")

        print(f"Barcode Path: {barcode_path}")
        print(f"PDF Path: {pdf_path}")

        return pdf_path

    except Exception as e:
        print("Error during PDF generation:")
        traceback.print_exc()
        raise
