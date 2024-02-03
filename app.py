from PIL import Image
import numpy as np
import streamlit as st

## LMS Daltonization
def rgb_to_lms(img):
    """
    lms_matrix = np.array(
        [[17.8824, 43.5161, 4.11935],
        [3.45565, 27.1554, 3.86714],
        [0.0299566, 0.184309, 1.46709]
        ]
        )
    """
    lms_matrix = np.array(
        [[0.3904725 , 0.54990437, 0.00890159],
        [0.07092586, 0.96310739, 0.00135809],
        [0.02314268, 0.12801221, 0.93605194]]
        )
    # Check if the image has an alpha channel
    if img.shape[2] == 4:
        # Separate the alpha channel
        alpha_channel = img[:, :, 3]
        # Perform the conversion only on the RGB channels
        lms_img = np.tensordot(img[:, :, :3], lms_matrix, axes=([2], [1]))
        # Reattach the alpha channel
        lms_img = np.dstack((lms_img, alpha_channel))
    else:
        # Perform the conversion as usual for RGB images
        lms_img = np.tensordot(img, lms_matrix, axes=([2], [1]))
    return lms_img
    # return np.tensordot(img, lms_matrix, axes=([2], [1]))

def lms_to_rgb(img):
    """
    rgb_matrix = np.array(
        [[0.0809444479, -0.130504409, 0.116721066],
        [0.113614708, -0.0102485335, 0.0540193266],
        [-0.000365296938, -0.00412161469, 0.693511405]
        ]
        )
    """
    rgb_matrix = np.array(
        [[ 2.85831110e+00, -1.62870796e+00, -2.48186967e-02],
        [-2.10434776e-01,  1.15841493e+00,  3.20463334e-04],
        [-4.18895045e-02, -1.18154333e-01,  1.06888657e+00]]
        )
    # Check if the image has an alpha channel
    if img.shape[2] == 4:
        # Separate the alpha channel
        alpha_channel = img[:, :, 3]
        # Perform the conversion only on the LMS channels
        rgb_img = np.tensordot(img[:, :, :3], rgb_matrix, axes=([2], [1]))
        # Reattach the alpha channel
        rgb_img = np.dstack((rgb_img, alpha_channel))
    else:
        # Perform the conversion as usual for LMS images
        rgb_img = np.tensordot(img, rgb_matrix, axes=([2], [1]))
    return rgb_img
    # return np.tensordot(img, rgb_matrix, axes=([2], [1]))

def simulate_colorblindness(img, colorblind_type):
    
    alpha_channel = None
    if img.shape[2] == 4:  # Image has an alpha channel
        alpha_channel = img[:, :, 3]  # Separate the alpha channel
        img = img[:, :, :3]  # Keep only the RGB channels

    lms_img = rgb_to_lms(img)
    if colorblind_type.lower() in ['protanopia', 'p', 'pro']:
        sim_matrix = np.array([[0, 0.90822864, 0.008192], [0, 1, 0], [0, 0, 1]], dtype=np.float16)
    elif colorblind_type.lower() in ['deuteranopia', 'd', 'deut']:
        sim_matrix =  np.array([[1, 0, 0], [1.10104433,  0, -0.00901975], [0, 0, 1]], dtype=np.float16)
    elif colorblind_type.lower() in ['tritanopia', 't', 'tri']:
        sim_matrix = np.array([[1, 0, 0], [0, 1, 0], [-0.15773032,  1.19465634, 0]], dtype=np.float16)
    else:
        raise ValueError('{} is an unrecognized colorblindness type.'.format(colorblind_type))
    lms_img = np.tensordot(lms_img, sim_matrix, axes=([2], [1]))
    # rgb_img = lms_to_rgb(lms_img)

    # Apply the simulation matrix to the LMS image
    lms_simulated = np.dot(lms_img, sim_matrix.T)

    # Convert the simulated LMS image back to RGB
    rgb_simulated = lms_to_rgb(lms_simulated)

    if alpha_channel is not None:
        rgb_simulated = np.dstack((rgb_simulated, alpha_channel))  # Reattach the alpha channel

    # Ensure the values are within the valid range
    rgb_simulated = np.clip(rgb_simulated, 0, 255).astype(np.uint8)

    return rgb_simulated
    # return rgb_img.astype(np.uint8)

def daltonize_correct(img, colorblind_type):
    colorblind_img = simulate_colorblindness(img, colorblind_type=colorblind_type)
    error_matrix = img - colorblind_img
    correction_matrix = np.array(
            [[0.0, 0.0, 0.0],
            [0.7, 1.0, 0.0],
            [0.7, 0.0, 1.0]]
            )
    corrected_error_matrix = np.tensordot(error_matrix, correction_matrix, axes=([2], [1]))
    return img + corrected_error_matrix

def main():
    
    st.set_page_config(layout="wide", page_title="Colorblind Image Tester", page_icon=":rainbow")

    st.title("Shot's Colorblind Image Test")

    sample_image1_path = 'images/sample_image_1.jpg'
    sample_image2_path = 'images/sample_image_2.png'
    
    with st.sidebar:
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
        
        sample_image1 = Image.open(sample_image1_path)
        st.image(sample_image1, use_column_width=True)
        
        colA1, colA2, colA3 = st.columns([1,3,1])
        with colA2:
        
            if st.button("Use Sample #1"):
                uploaded_file = sample_image1_path
        
        
        sample_image2 = Image.open(sample_image2_path)
        st.image(sample_image2, use_column_width=True)
        
        colB1, colB2, colB3 = st.columns([1,3,1])
        with colB2:
        
            if st.button("Use Sample #2"):
                uploaded_file = sample_image2_path
        
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        np_image = np.array(image)  # Convert PIL image to NumPy array for processing
        
        simulated_img_p = simulate_colorblindness(np_image, colorblind_type='p')
        simulated_img_d = simulate_colorblindness(np_image, colorblind_type='d')
        simulated_img_t = simulate_colorblindness(np_image, colorblind_type='t')
        grayscale_image = image.convert("L")

        # Convert NumPy array back to PIL Image for display
        simulated_img_p_pil = Image.fromarray(simulated_img_p)
        simulated_img_d_pil = Image.fromarray(simulated_img_d)
        simulated_img_t_pil = Image.fromarray(simulated_img_t)
        
        # Display images using Streamlit
        col1, col2, col3 = st.columns([1,4,1])
        with col2:
            st.image(image, caption='Original Image', use_column_width=True)

        colA1, colA2 = st.columns(2)
        
        with colA1:
            st.image(simulated_img_p_pil, caption='Simulated Protanopia', use_column_width=True)
            st.image(simulated_img_d_pil, caption='Simulated Deuteranopia', use_column_width=True)
        with colA2:
            st.image(simulated_img_t_pil, caption='Simulated Tritanopia', use_column_width=True)
            st.image(grayscale_image, caption='Simluated Achromatopsia', use_column_width=True)

if __name__ == "__main__":
    main()
