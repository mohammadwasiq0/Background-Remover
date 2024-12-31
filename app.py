import streamlit as st
from rembg import remove
from PIL import Image
import io
import requests

# App title
st.title("Background Remover App by Mohammad Wasiq & Zainul Abedeen")
st.write("Upload an image or provide an image URL to remove its background and download the result.")
st.write("Note: Please upload the image in .jpg and .png format.")

# Input option selection
input_option = st.radio("Select Input Option", ("Upload Image", "Image URL"))

if input_option == "Upload Image":
    # File uploader
    uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Load the image
        input_image = Image.open(uploaded_file)
        st.image(input_image, caption="Uploaded Image", use_column_width=True)

elif input_option == "Image URL":
    # URL input
    image_url = st.text_input("Enter Image URL")
    if image_url:
        try:
            # Fetch the image from the URL
            response = requests.get(image_url, stream=True)
            if response.status_code == 200:
                input_image = Image.open(io.BytesIO(response.content))
                st.image(input_image, caption="Image from URL", use_column_width=True)
            else:
                st.error("Failed to fetch image from URL. Please check the link.")
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Check if an image is available for processing
if 'input_image' in locals():
    # Remove background
    st.write("Removing background...")
    with st.spinner("Processing..."):
        input_bytes = io.BytesIO()
        input_image.save(input_bytes, format="PNG")
        output_bytes = remove(input_bytes.getvalue())
        output_image = Image.open(io.BytesIO(output_bytes))
    
    # Display result
    st.image(output_image, caption="Image without Background", use_column_width=True)

    # Download button
    output_buffer = io.BytesIO()
    output_image.save(output_buffer, format="PNG")
    output_buffer.seek(0)
    st.download_button(
        label="Download Image without Background",
        data=output_buffer,
        file_name="image_without_background.png",
        mime="image/png",
    )
