import streamlit as st
from PIL import Image
import numpy as np
import cv2
from colorblind import colorblind

# Function to convert PIL image to OpenCV format
def pil_to_cv(image):
    return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

# Function to convert OpenCV image to PIL format
def cv_to_pil(image):
    return Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

def main():
    
    st.set_page_config(layout="wide")

    # Streamlit app title
    st.title("Color Blindness Simulation")
            
    with st.sidebar:
        st.text("Select an Image To Test")
            # File uploader allows user to add their own image
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"], key="image")

    # If a file is uploaded, display it and apply the selected color blindness correction
    if uploaded_file is not None:

        image = Image.open(uploaded_file)
        cv_image = pil_to_cv(image)

        col1, col2, col3 = st.columns([1,4,1])
           
        colA1, colA2 = st.columns(2)
        colB1, colB2 = st.columns(2)
        
        with col2:
            st.image(image, caption='Original Image', use_column_width=True)
        
        with colA1:
            simulated_img = colorblind.simulate_colorblindness(cv_image, colorblind_type='protanopia')
            st.image(cv_to_pil(simulated_img), caption='Protanopia Image', use_column_width=True)

        with colA2:
            simulated_img = colorblind.simulate_colorblindness(cv_image, colorblind_type='deuteranopia')
            st.image(cv_to_pil(simulated_img), caption='Deuteranopia Image', use_column_width=True)

        with colB1:
            simulated_img = colorblind.simulate_colorblindness(cv_image, colorblind_type='tritanopia')
            st.image(cv_to_pil(simulated_img), caption='Tritanopia Image', use_column_width=True)

        with colB2:
            grayscale_image = image.convert('L')
            st.image(grayscale_image, caption='Grayscale Image', use_column_width=True)

            # Daltonizati
            # on correction
            # daltonized_img = colorblind.daltonize_correct(cv_image, colorblind_type=colorblind_type)
            # st.image(cv_to_pil(daltonized_img), caption='Daltonized Corrected Image', use_column_width=True)

            # # HSV correction
            # hsv_img = colorblind.hsv_color_correct(cv_image, colorblind_type=colorblind_type)
            # st.image(cv_to_pil(hsv_img), caption='HSV Corrected Image', use_column_width=True)

if __name__ == "__main__":
    main()