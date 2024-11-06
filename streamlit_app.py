import streamlit as st
import qrcode
from PIL import Image, ImageDraw, ImageOps
import io
import random
from io import BytesIO

# Function to generate a QR code with custom options
def generate_qr(data, error_correction, box_size, border, fill_color, back_color, logo_path=None, rounded=False, shadow=False, rotate_angle=0, background_img=None, custom_icon=None):
    qr = qrcode.QRCode(
        version=None,
        error_correction=error_correction,
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color=fill_color, back_color=back_color)

    # Apply logo (optional)
    if logo_path:
        logo = Image.open(logo_path)
        logo = logo.resize((50, 50))  # Resize logo
        img.paste(logo, (img.size[0] // 2 - 25, img.size[1] // 2 - 25), logo)

    # Apply rounded corners
    if rounded:
        img = img.convert("RGBA")
        img = ImageOps.expand(img, border=0, fill=back_color)
        img = round_corners(img, 20)

    # Apply shadow effect
    if shadow:
        img = img.convert("RGBA")
        shadow = img.copy()
        shadow = shadow.convert("RGBA")
        shadow = Image.new('RGBA', img.size, (0, 0, 0, 100))
        img = Image.alpha_composite(shadow, img)

    # Apply rotation
    img = img.rotate(rotate_angle, expand=True)

    # Apply background image
    if background_img:
        bg = Image.open(background_img)
        img = Image.composite(img, bg, img.convert("L"))

    # Custom Icon on QR code
    if custom_icon:
        icon = Image.open(custom_icon)
        icon = icon.resize((40, 40))  # Resize icon
        img.paste(icon, (img.size[0] // 2 - 20, img.size[1] // 2 - 20), icon)

    return img

# Function to round the corners of an image
def round_corners(img, radius):
    width, height = img.size
    circle = Image.new('L', (radius * 2, radius * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, radius * 2, radius * 2), fill=255)

    alpha = Image.new('L', img.size, 255)
    w, h = img.size
    alpha.paste(circle, (0, 0))
    alpha.paste(circle, (w - radius, 0))
    alpha.paste(circle, (0, h - radius))
    alpha.paste(circle, (w - radius, h - radius))

    img.putalpha(alpha)
    return img

# Function to generate a 3D perspective QR code effect
def generate_3d_qr(data, error_correction, box_size, border, fill_color, back_color):
    qr = qrcode.QRCode(
        version=None,
        error_correction=error_correction,
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color=fill_color, back_color=back_color)

    # Apply 3D perspective effect (simulation)
    img = img.convert("RGBA")
    img = img.rotate(45, expand=True)
    return img

# Streamlit UI
st.title("Advanced QR Code Generator")

# QR Code Type Selection
option = st.selectbox(
    "Select the type of QR code you want to create:",
    ("URL", "Contact Information (vCard)", "Email", "Geo Location", "Event (vCalendar)", "Text", "Wi-Fi", "SMS", "Payment Link", "3D Effect", "Dynamic Content")
)

# Collecting data based on selected QR code type
if option == "URL":
    data = st.text_input("Enter the URL:")
elif option == "Contact Information (vCard)":
    name = st.text_input("Enter your name:")
    email = st.text_input("Enter your email:")
    phone = st.text_input("Enter your phone number:")
    address = st.text_input("Enter your address:")
    company = st.text_input("Enter your company name:")
    data = f"BEGIN:VCARD\nVERSION:3.0\nFN:{name}\nEMAIL:{email}\nTEL:{phone}\nADR:{address}\nORG:{company}\nEND:VCARD"
elif option == "Email":
    email = st.text_input("Enter the email address:")
    subject = st.text_input("Enter the subject:")
    body = st.text_area("Enter the email body:")
    data = f"mailto:{email}?subject={subject}&body={body}"
elif option == "Geo Location":
    latitude = st.number_input("Enter Latitude:")
    longitude = st.number_input("Enter Longitude:")
    data = f"geo:{latitude},{longitude}"
elif option == "Event (vCalendar)":
    event_name = st.text_input("Enter the event name:")
    start_date = st.date_input("Enter the start date:")
    end_date = st.date_input("Enter the end date:")
    location = st.text_input("Enter event location:")
    data = f"BEGIN:VEVENT\nSUMMARY:{event_name}\nDTSTART:{start_date}\nDTEND:{end_date}\nLOCATION:{location}\nEND:VEVENT"
elif option == "Text":
    data = st.text_area("Enter the text data:")
elif option == "Wi-Fi":
    ssid = st.text_input("Enter Wi-Fi SSID:")
    password = st.text_input("Enter Wi-Fi Password:")
    encryption = st.selectbox("Select Encryption Type:", ["WPA", "WEP", "None"])
    data = f"WIFI:S:{ssid};T:{encryption};P:{password};;"
elif option == "SMS":
    phone = st.text_input("Enter the phone number:")
    message = st.text_input("Enter your message:")
    data = f"SMSTO:{phone}:{message}"
elif option == "Payment Link":
    payment_url = st.text_input("Enter your payment link:")
    data = payment_url
elif option == "3D Effect":
    data = st.text_input("Enter the data for 3D QR code:")
elif option == "Dynamic Content":
    data = f"https://api.example.com/qrdata/{random.randint(1000, 9999)}"  # Example dynamic data

# Additional customization options
error_correction = st.selectbox("Select Error Correction Level:", [
    qrcode.constants.ERROR_CORRECT_L,
    qrcode.constants.ERROR_CORRECT_M,
    qrcode.constants.ERROR_CORRECT_Q,
    qrcode.constants.ERROR_CORRECT_H,
])
box_size = st.slider("Select QR Code Size (box size):", 1, 10, 5)
border = st.slider("Select Border Size:", 1, 10, 4)
fill_color = st.color_picker("Select QR Code Color:", "#000000")
back_color = st.color_picker("Select Background Color:", "#FFFFFF")
logo = st.file_uploader("Upload Logo (optional):", type=["png", "jpg", "jpeg"])
rounded = st.checkbox("Rounded QR Code Blocks")
shadow = st.checkbox("Apply Shadow Effect")
rotate_angle = st.slider("Rotate QR Code (degrees):", 0, 360, 0)
background_img = st.file_uploader("Upload Background Image (optional):", type=["png", "jpg", "jpeg"])
custom_icon = st.file_uploader("Upload Custom Icon (optional):", type=["png", "jpg", "jpeg"])

# Generate QR Code button
if st.button("Generate QR Code"):
    if data:
        if option == "3D Effect":
            img = generate_3d_qr(data, error_correction, box_size, border, fill_color, back_color)
        else:
            img = generate_qr(data, error_correction, box_size, border, fill_color, back_color, logo, rounded, shadow, rotate_angle, background_img, custom_icon)

        # Show the generated QR Code
        st.image(img, caption="Your QR Code")

        # Allow download
        img_buffer = io.BytesIO()
        img.save(img_buffer, format="PNG")
        img_buffer.seek(0)

        st.download_button(
            label="Download QR Code",
            data=img_buffer,
            file_name="qr_code.png",
            mime="image/png",
        )
