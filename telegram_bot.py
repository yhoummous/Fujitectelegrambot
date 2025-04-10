import telebot
import os  # For file and directory handling
from reportlab.pdfgen import canvas  # For PDF creation
from barcode import Code128
from barcode.writer import ImageWriter

# Initialize Telegram Bot with your API token
API_TOKEN = '7639520248:AAGNp_iMnfXu957g6f56z8VbJM39bcdzjMQ'
bot = telebot.TeleBot(API_TOKEN)

# Command to start the bot
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to Fujitec Barcode Bot! Send me the data in the format:\n\n"
                          "Barcode Number, Part Name, Rack Number")

# Handle user input
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # Parse user input
        data = message.text.split(',')
        if len(data) != 3:
            bot.reply_to(message, "Please provide data in the format: Barcode Number, Part Name, Rack Number")
            return

        barcode_number, part_name, rack_number = data[0].strip(), data[1].strip(), data[2].strip()

        # Generate the PDF
        pdf_path = generate_pdf(barcode_number, part_name, rack_number)

        # Send the PDF back to the user
        with open(pdf_path, 'rb') as pdf_file:
            bot.send_document(message.chat.id, pdf_file)

        # Clean up the generated files
        if os.path.exists(pdf_path):
            os.remove(pdf_path)

    except Exception as e:
        bot.reply_to(message, f"An error occurred: {e}")

# Function to generate the PDF
def generate_pdf(barcode_number, part_name, rack_number):
    try:
        # Generate barcode image
        barcode_path = os.path.join(os.getcwd(), f"{barcode_number}.png")
        barcode = Code128(barcode_number, writer=ImageWriter())
        barcode.save(barcode_path)

        # Set up PDF size and layout
        pdf_path = os.path.join(os.getcwd(), f"{barcode_number}.pdf")
        pdf_width, pdf_height = 283.5, 425.25  # Dimensions in points (10cm x 15cm)
        c = canvas.Canvas(pdf_path, pagesize=(pdf_width, pdf_height))

        # Add barcode to PDF
        c.drawImage(barcode_path, x=70.875, y=283.5, width=141.75, height=56.7)

        # Add barcode number
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

        # Remove temporary barcode image
        if os.path.exists(barcode_path):
            os.remove(barcode_path)

        return pdf_path

    except Exception as e:
        print(f"Error during PDF generation: {e}")
        raise

# Start the bot
bot.polling()
