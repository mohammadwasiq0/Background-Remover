import streamlit as st
import cv2
import numpy as np
from rembg import remove

# Function to remove background
def remove_bg(image):
    return remove(image)

# Streamlit App
def main():
    st.title("Background Remover App")
    
    # File uploader
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        # Convert the file to an OpenCV image
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, 1)
        
        # Display the original image
        st.image(image, channels="BGR", caption="Original Image")
        
        # Remove background
        image_no_bg = remove_bg(image)
        
        # Display the image without background
        st.image(image_no_bg, channels="BGR", caption="Image without Background")
        
        # Download the image without background
        result = cv2.imencode('.png', image_no_bg)[1].tobytes()
        st.download_button("Download Image without Background", result, "image_no_bg.png")

if __name__ == "__main__":
    main()
