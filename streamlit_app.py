import streamlit as st
import qrcode
import numpy as np
import io
from PIL import Image

# Dummy function for user authentication and profile management
def authenticate_user(username, password):
    return username == "user" and password == "password"

# Function to generate QR code
def generate_qr(data, error_correction, box_size, border, fill_color, back_color, logo_path=None):
    qr = qrcode.QRCode(
        version=None,
        error_correction=error_correction,
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color=fill_color, back_color=back_color)

    if logo_path:
        logo = Image.open(logo_path)
        logo = logo.resize((50, 50))  # Resize logo
        img.paste(logo, (img.size[0] // 2 - 25, img.size[1] // 2 - 25), logo)

    return img

# Placeholder for scan analytics
def get_scan_analytics():
    return {"QR Code 1": 50, "QR Code 2": 30}  # Dummy data

# Streamlit application layout
st.title("Advanced QR Code Generator")

# User Authentication
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.subheader("User Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    if st.button("Login"):
        if authenticate_user(username, password):
            st.session_state.authenticated = True
            st.success("Logged in successfully!")
        else:
            st.error("Invalid username or password.")

if st.session_state.authenticated:
    st.subheader("QR Code Creation")

    # QR Code Type Selection
    option = st.selectbox(
        "Select the type of QR code you want to create:",
        ("URL", "Contact Information (vCard)", "Promotional Material", "Wi-Fi", "SMS", "Payment Link")
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
        photo = st.file_uploader("Upload Photo (optional):", type=["png", "jpg", "jpeg"])
        data = f"BEGIN:VCARD\nVERSION:3.0\nFN:{name}\nEMAIL:{email}\nTEL:{phone}\nADR:{address}\nORG:{company}\nEND:VCARD"
    elif option == "Promotional Material":
        data = st.text_area("Enter your promotional material text:")
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

    # Additional QR code customization options
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
    caption = st.text_input("Add caption below QR Code (optional):")

    # Generate QR Code button
    if st.button("Generate QR Code"):
        if option in ["URL", "Contact Information (vCard)", "Promotional Material", "Wi-Fi", "SMS", "Payment Link"] and data:
            img = generate_qr(data, error_correction, box_size, border, fill_color, back_color, logo)

            # Show the generated QR Code
            st.image(img, caption="Your QR Code")

            # Add caption below QR Code
            if caption:
                st.write(caption)

            # Save QR code to a BytesIO object
            img_buffer = io.BytesIO()
            img.save(img_buffer, format="PNG")
            img_buffer.seek(0)

            # Download option
            st.download_button(
                label="Download QR Code",
                data=img_buffer,
                file_name="qr_code.png",
                mime="image/png",
            )

            # Placeholder for scan analytics
            analytics = get_scan_analytics()
            st.subheader("Scan Analytics (Demo Data)")
            st.bar_chart(analytics)

            # Show usage history
            st.subheader("Usage History")
            st.write("This feature will show the history of generated QR codes.")

    # Logout option
    if st.button("Logout"):
        st.session_state.authenticated = False
        st.success("Logged out successfully!")
