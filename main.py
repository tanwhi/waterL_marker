from flask import Flask, render_template, flash, redirect, url_for
from flask_bootstrap import Bootstrap5
from PIL import Image, ImageDraw, ImageFont
from forms import UploadPictureForm, ContactForm
import base64
import io

app = Flask(__name__)
Bootstrap5(app)
app.config['SECRET_KEY'] = 'secret!'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/examples')
def examples():
    return render_template('examples.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = UploadPictureForm()
    if form.validate_on_submit():
        photo = form.photo.data
        logo = form.logo.data
        name = form.name.data
        water_text = form.water_text.data

        if logo and water_text:
           flash('You cannot add Logo and Text at the same time', 'warning')
           return redirect(url_for('upload'))
        elif logo and not water_text:
            watermarked_logo = logo_watermark(photo, logo)
            photo_url = image_to_data_url(watermarked_logo)
            return render_template('download.html', photo=photo_url, name=name)
        elif water_text and not logo:
            watermarked_text = text_watermark(photo, water_text)
            photo_url = image_to_data_url(watermarked_text)
            return render_template('download.html', photo=photo_url, name=name)

    return render_template('upload.html', form=form)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        message = form.message.data
        flash('Thank you for contacting us. We will get back with you shortly.', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html', form=form)

@app.route('/download')
def download():
    return render_template('download.html')

def text_watermark(photo, water_text):
    # Open the main image
    base_image = Image.open(photo).convert("RGBA")

    # Create a transparent layer for the text
    text_layer = Image.new('RGBA', base_image.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(text_layer)

    # Specify font and text (adjust size as needed)
    # On Windows, fonts are often in C:\Windows\Fonts
    font = ImageFont.truetype("arial.ttf", 40)
    text = water_text

    # Calculate position (e.g., bottom right)
    width, height = base_image.size
    left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
    text_width = right - left
    text_height = bottom - top
    x = width - text_width - 10
    y = height - text_height - 10

    # Draw the text with some transparency (alpha=128)
    draw.text((x, y), text, font=font, fill=(255, 255, 255, 128))

    # Combine the layers and save
    watermarked = Image.alpha_composite(base_image, text_layer)
    # watermarked.convert("RGB").save('watermarked_photo.jpg')
    return watermarked

def logo_watermark(photo, logo_start):
    main = Image.open(photo)
    logo = Image.open(logo_start).convert("RGBA")  # Ensure logo has transparency

    # Optional: Resize logo to 10% of main image width
    logo_width = main.width // 10
    logo_height = int(logo.height * (logo_width / logo.width))
    logo = logo.resize((logo_width, logo_height))

    # Paste logo onto bottom-right corner
    # The third argument 'logo' acts as a mask to preserve transparency
    main.paste(logo, (main.width - logo.width - 20, main.height - logo.height - 20), logo)

    # main.save('logo_watermarked.jpg')
    return main

def image_to_data_url(image):
    buffer = io.BytesIO()
    image.convert("RGB").save(buffer, format="JPEG")
    encoded = base64.b64encode(buffer.getvalue()).decode("ascii")
    return f"data:image/jpeg;base64,{encoded}"

if __name__ == '__main__':
    app.run(debug=True)